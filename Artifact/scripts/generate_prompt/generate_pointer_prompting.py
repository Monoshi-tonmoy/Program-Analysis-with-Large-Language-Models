import json
from pprint import pp

def make_basic_messages(system_prompt, prompt_template, query_ex):
    dialogs = [{"role": "system", "content": system_prompt}]
    prompt_dialogs = dialogs + [
        {"role": "user", "content": prompt_template.format(code="\n" + query_ex['code'].strip() + "\n")}
    ]
    return prompt_dialogs

def generate_pointer_prompt_template_v1(args, query_ex=None):
    """
        Low specificity, low Context, Single Prompt
    """

    system_prompt = "You are a super smart Program Analyst."
    prompt_template = "Analyze the pointers in the following code.\n```{code}```"

    return make_basic_messages(system_prompt, prompt_template, query_ex)

def generate_pointer_prompt_template_v2(args, query_ex=None):
    """
        Low specificity, low Context, Single Prompt
    """

    system_prompt = "You are a super smart Program Analyst."
    prompt_template = "Are there any potential issues with the following pointer use? \n```{code}```"

    return make_basic_messages(system_prompt, prompt_template, query_ex)

def generate_pointer_prompt_template_v3(args, query_ex=None):
    """
        Low specificity, High context, Single prompt
    """

    system_prompt = "You are a program analyst specializing in security vulnerabilities related to memory, buffer, and pointer misuse."
    
    prompt_template = """The following C / C++ code may or may not contain misuses such as memory, buffer or pointer issues, and is enclosed in triple backticks. Analyze the following code\n'''{code}'''"""

    return make_basic_messages(system_prompt, prompt_template, query_ex)

def generate_pointer_prompt_template_v4(args, query_ex=None):
    """
        High specificity, Low context, Single prompt
    """

    system_prompt = "You are a super smart Program Analyst."
    
    prompt_template = """Analyze this code snippet given by triple backticks for the following:
-Bad pointer arithmetic
-Unsafe dereferencing
-Buffer overflow or buffer underwrite
-Bad allocation / deallocation
-Improper sanitization of input
\n'''{code}'''"""

    return make_basic_messages(system_prompt, prompt_template, query_ex)



def generate_pointer_prompt_template_v5(args, query_ex=None):
    """
        High specificity, Low context, Single prompt
    """

    system_prompt = "You are a super smart Program Analyst."
    
    prompt_template = """Analyze this code snippet given by triple backticks for the following:
-Bad pointer arithmetic
-Unsafe dereferencing
-Buffer overflow or buffer underwrite
-Bad allocation / deallocation
-Improper sanitization of input
\n'''{code}'''"""

    return make_basic_messages(system_prompt, prompt_template, query_ex)
