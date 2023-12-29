import json
from pprint import pp

def make_basic_messages(system_prompt, prompt_template, query_ex):
    dialogs = [{"role": "system", "content": system_prompt}]
    prompt_dialogs = dialogs + [
        {"role": "user", "content": prompt_template.format(code="\n" + query_ex['code'].strip() + "\n")}
    ]
    return prompt_dialogs

def generate_CFG_prompt_template_v1(args, query_ex=None):
    """
        Basic Prompt
    """

    system_prompt = "You are a Program Analyst. Users will provide you with a program, and you will analyze its control flow."
    prompt_template = "Please share the control flow information of a program by enclosing the code in triple backticks: \n```{code}```"

    return make_basic_messages(system_prompt, prompt_template, query_ex)

def generate_CFG_prompt_template_v2(args, query_ex=None):
    """
        Basic prompt with definition
    """

    system_prompt = """You are a Program Analyst. Users will provide you with a program, and you will analyze its control flow."""
    prompt_template = """Please analyze and provide details on the decision points and loops in the control flow of a Computer program.\n
-Definition: Control flow information includes understanding how the program executes through different paths.\n\n
Now, based on the given information, Please share the control flow information of a program by enclosing the code in triple backticks: \n```{code}```"""

    return make_basic_messages(system_prompt, prompt_template, query_ex)


def generate_CFG_prompt_template_v3(args, query_ex=None):
    """
        Hands-on Prompt with Example Scenario
    """

    system_prompt = """You are a Program Analyst. Users will provide you with a program, and you will analyze its control flow."""
    
    prompt_template = """Please analyze and provide details on the decision points and loops in the control flow of a program.
-Definition: Control flow information includes understanding how the program executes through different paths.\n
-Example Scenario: Consider a program that calculates the average of an array of integers. Analyze the control flow to identify key decision points and loops.\n\n
Now, based on the given information, please share the control flow details by enclosing the code in triple backticks: \n```{code}```"""

    return make_basic_messages(system_prompt, prompt_template, query_ex)


