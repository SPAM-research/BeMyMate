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

import argostranslate.translate

from llm_responder import get_llm_response

class LlmHandler:
    def __init__(self, problem):
        # Maybe make a small inference to load the model ?
        #self.ollama_process = subprocess.Popen(["./ollama", "serve"])
        self.problem = problem
        self.outputs = []
        self.definitions = []
        self.equations = []
        self.llm = ChatOllama(
            model="mistral:7b-instruct-fp16",
            #model="stable-beluga:13b-fp16",
            #model="mixtral:8x7b-instruct-v0.1-q3_K_L",
            #callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature=0,
        )

    def call(self):
#        print("CALLING LLM")
#
#        if not self.definitions and not self.equations:
#            [equations, definitions] = get_llm_response(self.llm, self.problem)
#            new_definitions = [d.lower() for d in definitions if d[2:].lower() not in self.outputs]
#            new_equations = [e for e in equations if e not in self.outputs]
#            self.definitions+=new_definitions
#            self.equations+=new_equations
#
#        if self.definitions:
#            selected = self.definitions.pop(0)
#            response = argostranslate.translate.translate(selected, "en", "es")
#            self.outputs.append(selected[2:].lower())
#        elif self.equations:
#            response = self.equations.pop(0)
#            self.outputs.append(response)
#        else:
#            response = "Necesito ayuda"
#        
#        return response
        print("CALLING LLM")
        [equations, definitions] = get_llm_response(self.llm, self.problem)
        #print(f"DEFS: {definitions}")
        #print(f"EQS: {equations}")

        # Random do get equation, definition or message
        new_definitions = [d.lower() for d in definitions if d[2:].lower() not in self.outputs]
        new_equations = [e for e in equations if e not in self.outputs]
        #print(f"NEW DEFS: {new_definitions}")
        #print(f"NEW EQS: {new_equations}")

        if new_definitions:
            selected = random.choice(new_definitions)
            response = argostranslate.translate.translate(selected, "en", "es")
            self.outputs.append(selected[2:].lower())
            #print(f"NEW DEFS: {new_definitions}")
            #print(f"OUTPUTS: {self.outputs}")
        elif new_equations:
            response = random.choice(new_equations)
            self.outputs.append(response)
        else: 
            response = "Necesito ayuda"

        return response
