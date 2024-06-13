import re


""" This function determines if the last chat message provides options to discern
the type of message. If the last chat message starts 
with a prompt suggesting choices, it is considered as such.
i.e. Messages where Hints provides responses such as 'Did you mean:
1 -> CURRENT AGE OF JONATHAN
2 -> PAST AGE OF JONATHAN
0 -> None of the above'"""
def is_message_a_choice(problem):
    return problem.chat[-1]["message"].startswith("Querías referirte a:")

def is_last_message_a_suggestion(problem):
    #print("CHECKING SUG")
    last_message = problem.chat[-1]["message"]
    return re.search("Puedes.+definir|¿te refieres a |Te sugiero definir una letra para denotar la cantidad", last_message)
