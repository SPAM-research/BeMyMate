import re
import string

import argostranslate.translate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOllama
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser

already_defined_variables = []
variable_names = list(string.ascii_lowercase)

note_format = "variable is definition"
instructions = [
    f"Given a problem, variables and equations, define a variable {note_format} that hasn't been defined. Do not solve the problem. Your output must only be a variable definition {note_format}.",
    f"Given a problem, variables and equations, define a variable {note_format} that hasn't been defined. Do not solve the problem. Your output must only be a variable definition {note_format}. You must output something that isn't in the input.",
    f"Given a problem and some variables define a variable that hasn't been defined using the format {note_format}. Do not solve the problem. Output only the variable definition {note_format}.",
    f"Define a variable that hasn't been defined using the format {note_format}. Do not solve the problem. Output only the variable definition {note_format}.",
    f"Define a variable that hasn't been defined using the format {note_format} without solving the problem.",
    f"Your task is to define a variable with the format '{note_format}' without solving the problem.",
    f"Define a variable with the format '{note_format}' without solving the problem.",
]


def get_variable_definition(llm, problem):
    i = 0
    while True:
        if i >= len(instructions):
            empty += 1
            break
        output = get_llm_output(llm, problem, instructions[i])
        if output != "":
            # return "No sé que hacer..."
            break
        i += 1
    return clean_output(problem, output)


def get_llm_output(llm, problem, instructions):
    problem_text = problem.text
    notebook = ", ".join(problem.notebook)

    problem = f"""
    The problem: '{problem_text}'
    Variables: '{notebook}'
    Equations: ''
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", instructions),
            ("human", problem),
        ]
    )
    chain = prompt | llm
    llm_output = chain.invoke({}).content

    return llm_output


def clean_output(problem, output):
    output_lines = output.splitlines()

    global already_defined_variables
    already_defined_variables = [e[0] for e in problem.notebook]

    cleaned = output_lines
    cleaned = list(map(remove_beginning_whitespaces, cleaned))
    cleaned = list(filter(filter_operations, cleaned))
    cleaned = list(map(clean_represents, cleaned))
    cleaned = list(map(clean_defined_as, cleaned))
    cleaned = list(map(clean_var_colon, cleaned))
    cleaned = list(map(clean_var_equals, cleaned))
    cleaned = list(map(clean_let, cleaned))
    cleaned = list(map(clean_dash_var, cleaned))
    cleaned = list(map(clean_variable_is, cleaned))
    cleaned = list(map(clean_asterisk_var_colon, cleaned))
    cleaned = list(filter(filter_redundant, cleaned))
    cleaned = list(filter(filter_unwanted, cleaned))
    cleaned = list(filter(filter_input_or_empty, cleaned))

    joined = "\n".join(cleaned)
    translated = argostranslate.translate.translate(joined, "en", "es")
    output = translated.lower()

    return output


""" ################################
    Cleaning and filtering functions
    ################################ """


def clean_represents(i):
    match = re.search(r".+?(\"|\') represents.*?(?:,|\.|\n|$)", i)
    if match:
        var_name = (
            re.search(r"(\"|\').+?(\"|\')", match.group(0))
            .group(0)
            .replace('"', "")
            .replace("'", "")
        )
        definition = (
            re.sub(r".+? represents ", "", match.group(0))
            .replace(",", "")
            .replace("\n", "")
            .replace(".", "")
        )
        if var_name in already_defined_variables:
            return ""
        else:
            var = [v for v in variable_names if v not in already_defined_variables][0]
            already_defined_variables.append(var)
            return f"{var} is {definition}"
    else:
        return i


def clean_defined_as(i):
    match = re.search(r"\".+?\" can be defined as.*?(?:,|\.|\n|$)", i)
    if match:
        var_name = re.search(r"\".+?\"", match.group(0)).group(0).replace('"', "")
        definition = (
            re.sub(r"\".+?\" can be defined as ", "", match.group(0))
            .replace(",", "")
            .replace("\n", "")
            .replace(".", "")
        )
        if var_name in already_defined_variables:
            return ""
        else:
            var = [v for v in variable_names if v not in already_defined_variables][0]
            already_defined_variables.append(var)
            return f"{var} is {definition}"
    else:
        return i


def clean_let(i):
    match = re.search(r"Let .+? be .*?(?:,|\.|\n|$)", i)
    if match:
        var_name_aux = re.search(r"Let .+? ", match.group(0))
        var_name = re.search(r" .+? ", match.group(0)).group(0).replace(" ", "")
        definition = (
            re.sub(r"Let .+? be ", "", match.group(0))
            .replace(",", "")
            .replace("\n", "")
            .replace(".", "")
        )
        if var_name in already_defined_variables:
            return ""
        else:
            var = [v for v in variable_names if v not in already_defined_variables][0]
            already_defined_variables.append(var)
            return f"{var} is {definition}"
    else:
        return i


def clean_asterisk_var_colon(i):
    match = re.search(r"\*.+?(\"|\').+?(\"|\').*?(?:,|\.|\n|$)", i)
    if match:
        var_name = (
            re.search(r"\*.+?(\"|\').+?(\"|\')", match.group(0))
            .group(0)
            .replace(" ", "")
            .replace("*", "")
            .replace("'", "")
            .replace('"', "")
        )
        definition = (
            re.sub(r"\*.+?(\"|\').+?(\"|\') is ", "", match.group(0))
            .replace(",", "")
            .replace("\n", "")
            .replace(".", "")
        )
        if var_name in already_defined_variables:
            return ""
        else:
            var = [v for v in variable_names if v not in already_defined_variables][0]
            already_defined_variables.append(var)
            return f"{var} is {definition}"
    else:
        return i


def clean_var_colon(i):
    match = re.search(r"\*.+?:.*?(?:,|\.|\n|$)", i)
    if match:
        var_name = (
            re.search(r"\*.+?:", match.group(0))
            .group(0)
            .replace(" ", "")
            .replace("*", "")
            .replace(":", "")
        )
        definition = (
            re.sub(r"\*.+?: ", "", match.group(0))
            .replace(",", "")
            .replace("\n", "")
            .replace(".", "")
        )
        if var_name in already_defined_variables:
            return ""
        else:
            var = [v for v in variable_names if v not in already_defined_variables][0]
            already_defined_variables.append(var)
            return f"{var} is {definition}"
    else:
        return i


def clean_dash_var(i):
    match = re.search(r"-.+?:.*?(?:,|\.|\n|$)", i)
    if match:
        var_name = (
            re.search(r"-.+?:", match.group(0))
            .group(0)
            .replace(" ", "")
            .replace("-", "")
            .replace(":", "")
        )
        definition = (
            re.sub(r"\-.+?: ", "", match.group(0))
            .replace(",", "")
            .replace("\n", "")
            .replace(".", "")
        )
        if var_name in already_defined_variables:
            return ""
        else:
            var = [v for v in variable_names if v not in already_defined_variables][0]
            already_defined_variables.append(var)
            return f"{var} is {definition}"
    else:
        return i


def clean_var_equals(i):
    match = re.search(r"\*.+?=.*?(?:,|\.|\n|$)", i)
    if match:
        var_name = (
            re.search(r"\*.+?=", match.group(0))
            .group(0)
            .replace(" ", "")
            .replace("*", "")
            .replace("=", "")
        )
        print(var_name)
        definition = (
            re.sub(r"\*.+?= ", "", match.group(0))
            .replace(",", "")
            .replace("\n", "")
            .replace(".", "")
        )
        if var_name in already_defined_variables:
            return ""
        else:
            var = [v for v in variable_names if v not in already_defined_variables][0]
            return f"{var} is {definition}"
    else:
        return i


def clean_variable_is(i):
    match = re.search(r"The variable (\"|\').+?(\"|\') is .*?(?:,|\.|\n|$)", i)
    if match:
        var_name = (
            re.search(r"(\"|\').+?(\"|\')", match.group(0))
            .group(0)
            .replace('"', "")
            .replace("'", "")
        )
        definition = (
            re.sub(r"The variable (\"|\').+?(\"|\') is ", "", match.group(0))
            .replace(",", "")
            .replace("\n", "")
            .replace(".", "")
        )
        if var_name in already_defined_variables:
            return ""
        else:
            var = [v for v in variable_names if v not in already_defined_variables][0]
            already_defined_variables.append(var)
            return f"{var} is {definition}"
    else:
        return i


def filter_operations(l):
    return (
        not " = " in l
        and not " + " in l
        and not " - " in l
        and not " * " in l
        and not " / " in l
    )


def filter_input_or_empty(l):
    return (
        not re.search(r"^\s*The problem:", l)
        and not re.search(r"^\s*Variables:", l)
        and not re.search(r"^\s*Equations:", l)
        and not l.startswith("```")
        and not l == ""
    )


def filter_redundant(l):
    return not re.search(r"^where", l) and not ":" in l and not "=" in l


def filter_unwanted(l):
    return (
        not re.search(r"^\s*The variable definition for .+? is", l)
        and not re.search(r"^\s*The variable .+? is not defined", l)
        and not re.search(r"^\s*The variable that hasn't been defined is", l)
        and re.search(r"[a-zA-Z]", l)
        and not "?" in l
        and not l.startswith("The problem")
        and not l.startswith("*")
        and not l.startswith("-")
    )


def remove_beginning_whitespaces(l):
    return re.sub(r"^\s*", "", l)
