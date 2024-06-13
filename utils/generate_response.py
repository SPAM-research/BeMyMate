import random
import re
import string


def get_definition_block_variable(problem):
    last_message = problem.chat[-1]["message"]
    variable = ""
    if match := re.search(r"Espero una descripción para la letra (?P<var>.)", last_message):
        variable = match.group("var")
    elif match := re.search(r"denotar mediante la letra (?P<var>.)", last_message):
        variable = match.group("var")
    elif match := re.search(r"descripci.n .*para la letra (?P<var>.)", last_message):
        variable = match.group("var")
    elif match := re.search(r"cantidad quieres nombrar mediante la letra (?P<var>.)", last_message):
        variable = match.group("var")
    return variable



def get_message_for_choice(problem):
    last_message = problem.chat[-1]["message"].splitlines()
    suggestions = list(filter(lambda l: re.match(r"\d+ -> ", l), last_message))
    suggestions = [(e.split(" -> ",1)[0].strip(), e.split(" -> ",1)[1].strip()) for e in suggestions]
    notebook = [(e.split(" es ",1)[0].strip(), e.split(" es ",1)[1].strip()) for e in problem.notebook]
    notebook_vars = [b[1].strip() for b in notebook]
    usable_suggestions = [e for e in suggestions if e[1] not in notebook_vars]
    ret = usable_suggestions[0][0]
    if ret == "0": ret = "1"
    return ret


def get_message_for_suggestion(problem):
    last_message = problem.chat[-1]["message"]
    last_message = " ".join([line for line in last_message.split("\n") if line.strip()])
    usable_vars = [v for v in list(string.ascii_lowercase) if v not in [e[0] for e in problem.notebook]]
    random.shuffle(usable_vars)
    if match := re.search("Puedes intentar definir la ecuación.+?(?P<sug>.+=.+)", last_message):
        return match.group("sug") if match else "FAIL IN HANDLING FIRST SUGGESTION"
    elif match := re.search("Puedes definir (?P<var>.+) como (?P<val>.+)", last_message):
        return f"{usable_vars.pop()} es {match.group('var').strip()}" if match else "FAIL IN HANDLING SECOND SUGGESTION"
    elif match := re.search("Puedes intentar definir (?P<var>.+) en función de", last_message):
        return f"{usable_vars.pop()} es {match.group('var')}" if match else "FAIL IN HANDLING THIRD SUGGESTION"
    elif match := re.search("¿te refieres a .*¿quieres que denotemos.*", last_message, flags=re.DOTALL):
        return "Si"
    elif match := re.search("Te sugiero definir una letra para denotar la cantidad (?P<var>.+)", last_message):
        return f"{usable_vars.pop()} es {match.group('var')}" if match else "FAIL IN HANDLING FIFTH SUGGESTION"
    else:
        return "<CALL LLM>"
