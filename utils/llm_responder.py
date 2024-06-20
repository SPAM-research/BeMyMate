from langchain_community.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from unidecode import unidecode
from sympy import sympify, SympifyError
import re
import string
import random
from models.problem import Problem


already_defined_vars = []
variable_regex="[\"\'`]?(?P<variable>[a-zA-Z_\(\)\|]+?)[\"\'`]"
ending_regex = "(?:,|\(|\.|:|\n|$| and)"
debug = False
# 3- Each equation only uses previously introduced variables. 
# 4- Each quantity is only named by one variable.
# mistral
instructions_mistral = "Given a problem, variables and equations, define an equation that hasn't been defined. Do not solve the problem. Your output must only be an equation. Follow the suggestion."

# stable-beluga
instructions_stable_beluga_definitions = "Please, given a [PROBLEM STATEMENT] and [VARIABLES], define all the remaining variables (for example, 'x is number of apples'). Do not solve the problem. Each line of your output must contain a variable definition. Follow the suggestion. HINT: The needed [VARIABLES] are present on the problem statement."
instructions_stable_beluga_equations = "Please, given a [PROBLEM STATEMENT], [VARIABLES] and [EQUATIONS], define all the remaining [EQUATIONS]. Do not solve the problem. Each line of your output must contain an equation. Follow the suggestion."

# mixtral
instructions_mixtral = """Given a problem, variables and equations, define all the remaining variables and equations. Each line of your output must contain a variable definition or an equation. A variable definition is '<letter> is <definition>'. An equations is '<letter> = <expression>'. Follow the suggestion. Do not explain the variable definitions or the equations. Your output should have the following format:
x is number of oranges
y is number of apples
z is number of fruits
z = x+y"""

instructions_definitions = instructions_stable_beluga_definitions
instructions_equations = instructions_stable_beluga_equations


instructions_review = """
Please act as an impartial judge and evaluate the quality of the response provided to predict the next step to solve a mathematical problem displayed below. Your evaluation should consider helpfulness, relevance, and accuracy. Be as objective as possible.

Variables must be defined as '<letter> is <description>'. It is mandatory that every variable is defined as '<letter> is <description>', a variable CANNOT be defined on an equation. A variable that is not defined in [VARIABLES] cannot be used in an equation.
Variables CANNOT be infered. THEY MUST BE EXPLICITLY DEFINED ON [VARIABLES], OTHERWISE RETURN FALSE.
Your output verdict must strictly follow this format:

"True" if the message advances the resolution status of the mathematical problem by defining variables or using defined variables in equations.
"False" if it does not.
Take into account that equations must include variables that are defined in [VARIABLES]. Defining variables is crucial, even if they may be incorrect, as it counts as advancing the resolution status. Valid declarations of variables could be, for example, 'z is the current age of Abigail' or 'y is the current age of Jonathan' if they are related to the [PROBLEM STATEMENT].

[Message]
"""

instructions_conversational = """
Please act as a kid. You are going to solve MWP problems with another student. You will be provided with the current
resolution status of the problem. Your response must be adjusted to the message sent by the user. You will respond to [LAST MESSAGE] as a kid.
You are provided with the [PROBLEM STATEMENT], [VARIABLES] and [EQUATIONS], the objective is to define the equations and variables that allow to solve the problem.
Your output must be KID: <message>. DO NOT SOLVE THE PROBLEM. You want to solve the problem but remember you are a 7 year old kid who just learnt maths, so these are difficult problems for you

[Message]
"""

instructions_should_speak = """
Please act as an impartial judge and evaluate the messages of the [CHAT].
The [CHAT] contains messages from a collaborative ITS, on which students chat with other students and the system in order
to solve MWP.
Given the context, specially the messages sent by users (not 'system' and not 'agent'), you must decide 
whether the message which is going to be sent by 'agent' has to solve the MWP (define a variables or an equation) or 
converse with the kid.
You are provided with the last message sent by the human user on [LAST_MESSAGE_USER]
Be as objective as possible.
Your output verdict must strictly follow this format:
"True" if the agent has to answer to the student, because the student asked a question, said a reasonable thought, and so on.
"False" if the agent has to advance the resolution of the MWP. This might be because the student is proposing solutions to advance the MWP (you can infere if the MWP is advancing by analizing the response of the system on [SYSTEM_RESPONSE]) or the SYSTEM_RESPONSE is providing help.


[Message]
"""

""" Add an explicit multiplication sign if needed for each equation."""
def add_multiplication_sign(equations: list[str]) -> list[str]:
    modified_equations = []
    for expression in equations:
        modified_expression = expression
        # Add explicit multiplication symbol in expressions such as 2(x-6) or x(y+2)
        modified_expression = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', modified_expression)  # Letter followed by a number
        modified_expression = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', modified_expression)  # Number followed by a letter
        modified_expression = re.sub(r'(\d+)(\()', r'\1*\2', modified_expression)  # Number followed by a parenthesis
        modified_expression = re.sub(r'([a-zA-Z])(\()', r'\1*\2', modified_expression)  # Letter followed by a parenthesis
        modified_expression = re.sub(r'(\))(\d+)', r'\1*\2', modified_expression)  # Parenthesis followed by a number
        modified_expression = re.sub(r'(\))([a-zA-Z])', r'\1*\2', modified_expression)  # Parenthesis followed by a letter
        modified_equations.append(modified_expression)
    return modified_equations

def get_already_defined_variables(nb):
    return [e[0] for e in nb]

def substitute_multicharacter_variables(original_equations, original_explanation):
    equations = "\n".join(original_equations)
    explanation = "\n".join(original_explanation)
    
    matches = re.findall(r"[A-Za-z_ ]+", equations)
    matches = list(map(str.strip, matches))
    matches = list(filter(lambda m: m != "", matches))
    matches = list(set(matches))

    multichar_variables = [v for v in matches if len(v) > 1 and not v.startswith("p(")]
    monochar_variables = [v for v in matches if len(v) == 1]
    
    usable_var_names = [v for v in list(string.ascii_lowercase) if v not in already_defined_vars]
    random.shuffle(usable_var_names)
    
    for m in multichar_variables:
        v = usable_var_names.pop()
        equations = equations.replace(m, v)
        #explanation = explanation.replace(m, v)
        explanation = f"{explanation}\n{v} is {m}"

    return [equations.splitlines(), explanation.splitlines()]

def clean_where(i):
    definitions = []
    if re.search("^[a-zA-Z_\(\)\|]+ is .+?", i):
        return i
    match = re.finditer(f"{variable_regex}? (is|represents) (?P<description>.*?){ending_regex}", i)
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
    match = re.finditer(f"{variable_regex}? to represent (?P<description>.*?){ending_regex}", i)
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
    match = re.finditer(f"[L|l]et {variable_regex}? be (?P<description>.*?){ending_regex}", i)
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
        multi_match = re.search(f"{variable_regex}? is (?P<description>.*?)(?:,|\.|:|\n|$| and)", multi)
        multi_v = multi_match.group("variable")
        multi_def = multi_match.group("description")
        for mono in monochar_definitions:
            mono_match = re.search(f"{variable_regex}? is (?P<description>.*?)(?:,|\.|:|\n|$| and)", mono)
            mono_v = mono_match.group("variable")
            mono_def = mono_match.group("description")
            if multi_v == mono_def:
                list_out.remove(multi)
                # Try added on Thurday, April 11, 2024
                try: list_out.remove(mono)
                except: ...
                list_out.append(f"{mono_v} is {multi_def}")
    return list_out
    
def remove_formatting(l):
    l = re.sub(r"^\s*", "", l)
    l = re.sub(r'\*([a-zA-Z_0-9]+)\*', r'\1', l)
    l = re.sub(r"^\(?[a-z]\)\s*", "", l)
    return l
    
def remove_parenthesis(e):
    return re.sub(r'\((.)\)', r'\1', e)

def is_equation(l):
    return "=" in l

def construct_chat_history(chat):
    return [{"sender": "system" if e["sender"]=="system" else "you", "message": e["message"]} for e in chat]
    return "\n".join([e["message"] for e in chat[-6:] if e["sender"]=="system"])
    output = ""
    for e in chat:
        output += f"{e['sender']}: {e['message']}\n"
    #print(output)
    return output

def should_llm_speak_with_student(llm: ChatOllama, chat: list) -> bool:
    last_message_by_user = next((message["message"] for message in reversed(chat) if message["sender"] not in {"agent", "system"}), "")
    last_message_by_system = next((message["message"] for message in reversed(chat) if message["sender"] == "system"), "")
    problem_layout = f"""
    [CHAT]: '{chat}'
    [LAST_MESSAGE_USER]: '{last_message_by_user}'
    [SYSTEM_RESPONSE]: '{last_message_by_system}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_input}"),
        ("human", "{human_input}"),
    ])

    chain = prompt | llm

    llm_output = chain.invoke(
        {"system_input": instructions_should_speak, "human_input": problem_layout}
    ).content
    preprocessed = unidecode(llm_output).strip()

    if re.search(".*True|true.*", preprocessed):
        print(f"AGENT MUST SPEAK WITH USER")
        return True
    else:
        print(f"AGENT MUST SOLVE THE MWP")
        return False


""" When a conversational message is sent to the system, the agent should respond as a student, instead of aiming to
resolve the problem on its own """
def get_llm_conversational_response(llm: ChatOllama, problem: Problem):
    last_collaborative_message_by_user = next((message["message"] for message in reversed(problem.chat) if message["sender"] not in {"agent", "system"}), "")
    problem_layout = f"""
    Current status of mathematical problem:
    [PROBLEM STATEMENT]: '{problem.text}'
    [VARIABLES]: '{", ".join(problem.notebook)}'
    [EQUATIONS]: '{", ".join(problem.equations)}'
    [CONVERSATION]: '{problem.chat}'
    [LAST MESSAGE SENT BY YOUR PARTNER]: '{last_collaborative_message_by_user}'
    """
    print(f"[LAST MESSAGE]: '{problem.chat[-1]["message"]}")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_input}"),
        ("human", "{human_input}"),
    ])

    chain = prompt | llm

    llm_output = chain.invoke(
        {"system_input": instructions_conversational, "human_input": problem_layout}
    ).content

    return llm_output.split("KID:", 1)[1]

""" The LLM may hallucinate sometimes and/or get stuck, sending the same message over and over.
The aim of this function is to provide the LLM with the message which is going to be sent, substituting the 
variables with the full description, in order for the LLM to better understand what is going to be sent 
(i. e. for message 'x = 7' where x represents Abigail's age, the `response` param would be "Abigail's age = 7" """
def is_response_reasonable(llm, problem: Problem, proposed_response: str):
    problem_layout = f"""
    Current status of mathematical problem:
    [PROBLEM STATEMENT]: '{problem.text}'
    [VARIABLES]: '{", ".join(problem.notebook)}'
    [EQUATIONS]: '{", ".join(problem.equations)}'
    [PROPOSED STEP TO ADVANCE THE RESOLUTION OF THE PROBLEM]: '{proposed_response}'
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_input}"),
        ("human", "{human_input}"),
    ])
    if debug: print(f"\n\n{problem_layout}\n\n")

    chain = prompt | llm

    llm_output = chain.invoke(
        {"system_input": instructions_review, "human_input": problem_layout}
    ).content

    preprocessed = unidecode(llm_output).strip()
    # print(f"VEREDICT: {preprocessed}")
    if re.search(".*True|true.*", preprocessed):
        print(f"REVIEW CONSIDERS IT AN ACCEPTABLE ANSWER")
        return (True, "")
    else:
        print(f"REVIEW CONSIDERS IT AN UNACCEPTABLE ANSWER. REWRITE")
        match = re.search(r'(?P<DESCR>Hint:.*)', preprocessed, re.DOTALL)
        hint = match.group('DESCR') if match else ""
        print(f"hint: {hint}" )
        return (False, hint)

def get_llm_equations(llm, problem: Problem, previous_response: str, previous_response_review: str) -> list:
    if problem.last_suggestion is None or problem.last_suggestion == '' or problem.last_suggestion == ' ':
        problem.last_suggestion = problem.chat[-1]["message"]
        
    problem_layout = f"""
    [PROBLEM STATEMENT]: '{problem.text}'
    [VARIABLES]: '{", ".join(problem.notebook)}'
    [EQUATIONS]: '{", ".join(problem.equations)}'
    """
    # if (previous_response != "" and previous_response_review != ""):
    #     problem_layout = problem_layout + f"""This was your previous response: '{previous_response}'
    # This is the review to your previous response. Take this review into account when sending next message: '{previous_response_review}'
    # System suggestion to your previous response: Take this review into account when sending next message: '{problem.last_suggestion}'
    # """
        # problem_layout = problem_layout + f"""[HINT]: {previous_response_review}'"""
    print(" ----------- getting LLM RESPONSE -----------")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_input}"),
        ("human", "{human_input}"),
    ])
    if debug: print(f"\n\n{problem_layout}\n\n")

    chain = prompt | llm

    llm_output = chain.invoke(
        {"system_input": instructions_equations, "human_input": problem_layout}
    ).content

    if debug: print(f"\n\nRAW:\n{llm_output}\n\n")
    preprocessed = unidecode(llm_output).strip()
    preprocessed = preprocessed.replace(":", ":\n")
    preprocessed = preprocessed.replace("\\", "")
    output_lines = preprocessed.splitlines()
    # print(f"output_lines splitlines: {output_lines}")
    global already_defined_vars
    already_defined_vars = get_already_defined_variables(problem.notebook)

    output_lines = [l for l in output_lines if l != "" and not "```" in l]
    output_lines = list(map(remove_formatting, output_lines))

    equations = list(filter(is_equation, output_lines))
    
    explanation = list(filter(lambda l: not is_equation(l), output_lines))

    [equations, explanation] = substitute_multicharacter_variables(equations, explanation)
    print(f"equations substitute_multicharacter_variables: {equations}")


    equations = list(map(remove_parenthesis, equations))
    equations = list(map(lambda l: re.sub(r"^\*\s*", "", l), equations))
    equations = list(map(lambda l: re.sub(r"^-\s*", "", l), equations))
    equations = list(map(lambda l: re.sub(r"\*$", "", l), equations))
    equations = list(map(lambda l: l.replace("'", ""), equations))
    print(f"equations remove_parenthesis: {equations}")


    equations = list(filter(lambda e: e != "", equations))
    print(f"equations equations: {equations}")
    
    aux = []
    for e in equations:
        aux+=e.split(",")
    equations = aux
    equations = add_multiplication_sign(equations)
    print(f"equations final: {equations}")
    print(" ----------- LLM EQUATIONS -----------")
    return equations

def get_llm_definitions(llm, problem: Problem, previous_response: str, previous_response_review: str) -> list[str]:
    if problem.last_suggestion is None or problem.last_suggestion == '' or problem.last_suggestion == ' ':
        problem.last_suggestion = problem.chat[-1]["message"]
        
    problem_layout = f"""
    [PROBLEM STATEMENT]: '{problem.text}'
    [VARIABLES]: '{", ".join(problem.notebook)}'
    [EQUATIONS]: '{", ".join(problem.equations)}'
    """
    # if (previous_response != "" and previous_response_review != ""):
    #     problem_layout = problem_layout + f"""This was your previous response: '{previous_response}'
    # This is the review to your previous response. Take this review into account when sending next message: '{previous_response_review}'
    # System suggestion to your previous response: Take this review into account when sending next message: '{problem.last_suggestion}'
    # """
        # problem_layout = problem_layout + f"""[HINT]: {previous_response_review}'"""
    print(" ----------- getting LLM RESPONSE -----------")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_input}"),
        ("human", "{human_input}"),
    ])
    if debug: print(f"\n\n{problem_layout}\n\n")

    chain = prompt | llm

    llm_output = chain.invoke(
        {"system_input": instructions_definitions, "human_input": problem_layout}
    ).content

    if debug: print(f"\n\nRAW:\n{llm_output}\n\n")
    preprocessed = unidecode(llm_output).strip()
    preprocessed = preprocessed.replace(":", ":\n")
    preprocessed = preprocessed.replace("\\", "")
    output_lines = preprocessed.splitlines()
    # print(f"output_lines splitlines: {output_lines}")
    global already_defined_vars
    already_defined_vars = get_already_defined_variables(problem.notebook)

    output_lines = [l for l in output_lines if l != "" and not "```" in l]
    output_lines = list(map(remove_formatting, output_lines))

    explanation = list(filter(lambda l: not is_equation(l), output_lines))
    equations = list(filter(is_equation, output_lines))

    [equations, explanation] = substitute_multicharacter_variables(equations, explanation)
    explanation = list(map(clean_let, explanation))
    explanation = list(map(clean_lets_define, explanation))
    explanation = list(map(clean_where, explanation))

    explanation = "\n".join(explanation).splitlines()
    explanation = list(filter(lambda e: ":" not in e, explanation))
    explanation = clean_redundant(explanation)
    explanation = list(filter(lambda e: re.search(r"^[a-z] .s", e), explanation))

    explanation = list(filter(lambda e: e != "", explanation))
    explanation = list(map(lambda e: e.replace("_", " ".lower()), explanation))
    explanation = list(map(lambda e: e.replace("'", "".lower().strip()), explanation))
    usable_vars = [v for v in list(string.ascii_lowercase) if v not in already_defined_vars]
    explanation = list(map(lambda e: e if e[0] not in already_defined_vars else usable_vars.pop()+e[1:], explanation))
    
    print(" ----------- LLM VARIABLES -----------")
    return explanation
    
