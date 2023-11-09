from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser

"""
    Do as told:
        mistral:7b-instruct-fp16
    Translators:
        llama2:13b-chat
"""

model_to_use = "llama2:13b-chat"
model_to_use = "vicuna:33b-q4_K_M"
model_to_use = "orca-mini:13b-q6_K"
model_to_use = "mistral-openorca:7b-fp16"
model_to_use = "mistral:7b-instruct-fp16" #model_to_use = "mistral:7b-instruct"
#model_to_use = "nous-hermes:7b-llama2-fp16"
#model_to_use = "nous-hermes:13b-llama2-q8_0"


llm = ChatOllama(
    model=model_to_use,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    temperature=0.01,
)


enunciado = "Abigail tiene cuatro años más que Jonathan. Hace seis años ella tenía el doble de años que él. ¿Cuántos años tiene ahora Abigail?"
enunciado = "Un terreno con forma de cuadrado tiene un lado de 5 metro. ¿Cuál es el área del terreno?"
enunciado = "En un club de tenis tienen dos carros con 105 y 287 pelotas, respectivamente. Las van a poner en botes de 7 pelotas para utilizarlas en un torneo. ¿Cuántos botes serán necesarios?"
enunciado = "Disponemos de dos contenedores con 396 y 117 kg de patatas, respectivamente. Para su venta, deben envasarse en bolsas que contengan 9 kg. ¿Cuántas bolsas serán necesarias?"
notebook = ""
equations = ""

#equation_format =  "'y = <MATHEMATICAL EXPRESSION>'"
note_format = "'y is NUMBER OF ORANGES'"
#required_format = equation_format
required_format = note_format

# This seems to work with mistral-instruct
instructions = f"Given a problem, your task is to pose an equation with the format {required_format} that can further the resolution of the problem. Your output should only be a equation with the format {required_format}."
instructions = f"Given a problem, your task is to pose an equation with the format {required_format} that can further the resolution of the problem. Your output must only be a equation with the format {required_format}."

problem = f"""
The problem: {enunciado}
"""

#instructions = f"Your task is to translate English into Spanish. Your output must be in Spanish."
#instructions = f"Given a sentence, your task is to translate it into Spanish. Your output must be in Spanish."
#problem = "It's very hot."

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "{system_input}"),
        ("human", "{human_input}"),
    ]
)

chain = prompt | llm

output = chain.invoke({"system_input": instructions, "human_input": problem}).content
# print(output)
print()