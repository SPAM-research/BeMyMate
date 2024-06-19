import re
import subprocess
import time
import os
import signal
import random

from langchain_community.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
import ast
import argostranslate.translate
import sympy as sp
from utils.llm_responder import get_llm_definitions, get_llm_equations, is_response_reasonable
from models.problem import Problem
import utils.response_analyzer as response_analyzer

class LlmHandler:
    def __init__(self, problem: Problem):
        # Maybe make a small inference to load the model ?
        #self.ollama_process = subprocess.Popen(["./ollama", "serve"])
        self.problem = problem

        self.outputs = []
        self.definitions = []
        self.equations = []
        self.is_response_reasonable = True
        self.previous_response_review = ""
        self.llm = ChatOllama(
            model="llama3:latest",
            # model="stable-beluga:13b-fp16",
            #model="mixtral:8x7b-instruct-v0.1-q3_K_L",
            #callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature=0.6,
        )

    def call(self):
        should_response_resolve = should_response_resolve(self.problem)
        response = ""
        definitions = get_llm_definitions(self.llm, self.problem, response, self.previous_response_review)
        filtered_definitions = response_analyzer.definitions_validator(definitions, self.outputs, self.problem.notebook)

        print("filtered_definitions: ", filtered_definitions)

        if filtered_definitions:
            response = random.choice(filtered_definitions)
            self.outputs.append(response[2:].lower())
        elif len(self.problem.notebook) >= 1 and response == "": # If no new definitions are proposed, generate an equation
            equations = get_llm_equations(self.llm, self.problem, response, self.previous_response_review)
            filtered_equations = response_analyzer.equations_validator(equations, self.outputs, self.problem.notebook, self.problem.equations)
            if filtered_equations:
                response = random.choice(filtered_equations)
                self.outputs.append(response)
        
        if response == "": 
            response = "I need help"

        # TODO: hacer dos funciones is_definition_reasonable y is_equation_reasonable para comprobar la definición de variable o ecuación
        # if response != "I need help":
        #     (self.is_response_reasonable, self.previous_response_review)  = is_response_reasonable(self.llm, self.problem, response)


        return response
