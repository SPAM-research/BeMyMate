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

from utils.llm_responder import get_llm_response

class LlmHandler:
    def __init__(self, problem):
        # Maybe make a small inference to load the model ?
        #self.ollama_process = subprocess.Popen(["./ollama", "serve"])
        self.problem = problem
        self.outputs = []
        self.definitions = []
        self.equations = []
        self.llm = ChatOllama(
            model="llama3:latest",
            #model="stable-beluga:13b-fp16",
            #model="mixtral:8x7b-instruct-v0.1-q3_K_L",
            #callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature=0,
        )

    def call(self):
        [equations, definitions] = get_llm_response(self.llm, self.problem)

        # Random do get equation, definition or message
        new_definitions = [d.lower() for d in definitions if d[2:].lower() not in self.outputs]
        new_equations = [e for e in equations if e not in self.outputs]

        print("New definitions: ", new_definitions)
        if new_definitions:

            selected = random.choice(new_definitions)
            print("argostranslate: ",  argostranslate.translate.translate("Hello world", "en", "es"))
            response = argostranslate.translate.translate(selected, "en", "es")
            self.outputs.append(selected[2:].lower())
        elif new_equations:
            response = random.choice(new_equations)
            self.outputs.append(response)
        else: 
            response = "Necesito ayuda"

        return response
