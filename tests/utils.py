import random
import re
import string

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOllama
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from sympy import SympifyError, sympify
from unidecode import unidecode

# model_to_use = "llama2:13b-chat"
# model_to_use = "vicuna:33b-q4_K_M"
# model_to_use = "orca-mini:13b-q6_K"
# model_to_use = "mistral-openorca:7b-fp16"
# model_to_use = "nous-hermes:7b-llama2-fp16"
# model_to_use = "nous-hermes:13b-llama2-q8_0"
model_to_use = "llama3:latest"  # model_to_use = "mistral:7b-instruct"
# model_to_use = "dolphin2.1-mistral:7b"  # model_to_use = "mistral:7b-instruct"

llm = ChatOllama(
    model=model_to_use,
    # callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    temperature=0,
)


already_defined_vars = ["x"]
variable_names = list(string.ascii_lowercase)
variable_regex = "[\"'`]?(?P<variable>[a-zA-Z_\(\)\|]+?)[\"'`]"
ending_regex = "(?:,|\(|\.|:|\n|$| and)"


def get_already_defined_variables(nb):
    defined_variables = []
    if nb != "":
        entries = nb.split(", ")
        defined_variables = [e[0] for e in entries]
    already_defined_vars = defined_variables
    return defined_variables


def substitute_multicharacter_variables(original_equations, original_explanation):
    equations = "\n".join(original_equations)
    explanation = "\n".join(original_explanation)

    matches = re.findall(r"[A-Za-z_ ]+", equations)
    matches = list(map(str.strip, matches))
    matches = list(filter(lambda m: m != "", matches))
    matches = list(set(matches))

    multichar_variables = [v for v in matches if len(v) > 1 and not v.startswith("p(")]
    monochar_variables = [v for v in matches if len(v) == 1]

    usable_var_names = [
        v
        for v in variable_names
        if not v in monochar_variables and not v in already_defined_vars
    ]
    random.shuffle(usable_var_names)

    for m in multichar_variables:
        v = usable_var_names.pop()
        equations = equations.replace(m, v)
        # explanation = explanation.replace(m, v)
        explanation = f"{explanation}\n{v} is {m}"

    return [equations.splitlines(), explanation.splitlines()]


def clean_where(i):
    definitions = []
    if re.search("^[a-zA-Z_\(\)\|]+ is .+?", i):
        return i
    match = re.finditer(
        f"{variable_regex}? (is|represents) (?P<description>.*?){ending_regex}", i
    )
    for m in match:
        definitions.append(f"{m.group('variable')} is {m.group('description')}")
    if definitions:
        return "\n".join(definitions)
    else:
        return i


def clean_lets_define(i):
    definitions = []
    if re.search("^[a-zA-Z_\(\)\|]+ is .+?", i):
        return i
    match = re.finditer(
        f"{variable_regex}? to represent (?P<description>.*?){ending_regex}", i
    )
    for m in match:
        definitions.append(f"{m.group('variable')} is {m.group('description')}")
    if definitions:
        return "\n".join(definitions)
    else:
        return i


def clean_let(i):
    definitions = []
    if re.search("^[a-zA-Z_\(\)\|]+ is .+?", i):
        return i
    match = re.finditer(
        f"[L|l]et {variable_regex}? be (?P<description>.*?){ending_regex}", i
    )
    for m in match:
        if m.group("variable") != "would":
            definitions.append(f"{m.group('variable')} is {m.group('description')}")
    if definitions:
        return "\n".join(definitions)
    else:
        return i


def clean_redundant(list_in):
    monochar_definitions = [d for d in list_in if re.match(r"^[a-z_] is .*", d)]
    multichar_definitions = [d for d in list_in if re.match(r"^[a-z_]{2,} is .*", d)]
    list_out = list_in[:]

    for multi in multichar_definitions:
        multi_match = re.search(
            f"{variable_regex}? is (?P<description>.*?)(?:,|\.|:|\n|$| and)", multi
        )
        multi_v = multi_match.group("variable")
        multi_def = multi_match.group("description")
        for mono in monochar_definitions:
            mono_match = re.search(
                f"{variable_regex}? is (?P<description>.*?)(?:,|\.|:|\n|$| and)", mono
            )
            mono_v = mono_match.group("variable")
            mono_def = mono_match.group("description")
            if multi_v == mono_def:
                list_out.remove(multi)
                list_out.remove(mono)
                list_out.append(f"{mono_v} is {multi_def}")
    return list_out


def remove_formatting(l):
    l = re.sub(r"^\s*", "", l)
    l = re.sub(r"\*([a-zA-Z_0-9]+)\*", r"\1", l)
    l = re.sub(r"^\(?[a-z]\)\s*", "", l)
    return l


def remove_parenthesis(e):
    return re.sub(r"\((.)\)", r"\1", e)


def is_equation(l):
    return "=" in l


def is_well_formed(l):
    expression = re.sub(r"([0-9]+)([A-Za-z_ ]+)", r"\1*\2", l).replace("=", "+")
    try:
        sympify(expression)
        return True
    except SympifyError:
        return False


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

    preprocessed = unidecode(llm_output)
    preprocessed = preprocessed.replace(":", ":\n")
    preprocessed = preprocessed.replace("\\", "")
    output_lines = preprocessed.splitlines()

    global already_defined_vars
    already_defined_vars = get_already_defined_variables(notebook)

    output_lines = [l for l in output_lines if l != "" and not "```" in l]
    output_lines = list(map(remove_formatting, output_lines))

    equations = list(filter(is_equation, output_lines))
    equations = list(map(lambda l: l.replace("\\", ""), equations))

    explanation = list(filter(lambda l: not is_equation(l), output_lines))

    [equations, explanation] = substitute_multicharacter_variables(
        equations, explanation
    )

    explanation = list(map(clean_let, explanation))
    explanation = list(map(clean_lets_define, explanation))
    explanation = list(map(clean_where, explanation))

    equations = list(map(remove_parenthesis, equations))
    equations = list(map(lambda l: re.sub(r"^\*\s*", "", l), equations))
    equations = list(map(lambda l: re.sub(r"^-\s*", "", l), equations))
    equations = list(map(lambda l: re.sub(r"\*$", "", l), equations))

    explanation = "\n".join(explanation).splitlines()
    explanation = list(filter(lambda e: ":" not in e, explanation))
    explanation = clean_redundant(explanation)
    explanation = list(filter(lambda e: re.search(r"^[a-z] is", e), explanation))

    equations = "\n".join(list(filter(lambda e: e != "", equations)))
    explanation = (
        "\n".join(list(filter(lambda e: e != "", explanation)))
        .replace("_", " ")
        .lower()
    )
    cleaned_output = f"{equations}\n====\n{explanation}"
    return [llm_output, cleaned_output]
