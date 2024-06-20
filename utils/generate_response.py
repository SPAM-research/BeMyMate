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
    pattern = re.compile(r"(?P<DIGIT>\d{1,2}) -> (?P<DESCR>[\w ]+)")
    suggestions = [pattern.search(line) for line in last_message if pattern.search(line)]
    suggestions = [(match.group("DIGIT"), match.group("DESCR")) for match in suggestions]
    notebook = [(e.split(" es ", 1)[0].strip(), e.split(" es ", 1)[1].strip()) for e in problem.notebook]
    notebook_vars = [b[1].strip() for b in notebook]
    usable_suggestions = [e for e in suggestions if e[1] not in notebook_vars]
    ret = usable_suggestions[0][0]
    if ret == "0": ret = "1"    
    return ret


def get_message_for_suggestion(problem):
    last_message = problem.chat[-1]["message"]
    last_message = " ".join([line for line in last_message.split("\n") if line.strip()])
    usable_vars = [v for v in list(string.ascii_lowercase) if v not in [e[0] for e in problem.notebook]]
    notebook_letters = [item.split(' es ', 1)[0] for item in problem.notebook]
    notebook_descriptions = [item.split(' es ', 1)[1] for item in problem.notebook]
    random.shuffle(usable_vars)
    if match := re.search("You can try to define an equation using using .+?(?P<sug>.+=.+)", last_message):
        return match.group("sug") if match else "FAIL IN HANDLING FIRST SUGGESTION"
    elif match := re.search("You may try to define \r<br /> (?P<var>.*)\r<br /> as (?!(?:a function of)) (?P<equation>.*)", last_message):
        description = match.group('var').strip()
        letter_to_description = notebook_letters[notebook_descriptions.index(description.upper())]
        return f"{usable_vars.pop()} is {description}" if description in problem.notebook else f"{letter_to_description} = {match.group('equation').strip()}"
    elif match := re.search("Puedes definir (?P<var>.+) como (?P<val>.+)", last_message):
        return f"{usable_vars.pop()} is {match.group('var').strip()}" if match else "FAIL IN HANDLING SECOND SUGGESTION"
    elif match := re.search("You may try to define \r<br />  (?P<var>.*)\r<br />  as a function of", last_message):
        return f"{usable_vars.pop()} is {match.group('var')}" if match else "FAIL IN HANDLING THIRD SUGGESTION"
    elif match := re.search("You mean .*? do you want us to.*", last_message, flags=re.DOTALL):
        return "Yes"
    elif match := re.search("Te sugiero definir una letra para denotar la cantidad (?P<var>.+)", last_message):
        return f"{usable_vars.pop()} is {match.group('var')}" if match else "FAIL IN HANDLING FIFTH SUGGESTION"
    else:
        return "<CALL LLM>"
