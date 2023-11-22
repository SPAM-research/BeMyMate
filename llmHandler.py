import re
import subprocess
import time
import os
import signal

from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser

from problem import Problem
from variable_definition import get_variable_definition


default_model = "llama2:7b-chat"
default_model = "mistral-openorca"
default_model = "llama2:13b-chat"
default_model = "mistral:7b-instruct-fp16"

#note_format = "variable is definition"
#get_variable_definition_instructions = [
#    f"Given a problem, variable and equations, define a variable {note_format} that hasn't been defined. Do not solve the problem. Your output must only be a variable definition {note_format}.",
#    f"Given a problem, variable and equations, define a variable {note_format} that hasn't been defined. Do not solve the problem. Your output must only be a variable definition {note_format}. You must output something that isn't in the input.",
#    f"Given a problem and some variables define a variable that hasn't been defined using the format {note_format}. Do not solve the problem. Output only the variable definition {note_format}.",
#    f"Define a variable that hasn't been defined using the format {note_format}. Do not solve the problem. Output only the variable definition {note_format}.",
#    f"Define a variable that hasn't been defined using the format {note_format} without solving the problem.",
#    f"Your task is to define a variable with the format '{note_format}' without solving the problem.",
#    f"Define a variable with the format '{note_format}' without solving the problem.",
#]

class LlmHandler:
    def __init__(self, problem):
        # Maybe make a small inference to load the model ?
        #self.ollama_process = subprocess.Popen(["./ollama", "serve"])
        self.problem = problem
        self.llm = ChatOllama(
            model=default_model,
            #callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature=0,
        )

    def call(self):
        # Random do get_variable, get_equation or get message
        #response = self.get_variable_definition()
        response = get_variable_definition(self.llm, self.problem)
        return response


    #def process_unknown_quantities(self, quantities):
    #    unknown_quantities = []
    #    for q in quantities:
    #        name = q["name"]
    #        description = re.search(r"text=(.*?), language", q["description"]).group(1)
    #        unknown_quantities.append({"name": name, "description": description})
    #    return unknown_quantities

    #def process_known_quantities(self, quantities):
    #    known_quantities = []
    #    for q in quantities:
    #        name = q["name"]
    #        description = re.search(r"text=(.*?), language", q["description"]).group(1)
    #        value = q["value"]
    #        known_quantities.append(
    #            {"name": name, "description": description, "value": value}
    #        )
    #    return known_quantities

    #def process_graphs(self, graphs):
    #    graph_list = []
    #    for g in graphs:
    #        path_list = []
    #        for p in g["paths"]:
    #            match p["type"]:
    #                case "Addition":
    #                    op = "' + '"
    #                case "Subtraction":
    #                    op = "' - '"
    #                case "Multiplication":
    #                    op = "' * '"
    #                case "Division":
    #                    op = "' / '"
    #            path = f"'{p['result']}' = '{op.join(p['nodes'])}'"
    #            path_list.append(path)
    #        graph_list.append(path_list)
    #    return graph_list