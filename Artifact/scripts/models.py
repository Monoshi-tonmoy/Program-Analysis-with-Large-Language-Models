import json
import os
import gc

import backoff
import dotenv
import torch
import openai
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, AutoModelForSeq2SeqLM


class Model:
    def __init__(self, model_id, api_type="hf", tokenizer_only=False, print_only_mode=False) -> None:
        self.print_only_mode = print_only_mode
        self.model_id = model_id
        self.api_type = api_type
        self.tokenizer_only = tokenizer_only
        self.initialize()
        self.prefix = None
    
    def initialize_openai(self):
        dotenv.load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def initialize_hf(self):
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16
        )
        print(self.model_id)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        if not self.tokenizer_only:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                quantization_config=quantization_config,
                device_map="auto",
            )
    
    def initialize(self):
        if self.api_type == "openai":
            self.initialize_openai()
        else:
            self.initialize_hf()

    def tokenize_llama(self, dialogs):
        assert len(dialogs) >= 1, "Invalid dialogs"
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
        
        
        print(dialogs[0])
        if dialogs[0]["role"] == "system":
            dialogs = [
                {
                    "role": dialogs[1]["role"],
                    "content": B_SYS + dialogs[0]["content"] + E_SYS + dialogs[1]["content"],
                }
            ] + dialogs[2:]
        dialog_tokens = []
        for prompt, answer in zip(dialogs[::2], dialogs[1::2]):
            assert prompt["role"] == "user", prompt["role"]
            assert answer["role"] == "assistant", answer["role"]
            inputs = self.tokenizer.encode(
                f"{B_INST} {(prompt['content']).strip()} {E_INST} {(answer['content']).strip()} ",
                add_special_tokens=False
            )
            input_ids = [self.tokenizer.bos_token_id] + inputs + [self.tokenizer.eos_token_id]
            dialog_tokens.extend(input_ids)
        
        inputs = self.tokenizer.encode(
            f"{B_INST} {(dialogs[-1]['content']).strip()} {E_INST}",
            add_special_tokens=False,
        )
        dialog_tokens.extend([self.tokenizer.bos_token_id] + inputs)
        if self.prefix is not None:
            dialog_tokens.extend(self.tokenizer.encode(self.prefix, add_special_tokens=False))
        return torch.tensor([dialog_tokens]).to("cuda")

    
    
    def tokenize_falcon(self, dialogs):
        text = ""
        for prompt in dialogs:
            if prompt['role'] == 'system':
                text += prompt["content"] + "\n\n"
            elif prompt['role'] == 'user':
                text += "\n" + prompt["content"] + "\n\n"
            else:
                text += "Output"+prompt["content"] + "\n\n"
        text += "Output\n"
        if self.prefix is not None:
            text += self.prefix
        return self.tokenizer.encode(text, return_tensors="pt").to("cuda")
    
    
    
    def tokenize_starcoder(self, dialogs):
        system_token, user_token = "<|system|>", "<|user|>"
        assistant_token, end_token = "<|assistant|>", "<|end|>"
        text = ""
        for prompt in dialogs:
            if prompt['role'] == 'system':
                text += system_token + "\n" + prompt['content'] + end_token + "\n"
            elif prompt['role'] == 'user':
                text += user_token + "\n" + prompt["content"] + end_token + "\n"
            else:
                text += assistant_token + "\n" + prompt["content"] + end_token + "\n"
        text += assistant_token
        if self.prefix is not None:
            text += self.prefix
        return self.tokenizer.encode(text, return_tensors="pt").to("cuda")

    def tokenize_wizardcoder(self, dialogs):
        text = ""
        for prompt in dialogs:
            if prompt['role'] == 'system':
                text += prompt["content"] + "\n\n"
            elif prompt['role'] == 'user':
                text += "### Instruction:\n" + prompt["content"] + "\n\n"
            else:
                text += "### Response:\n" + prompt["content"] + "\n\n"
        text += "### Response:\n"
        if self.prefix is not None:
            text += self.prefix
        return self.tokenizer.encode(text, return_tensors="pt").to("cuda")
    

    
    def tokenize(self, dialogs):

        if self.api_type == "llama":
            return self.tokenize_llama(dialogs)
        elif self.api_type == "starcoder":
            return self.tokenize_starcoder(dialogs)
        elif self.api_type == "wizardcoder":
            return self.tokenize_wizardcoder(dialogs)
        elif self.api_type=="falcon":
            return self.tokenize_falcon(dialogs)
        else:
            pass


    @backoff.on_exception(backoff.expo, openai.error.ServiceUnavailableError)
 
    @backoff.on_exception(backoff.expo, openai.error.RateLimitError, giveup=lambda ex: "You exceeded your current quota" in str(ex))
    def query_openai(self, dialogs, return_metadata):
        if self.prefix is not None:
            dialogs[-1]["content"] += self.prefix

        completion = openai.ChatCompletion.create(
            model=self.model_id, 
            messages=dialogs,
            n=1,
            temperature=0.1,
            max_tokens=512,
        )
        if return_metadata:
            return {
                "input_json": json.dumps(dialogs),
                "output_completion": completion,
                "output_tokens": [],
                "output": completion["choices"][0]["message"]["content"],
            }
        else:
            return completion["choices"][0]["message"]["content"]

    def query_hf(self, dialogs, return_metadata):
        input_ids = self.tokenize(dialogs)
        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_new_tokens=512,

                # do_sample=False,

                do_sample=True,
                top_p=0.9,
                temperature=0.1,

                pad_token_id=self.tokenizer.pad_token_id,
            )
        output = output.to("cpu")[0]
        print("RESPONSE WITHOUT INPUT:", self.tokenizer.decode(output[input_ids.shape[1]:]))
        if return_metadata:
            ret = {
                "input_json": json.dumps(dialogs),
                "output_tokens": self.tokenizer.convert_ids_to_tokens(output),
                "output": self.tokenizer.decode(output),
                "output_without_input": self.tokenizer.decode(output[input_ids.shape[1]:]),
            }
        else:
            ret = self.tokenizer.decode(output)
        del input_ids
        gc.collect()
        torch.cuda.empty_cache()
        gc.collect()
        return ret

    def query(self, dialogs, return_metadata=False):
        if self.print_only_mode:
            print_dialog(dialogs, True, self)
        if self.api_type == "openai":
            return self.query_openai(dialogs, return_metadata=return_metadata)
        else:
            return self.query_hf(dialogs, return_metadata=return_metadata)
