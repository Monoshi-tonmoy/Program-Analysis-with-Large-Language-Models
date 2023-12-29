import json
from pprint import pp

def make_basic_messages(system_prompt, prompt_template, query_ex):
    dialogs = [{"role": "system", "content": system_prompt}]
    prompt_dialogs = dialogs + [
        {"role": "user", "content": prompt_template.format(code="\n" + query_ex['code'].strip() + "\n")}
    ]
    return prompt_dialogs

def generate_DFG_prompt_template_v1(args, query_ex=None):
    """
        Basic Dataflow Prompt
    """

    system_prompt = "You are a Program Analyst. Users will provide you with a program, and you will analyze its dataflow."
    prompt_template = "Please share the dataflow information of a program by enclosing the code in triple backticks: \n```{code}```"

    return make_basic_messages(system_prompt, prompt_template, query_ex)

def generate_DFG_prompt_template_v2(args, query_ex=None):
    """
        Dataflow Prompt with Definition
    """
    system_prompt = """You are a Program Analyst. Users will provide you with a program, and you will analyze its dataflow."""
    prompt_template = """Please analyze and provide details on the dataflow in a Computer program.\n
-Definition: Dataflow information includes understanding how data is manipulated and flows through different parts of the program.\n\n
Now, based on the given information, Please share the dataflow details of a program by enclosing the code in triple backticks: \n```{code}```"""

    return make_basic_messages(system_prompt, prompt_template, query_ex)


def generate_DFG_prompt_template_v3(args, query_ex=None):
    """
        Hands-on Dataflow Prompt with Example Scenario
    """

    system_prompt = """You are a Program Analyst. Users will provide you with a program, and you will analyze its dataflow."""
    
    prompt_template = """Please analyze and provide details on the dataflow in a program.
-Definition: Dataflow information includes understanding how data is manipulated and flows through different parts of the program.\n
-Example Scenario: Consider a program that sorts an array of integers. Analyze the dataflow to identify how the elements are manipulated during the sorting process.\n\n
Now, based on the given information, please share the dataflow details by enclosing the code in triple backticks: \n```{code}```"""

    return make_basic_messages(system_prompt, prompt_template, query_ex)

