import re
import string
import random

def last_message_is_clarification(problem):
    return problem.chat[-1]["message"].startswith("Querías referirte a:")

def get_message_for_clarification(problem):
    print("HANDLING CLARIFICATION")
    last_message = problem.chat[-1]['message'].replace("<br>", "\n").splitlines()
    suggestions = list(filter(lambda l: re.match(r"\d+ -> ", l), last_message))
    suggestions = [(e.split(" -> ",1)[0].strip(), e.split(" -> ",1)[1].strip()) for e in suggestions]
    notebook = [(e.split(" es ",1)[0].strip(), e.split(" es ",1)[1].strip()) for e in problem.notebook]
    notebook_vars = [b[1].strip() for b in notebook]
    usable_suggestions = [e for e in suggestions if e[1] not in notebook_vars]
    ret = usable_suggestions[0][0]
    if ret == "0": ret = "1"
    return ret

def last_message_is_suggestion(problem):
    #print("CHECKING SUG")
    last_message = problem.chat[-1]["message"]
    return re.search("Puedes.+definir|¿te refieres a |Te sugiero definir una letra para denotar la cantidad", last_message)

def get_message_for_suggestion(problem):
    print("HANDLING SUGGESTION")
    last_message = problem.chat[-1]["message"]
    last_message = " ".join([line for line in last_message.split("\n") if line.strip()])
    if match := re.search("Puedes intentar definir la ecuación.+?(?P<sug>.+=.+)", last_message):
        print("HANDLING FIRST SUGGESTION")
        return match.group("sug") if match else "FAIL IN HANDLING FIRST SUGGESTION"
    elif match := re.search("Puedes definir (?P<var>.+) como (?P<val>.+)", last_message):
        print("HANDLING SECOND SUGGESTION")
        #return f"{match.group('var')} es {match.group('val')}" if match else "FAIL IN HANDLING SECOND SUGGESTION"
        return match.group('val') if match else "FAIL IN HANDLING SECOND SUGGESTION"
    elif match := re.search("Puedes intentar definir (?P<var>.+) en función de", last_message):
        print("HANDLING THIRD SUGGESTION")
        usable_vars = [v for v in list(string.ascii_lowercase) if v not in [e[0] for e in problem.notebook]]
        random.shuffle(usable_vars)
        return f"{usable_vars.pop()} es {match.group('var')}" if match else "FAIL IN HANDLING THIRD SUGGESTION"
    elif match := re.search("¿te refieres a .*¿quieres que denotemos.*", last_message, flags=re.DOTALL):
        print("HANDLING FOURTH SUGGESTION")
        return "Si"
    elif match := re.search("Te sugiero definir una letra para denotar la cantidad (?P<var>.+)", last_message):
        print("HANDLING FIFTH SUGGESTION")
        usable_vars = [v for v in list(string.ascii_lowercase) if v not in [e[0] for e in problem.notebook]]
        random.shuffle(usable_vars)
        return f"{usable_vars.pop()} es {match.group('var')}" if match else "FAIL IN HANDLING FIFTH SUGGESTION"
    else:
        print("HANDLING ELSE SUGGESTION")
        return "<CALL LLM>"