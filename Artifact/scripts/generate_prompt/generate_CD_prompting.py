import json
from pprint import pp

def make_basic_messages(system_prompt, prompt_template, query_ex):
    dialogs = [{"role": "system", "content": system_prompt}]
    prompt_dialogs = dialogs + [
        {"role": "user", "content": prompt_template.format(code="\n" + query_ex['code'].strip() + "\n")}
    ]
    return prompt_dialogs

def generate_CD_prompt_template_v1(args, query_ex=None):
    """
        Basic Cyclic Dependency Analysis Prompt
    """

    system_prompt = "You are a smart Program Analyst."
    prompt_template = "Please share the cyclic dependency analysis information of a program by enclosing the code in triple backticks: \n```{code}```"

    return make_basic_messages(system_prompt, prompt_template, query_ex)

def generate_CD_prompt_template_v2(args, query_ex=None):
    """
        Cyclic Dependency Analysis Prompt with Definition
    """

    system_prompt = """You are a Program Analyst. Users will provide you with a program, and you will analyze its cyclic dependencies."""
    prompt_template = """Please analyze and provide details on the cyclic dependencies in a Computer program.\n
-Definition: Cyclic dependency analysis involves understanding how dependencies form cycles within different parts of the program.\n\n
Now, based on the given information, Please share the cyclic dependency analysis details of a program by enclosing the code in triple backticks: \n```{code}```"""

    return make_basic_messages(system_prompt, prompt_template, query_ex)

def generate_CD_prompt_template_v3(args, query_ex=None):
    """
        Hands-on Cyclic Dependency Analysis Prompt with Example Scenario
    """

    system_prompt = """You are a Program Analyst. Users will provide you with a program, and you will analyze its cyclic dependencies."""
    
    prompt_template = """Please analyze and provide details on the cyclic dependencies in a program.
-Definition: Cyclic dependency analysis involves understanding how dependencies form cycles within different parts of the program.\n
-Example Scenario: Consider a program that involves multiple modules with interdependent imports. Analyze the cyclic dependencies to identify how modules are interconnected in a cyclic manner.\n\n
Now, based on the given information, please share the cyclic dependency analysis details by enclosing the code in triple backticks: \n```{code}```"""

    return make_basic_messages(system_prompt, prompt_template, query_ex)