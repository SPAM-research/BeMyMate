import re

from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser

from problem import Problem


default_model = "llama2:7b-chat"
default_model = "mistral-openorca"
default_model = "llama2:13b-chat"


class LlmHandler:
    def __init__(self, problem):
        self.problem = problem
        self.llm = ChatOllama(
            model=default_model,
            # callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature=0,
        )

    def process_unknown_quantities(self, quantities):
        unknown_quantities = []
        for q in quantities:
            name = q["name"]
            description = re.search(r"text=(.*?), language", q["description"]).group(1)
            unknown_quantities.append({"name": name, "description": description})
        return unknown_quantities

    def process_known_quantities(self, quantities):
        known_quantities = []
        for q in quantities:
            name = q["name"]
            description = re.search(r"text=(.*?), language", q["description"]).group(1)
            value = q["value"]
            known_quantities.append(
                {"name": name, "description": description, "value": value}
            )
        return known_quantities

    def process_graphs(self, graphs):
        graph_list = []
        for g in graphs:
            path_list = []
            for p in g["paths"]:
                match p["type"]:
                    case "Addition":
                        op = "' + '"
                    case "Subtraction":
                        op = "' - '"
                    case "Multiplication":
                        op = "' * '"
                    case "Division":
                        op = "' / '"
                path = f"'{p['result']}' = '{op.join(p['nodes'])}'"
                path_list.append(path)
            graph_list.append(path_list)
        return graph_list

    def call(self):
        # BIG METHOD
        # Create the llm call
        # Call it
        # Return response
        return "RESPONSE"
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", instr),
                ("human", problem),
            ]
        )
        chain = prompt | llm
        response = chain.invoke([]).content
        return response
