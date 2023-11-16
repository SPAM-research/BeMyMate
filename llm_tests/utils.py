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
    # callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    temperature=0,
)


def clean_represents(i):
    match = re.search(r"\" represents.*?(?:,|\.|\n|$)", i)
    variable_names = ["x", "y", "z", "u", "v", "w", "a", "b", "c", "d"]
    used_variable_names = ["x", "y", "z", "u", "v", "w", "a", "b", "c"]
    if match:
        var = [v for v in variable_names if v not in used_variable_names][0]
        definition = match.group(0).replace("\" represents", "is", 1).replace(",","").replace("\n","").replace(".","")
        return f"{var} {definition}"
    else:
        return i

def clean_defined_as(i):
    match = re.search(r"\" can be defined as.*?(?:,|\.|\n|$)", i)
    variable_names = ["x", "y", "z", "u", "v", "w", "a", "b", "c", "d"]
    used_variable_names = ["x", "y", "z", "u", "v", "w", "a", "b", "c"]
    if match:
        var = [v for v in variable_names if v not in used_variable_names][0]
        definition = match.group(0).replace("\" can be defined as", "is", 1).replace(",","").replace("\n","").replace(".","")
        return f"{var} {definition}"
    else:
        return i

def clean_let(i):
    match = re.search(r"Let .*? be .*?(?:,|\.|\n|$)", i)
    variable_names = ["x", "y", "z", "u", "v", "w", "a", "b", "c", "d"]
    used_variable_names = ["x", "y", "z", "u", "v", "w", "a", "b", "c"]
    if match:
        var = [v for v in variable_names if v not in used_variable_names][0]
        definition = re.sub(r".*?be ", "is ", match.group(0)).replace(",","").replace("\n","").replace(".","")
        return f"{var} {definition}"
    else:
        return i

def not_input_or_empty_line(l):
    return not re.search(r"^\s*The problem:", l) and not re.search(r"^\s*Variables:", l) and not re.search(r"^\s*Equations:", l) and not l.startswith("```") and not l == ""

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
    
    llm_output = chain.invoke({"system_input": instructions, "human_input": problem}).content
    
    """
        Notes:
            "can be defined as .*? (.|,)" is a recurring string
            ": WANTED_OUTPUT" is a recurring line format
    """
    
    filtered_output_lines_list = list(filter(not_input_or_empty_line, llm_output.splitlines()))
    
    cleaned_represents = list(map(clean_represents, filtered_output_lines_list))
    cleaned_defined_as = list(map(clean_defined_as, cleaned_represents))
    cleaned_let = list(map(clean_defined_as, cleaned_defined_as))
    
    final = cleaned_let
    output = "\n".join(final)
    
    return output