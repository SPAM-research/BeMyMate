from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
import re

# model_to_use = "llama2:13b-chat"
# model_to_use = "vicuna:33b-q4_K_M"
# model_to_use = "orca-mini:13b-q6_K"
# model_to_use = "mistral-openorca:7b-fp16"
# model_to_use = "nous-hermes:7b-llama2-fp16"
# model_to_use = "nous-hermes:13b-llama2-q8_0"
model_to_use = "mistral:7b-instruct-fp16"  # model_to_use = "mistral:7b-instruct"

llm = ChatOllama(
    model=model_to_use,
    #callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    temperature=0,
)

already_defined_variables = []
variable_names = ["x", "y", "z", "u", "v", "w", "a", "b", "c", "d"]


def clean_represents(i):
    match = re.search(r".+?(\"|\') represents.*?(?:,|\.|\n|$)", i)
    if match:
        var_name = re.search(r"(\"|\').+?(\"|\')", match.group(0)).group(0).replace('"', "").replace("'", "")
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
            .replace("\"", "")
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
            .replace("\"", "")
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
    return (
        not re.search(r"^where", l)
        and not ":" in l
        and not "=" in l
    )

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


def get_already_defined_variables(nb):
    defined_variables = []
    if nb != "":
        entries = nb.split(", ")
        defined_variables = [e[0] for e in entries]
    already_defined_variables = defined_variables
    return defined_variables


def no_numbers_operators_or_definitions(i):
    return (
        not "=" in i
        and not "ariable definition" in i
        and not re.search(r"[0-9]", i)
    )

def remove_beginning_whitespaces(l):
    return re.sub(r"^\s*", "", l)



def test_problem(problem, instructions):
    problem_text = problem[0]
    notebook = problem[1]

    problem = f"""
    The problem: '{problem_text}'
    Variables: '{notebook}'
    Equations: ''
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_input}"),
            ("human", "{human_input}"),
        ]
    )

    chain = prompt | llm

    llm_output = chain.invoke(
        {"system_input": instructions, "human_input": problem}
    ).content

    output_lines = llm_output.splitlines()

    global already_defined_variables
    already_defined_variables = get_already_defined_variables(notebook)

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


    removed_input_and_empty = list(filter(filter_input_or_empty, cleaned))

    """ #############################
        ##   BE CAREFUL WITH THIS  ##
        ############################# """
    #removed_input_and_empty = list(filter(no_numbers_operators_or_definitions, removed_input_and_empty))

    cleaned_output = "\n".join(removed_input_and_empty)

    return [llm_output, cleaned_output]
