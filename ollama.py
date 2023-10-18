from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser


llm = ChatOllama(
    # model="llama2:13b-chat",
    # model="mistral-openorca",
    model="llama2:7b-chat",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    temperature=0,
)


class VarsExtractor(BaseOutputParser):
    def parse(self, text: str):
        lines = text.split("\n")
        vars = [line.strip("*").strip() for line in lines if line.startswith("*")]
        return vars


get_known_vars_instructions = "Eres un asistente diseñado para extraer y enumerar las variables conocidas del problema proporcionado. No resuelva el problema, no agregue explicaciones o listas adicionales, no realice ningún cálculo y no proporcione ningún otro comentario. MUESTRA SÓLO LAS VARIABLES CONOCIDAS."
get_known_vars_instructions = "Eres un asistente diseñado para extraer y enumerar las variables conocidas del problema proporcionado. No resuelva el problema, no agregue explicaciones o listas adicionales, no realice ningún cálculo y no proporcione ningún otro comentario. MUESTRA SÓLO LAS VARIABLES CONOCIDAS. Si el problema fuera 'Pedro y Juan han decidido vender limonadas en un día caluroso. Pedro vendió algunas limonadas a 2 euros cada una y Juan vendió las suyas a 3 euros cada una. Al final del día, Pedro y Juan habían vendido un total de 45 limonadas y habían recaudado 120 euros juntos. ¿Cuántas limonadas vendió cada uno?' deberías mostrar lo siguiente el formato '* Precio de limonadas de Pedro = 2\n* Precio de limonadas de Juan = 2'"

get_unknown_vars_instructions = "Eres un asistente diseñado para extraer y enumerar las variables desconocidas del problema proporcionado. No resuelva el problema, no agregue explicaciones o listas adicionales, no realice ningún cálculo y no proporcione ningún otro comentario. MUESTRE SÓLO LAS VARIABLES DESCONOCIDAS SIN USAR NINGUNA INCÓGNITA."

problem2 = "Pedro y Juan han decidido vender limonadas en un día caluroso. Pedro vendió algunas limonadas a 2 euros cada una y Juan vendió las suyas a 3 euros cada una. Al final del día, Pedro y Juan habían vendido un total de 45 limonadas y habían recaudado 120 euros juntos. ¿Cuántas limonadas vendió cada uno?"
problem3 = "Lucía y Marta decidieron empezar un pequeño negocio vendiendo pulseras y collares durante el verano. El precio de cada pulsera es de 4 euros y el de cada collar es de 6 euros. En un día particular, vendieron un total de 25 ítems y recaudaron 110 euros. ¿Cuántas pulseras y cuántos collares vendieron?"
problem4 = "En una tienda de mascotas, venden tres tipos diferentes de comida para animales: para perros, gatos y pájaros. Un día, se vendieron un total de 150 unidades entre las tres variedades. La comida para perros cuesta 3 euros la unidad, la comida para gatos cuesta 5 euros la unidad y la comida para pájaros cuesta 2 euros la unidad. Ese día, se recaudaron 500 euros en total. Si se sabe que se vendieron el mismo número de unidades de comida para perros y para gatos, ¿cuántas unidades de cada tipo de comida se vendieron?"
problem1 = "Un grupo de estudiantes financia su viaje de fin de curso con la venta de participaciones de lotería, por importe de 1, 2 y 5 euros. Han recaudado, en total, 600 euros y han vendido el doble de participaciones de 1 euro que de 5 euros. Si han vendido un total de 260 participaciones, calcula el número de participaciones que han vendido de cada importe."
problem = problem4


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "{instructions}"),
        ("human", "HOLA QUE TAL"),
        ("human", "{input}"),
    ]
)

# chain = prompt | llm | VarsExtractor()
chain = prompt | llm

# OpenAI can use abatch instead
known_vars, unknown_vars = chain.batch(
    [
        {"instructions": get_known_vars_instructions, "input": problem},
        {"instructions": get_unknown_vars_instructions, "input": problem},
    ]
)

print("KNOWN:")
print(known_vars)
print("\nUNKNOWN:")
print(unknown_vars)
