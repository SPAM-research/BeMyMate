import re
import sympy as sp
""" Validate definitions. The validations / sanitizations are presented as follow:
- Descriptions must no be on the notebook already 
- Definitions must coincide with the pattern of like-expressions 'x is Abigail's age' """
def definitions_validator(definitions: list[str], outputs: list[str], notebook: list[str]) -> list[str]:
    # regex for expressions like 'x is Abigail age'
    pattern = re.compile(r"^[a-zA-Z] is [a-zA-Z\s]+$")
    notebook_descriptions = [item.split(' es ', 1)[1] for item in notebook]
    new_definitions = [d.lower() for d in definitions if d[2:].lower() not in outputs]
    new_filtered_definitions = [definition for definition in new_definitions if pattern.match(definition) and definition.split(' is ', 1)[1].upper() not in notebook_descriptions]
    return new_filtered_definitions

""" Validate equations. The validations / sanitizations are presented as follow:
- Equations must no be on the notebook already
- Equations must be valid mathematical equations
- Equations must use letters already present on the notebook """
def equations_validator (equations: list[str], outputs: list[str], notebook: list[str], notebook_equations: list[str]) -> list:
    new_equations = [e for e in equations if e not in outputs]
    notebook_letters = [item.split(' es ', 1)[0] for item in notebook]
    new_filtered_equations = []
    for equation in new_equations:
        letters_in_equation = set(re.findall(r'[a-zA-Z]', equation))
        if letters_in_equation.issubset(notebook_letters) and equation not in notebook_equations and '?' not in equation:
            new_filtered_equations.append(equation)
    
    valid_equations = []
    
    for equation in new_filtered_equations:
        try:
            if '=' in equation: # if an = is present, analyze each side as its own equation
                lhs, rhs = equation.split('=')
                sp.sympify(lhs.strip())
                sp.sympify(rhs.strip())
            else:
                sp.sympify(equation)
            valid_equations.append(equation)
        except (sp.SympifyError, SyntaxError):
            # Mathematical expression not valid
            pass
    
    return valid_equations