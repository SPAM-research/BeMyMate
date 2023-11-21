from utils import test_problem
from problems import problems
import os
#os.system("clear")


note_format = "variable is definition"
equation_format = "'y = mathematical expression'"
# required_format = equation_format
required_format = note_format



# These seem to work with mistral-instruct
i2_1 = f"Given a problem, variable and equations, define a variable {note_format} that hasn't been defined. Do not solve the problem. Your output must only be a variable definition {note_format}. You must output something that isn't in the input."
i2_2 = f"Given a problem and some variables define a variable that hasn't been defined using the format {note_format}. Do not solve the problem. Output only the variable definition {note_format}."


i1_1 = f"Given a problem, variable and equations, define a variable {note_format} that hasn't been defined. Do not solve the problem. Your output must only be a variable definition {note_format}."
i1_2 = f"Given a problem, your task is to pose an equation with the format {required_format} that can further the resolution of the problem. Your output must only be a equation with the format {required_format}."
i1_3 = f"Given a problem, your task is to pose a variable definition with the format {required_format} that can further the resolution of the problem. Your output must only be a variable definition with the format {required_format}."
i1_4 = f"Given a problem and variable definitions, define a variable like {required_format} that hasn't been defined."
i1_5 = f"Given a problem and variable definitions, define one of the unknown variables of the problem with the following format '{required_format}'."




instructions = i1_1


instructions2 = ""#i2_1
instructions2 = i2_1
instructions2 = i2_1





prob_sep = "========================================"
sec_sep =  "--------------------"
head_sep = "####################"
up_sep = "vvvvvvvvvvvvvvvvvvvv"
down_sep = "^^^^^^^^^^^^^^^^^^^^"
all_outputs = []
i = 1
empty = 0

ttf = 56
problem_set = problems[ttf-1:ttf]
problem_set = problems[:]
total = len(problem_set)

for problem in problem_set:
    print(f"{i}/{total}")
    [original, output] = test_problem(problem, instructions)
    if output == "":
        if instructions2 != "":
            [original, output2] = test_problem(problem, instructions2)
            if output2 == "":
                empty += 1
            else:
                all_outputs.append(f"{i}\nT: {problem[0]}\nN: {problem[1]}\n{sec_sep}\n{original}\n{up_sep}\n{output2}\n{down_sep}\n\n")
        else:
            empty += 1
    else:
        all_outputs.append(f"{i}\nT: {problem[0]}\nN: {problem[1]}\n{sec_sep}\n{original}\n{up_sep}\n{output}\n{down_sep}\n\n")
    i += 1
    #os.system("clear")

empty_string = f"NOT VALID: {empty}/{total} ({round(empty/total*100, 2)}%)"
all_outputs_string = f"\n{prob_sep}\n".join(all_outputs)
final_string = f"INSTRUCTIONS1: \"{instructions}\"\nINSTRUCTIONS2: \"{instructions2}\"\n{head_sep}\n{empty_string}\n{head_sep}\n{all_outputs_string}"
print(final_string)
open("results/results.txt", "w").write(final_string)

