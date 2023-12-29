import argparse

import tqdm

from utils import *
from models import *
from generate_prompt import *
from global_variables import data_dir, result_dir, models_ids, api_types
import transformers


def get_model(args, tokenizer_only=False):
    model = Model(model_id=models_ids[args.model], api_type=api_types[args.model], tokenizer_only=tokenizer_only)
    return model

def get_prompt(args=None, query_ex=None):
    generate_prompt_function = eval(f"generate_{args.mode}_prompt_template_v{args.template}")
    prompt = generate_prompt_function(args, query_ex=query_ex)
    print(prompt)
    return prompt

def get_answer(args=None, query_ex=None):
    prompt = get_prompt(args=args, query_ex=query_ex)
    if args.model_ is None:
        args.model_ = get_model(args)
    return args.model_.query(prompt, return_metadata=True)

def add_arguments(parser):
    parser.add_argument("--model", type=str, default="llama")
    parser.add_argument("--dataset",type=str)
    parser.add_argument("--template", type=int, default=1)
    parser.add_argument("--mode", default="basic")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()

    args.model_ = None
    args.data = read_jsonl(f"{data_dir}/{args.dataset}.jsonl")
    
    results = []


    for i, ex in enumerate(tqdm.tqdm(args.data)):
        response = get_answer(args, ex)
        results.append(response)
        write_file(f"{result_dir}/{args.model}/{args.mode}_prompt_template_{args.template}/details/example_{ex['idx']}.txt", response["output"])
        write_file(f"{result_dir}/{args.model}/{args.mode}_prompt_template_{args.template}/details/example_{ex['idx']}_tokens.txt", str(response["output_tokens"]))
        write_file(f"{result_dir}/{args.model}/{args.mode}_prompt_template_{args.template}/details/example_{ex['idx']}_input.txt", response["input_json"])



