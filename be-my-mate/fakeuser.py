import concurrent.futures
import json
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from models.problem import Problem
from models.user import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from constants import BASE_URL
from utils.llm_handler import LlmHandler
from utils.utils import (
    get_definition_block_variable,
    get_message_for_clarification,
    get_message_for_suggestion,
    last_message_is_clarification,
    last_message_is_suggestion,
)

agents_collection = 15
default_sleep = 3
max_consecutive_helps = 10
max_steps = 100
max_resolutions = 10
debug = False


# problemas100 = [0, 2, 5, 19, 20, 21, 22, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 53, 54, 57, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 82, 83, 84, 85, 87, 88, 98, 100, 101, 102, 108, 109, 110, 111, 112, 113, 114, 119, 120, 121, 124, 126, 128, 129, 130, 131, 132, 133, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 161, 171, 174, 180, 181, 182, 183, 184, 185, 186]

# Last five were problematic
problemas25 = [
    0,
    2,
    5,
    19,
    20,
    21,
    22,
    27,
    28,
    29,
    30,
    31,
    32,
    34,
    39,
    40,
    98,
    30,
    98,
    120,
    40,
    108,
    129,
    174,
    181,
]


class FakeUser:
    def __init__(self, problem_in_wrapper):
        if debug:
            print("INIT")
        self.problem = Problem()
        self.session = requests.Session()
        self.set_problem(problem_in_wrapper)
        self.get_additional_problem_info()
        self.problem_in_wrapper = problem_in_wrapper

    def solve_problem(self):
        if debug:
            print("SOLVE PROBLEM")
        self.llm_handler = LlmHandler(self.problem)
        self.finished = False
        self.consecutive_helps = 0
        self.steps = 0
        self.helps = 0

        self.enter_problem(self.problem_in_wrapper)

        # print("SOLVING NOW")
        while not self.finished:
            self.get_problem_state()
            if not self.finished:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self.get_message)
                    try:
                        result = future.result(timeout=30)
                        self.send_message(result)
                    except concurrent.futures.TimeoutError:
                        quit()
                time.sleep(default_sleep)

            # print("\n")

        self.save_statistics()

    def get_message(self):
        if debug:
            print("GET MESSAGE: ONE")
        if self.problem.chat[-1]["message"].startswith("Muy bien"):
            self.problem.last_suggestion = ""

        if debug:
            print("GET MESSAGE: TWO")
        if last_message_is_clarification(self.problem):
            if debug:
                print("GET MESSAGE: THREE")
            response = get_message_for_clarification(self.problem)
        elif last_message_is_suggestion(self.problem):
            if debug:
                print("GET MESSAGE: FOUR")
            self.problem.last_suggestion += (
                "\n".join(
                    [l for l in self.problem.chat[-1]["message"].splitlines() if l]
                )
                + "\n\n"
            )
            response = get_message_for_suggestion(self.problem)
            if response == "<CALL LLM>":
                response = self.llm_handler.call()
        else:
            if debug:
                print("GET MESSAGE: FIVE")
            response = self.llm_handler.call()
        if debug:
            print(f"\n\nPROC:\n{response}\n\n")
        if debug:
            print("GET MESSAGE: SIX")

        # response = self.ask_for_human_message(response)

        response = response.strip().lower()

        if var := get_definition_block_variable(self.problem):
            if re.search("[a-z] es .*", response) and not re.search("ayuda", response):
                # print("DEFINITION BLOCK")
                response = f"{var}{response[1:]}"
                # print(response)

        if debug:
            print("GET MESSAGE: SEVEN")
        if not re.search(r"^[0-9]+$|^si$", response):
            self.steps += 1
        if re.search(r"ayuda", response):
            self.helps += 1
            self.consecutive_helps += 1
        else:
            self.consecutive_helps = 0

        return response

    def save_statistics(self):
        if debug:
            print("SAVE STATS")
        self.nb = len(self.problem.notebook)
        self.uq = len(self.problem.unknown_quantities)
        self.eq = len(self.problem.equations)
        self.gs = len(self.problem.graphs[0]["paths"])
        if self.nb > self.uq:
            self.uq = self.nb
        if self.eq > self.gs:
            self.gs = self.eq
        if self.consecutive_helps == max_consecutive_helps:
            self.finish_state = "HELP LOOP"
        elif self.steps == max_steps:
            self.finish_state = "MANY STEPS"
        else:
            self.finish_state = "FINISHED"
            self.eq = self.gs

    def ask_for_human_message(self, response):
        print(f"AGENT RESPONSE: {response}")
        if opt := input("DEFAULT? "):
            response = opt
        return response

    def last_message_is_from_tutor(self):
        return self.problem.chat[-1]["sender"] == "system"

    def clean_chat_message(self, message):
        message = message.replace("\r", "")
        message = re.sub(r"</?br/?>", "\n", message)
        message = re.sub(r"&gt;", ">", message)
        return message

    def reset_current_problem(self):
        if debug:
            print("RESET PROBLEM")
        try:
            driver.find_element(
                By.XPATH, "//button[contains(text(), 'Entendido')]"
            ).click()
        except:
            ...
        time.sleep(1)
        try:
            driver.find_element(
                By.XPATH, "//button[contains(text(), 'Reiniciar')]"
            ).click()
        except:
            ...
        time.sleep(1)
        try:
            driver.find_element(By.CSS_SELECTOR, ".accept").click()
        except:
            ...

    def go_to_problem(self):
        if debug:
            print("GOTO PROBLEM")
        while True:
            try:
                driver.find_element(
                    By.CSS_SELECTOR,
                    ".message_input_collection.message_input.form-control",
                )
            except:
                driver.get(f"${BASE_URL}/collections")
                time.sleep(default_sleep)
                while True:
                    while True:
                        try:
                            driver.find_element(By.ID, "pagination-next-page")
                        except:
                            time.sleep(1)
                        else:
                            break
                    try:
                        collection = driver.find_element(
                            By.ID, f"row-{str(agents_collection)}"
                        )
                    except:
                        driver.find_element(By.ID, "pagination-next-page").click()
                        time.sleep(1)
                    else:
                        break
                collection.click()
                time.sleep(10)
            else:
                break

    def set_problem(self, problem_index):
        if debug:
            print("SET PROBLEM")
        collection_dict = json.loads(open("collection_all_problems.json", "r").read())
        all_problems = collection_dict["problems"]
        number_of_problems = len(all_problems)
        # if problem_index >= number_of_problems: problem_index = number_of_problems
        collection_dict["problems"] = [all_problems[problem_index]]
        self.login_backend()
        while True:
            if (
                self.session.put(
                    f"${BASE_URL}/api/wrapper/{str(agents_collection)}",
                    json=json.loads(json.dumps(collection_dict)),
                ).status_code
                == 200
            ):
                break

    def enter_problem(self, problem_index):
        if debug:
            print("ENTER PROBLEM")
        self.go_to_problem()
        time.sleep(default_sleep)
        self.reset_current_problem()
        time.sleep(default_sleep)
        self.go_to_problem()
        # while True:
        #    try: driver.find_element(By.CSS_SELECTOR, ".message_input_collection.message_input.form-control")
        #    except:
        #        driver.get(f"https://betatutorchat.uv.es/collections/{str(agents_collection)}/problem/{problem_id}")
        #        time.sleep(5)
        #    else: break

    def send_message(self, message):
        if debug:
            print("SEND MESSAGE")
        self.go_to_problem()
        chat_input = driver.find_element(
            By.CSS_SELECTOR, ".message_input_collection.message_input.form-control"
        )
        time.sleep(2)
        chat_input.clear()
        time.sleep(2)
        chat_input.send_keys(message)
        time.sleep(2)
        chat_input.send_keys(Keys.ENTER)
        time.sleep(2)

    def check_if_finished(self):
        if debug:
            print("CHECK FINISHED")
        try:
            driver.find_element(
                By.XPATH,
                "//button[contains(text(), '¡Felicidades! Has resuelto el problema (Presiona para continuar)')]",
            )
            self.finished = True
        except:
            if (
                self.consecutive_helps == max_consecutive_helps
                or self.steps == max_steps
            ):
                self.finished = True

    def get_problem_state(self):
        if debug:
            print("GET PROBLEM STATE")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        self.check_if_finished()
        self.problem.text = soup.find("p", class_="card-text").text
        self.problem.notebook = [
            note.text
            for note in soup.find_all("div", id="Notebook")[0].find_all("div")
            if not note.input
        ]
        self.problem.equations = [
            note.text
            for note in soup.find_all("div", id="Notebook")[1].find_all("div")
            if not note.input
        ]
        boxes = soup.find("ul", id="chatMessages").find_all("div", class_="box")
        self.problem.chat = [
            {
                "sender": ("system" if "left" in box.li["class"] else "user"),
                "message": self.clean_chat_message(
                    box.find("div", class_="text").decode_contents()
                ),
            }
            for box in boxes
        ]

    def login_backend(self):
        if debug:
            print("LOGIN BACKEND")
        while True:
            if (
                self.session.post(
                    f"{BASE_URL}/api/login",
                    json={
                        "username": os.getenv("AGENT_USERNAME"),
                        "password": os.getenv("AGENT_PASSWORD"),
                        "timeZone": "Europe/Madrid",
                        "lastConnection": 0,
                    },
                ).status_code
                == 200
            ):
                break

    def get_additional_problem_info(self):
        if debug:
            print("GET ADD PROB INFO")
        self.login_backend()

        while True:
            wrapper_response = self.session.get(
                f"{BASE_URL}/api/wrapper/{str(agents_collection)}/problems"
            )
            if wrapper_response.status_code == 200:
                break

        problem_id = json.loads(wrapper_response.text)["wrapperProblems"][0]["id"]

        while True:
            problem_response = self.session.get(
                f"{BASE_URL}/api/problems/{str(problem_id)}"
            )
            if problem_response.status_code == 200:
                break

        problem_dict = json.loads(problem_response.text)
        self.problem.name = problem_dict["name"]
        self.problem.known_quantities = problem_dict["knownQuantities"]
        self.problem.unknown_quantities = problem_dict["unknownQuantities"]
        self.problem.graphs = problem_dict["graphs"]
        self.problem.id = problem_id
        self.uq = len(self.problem.unknown_quantities)
        self.eq = len(self.problem.equations)
        self.gs = len(self.problem.graphs[0]["paths"])


def login():
    driver.get(BASE_URL)

    while True:
        try:
            username_input = driver.find_element(By.ID, "username")
        except:
            time.sleep(1)
        else:
            break

    username_input.clear()
    username_input.send_keys("agent")

    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys("agent")

    password_input.send_keys(Keys.ENTER)


def read_resolutions():
    file = open("resolutions", "r")
    resolutions = json.loads(file.read())
    file.close()
    return resolutions


def write_resolutions(resolutions):
    file = open("resolutions", "w")
    file.write(json.dumps(resolutions, indent=4))
    file.close()


# Read resolutions json and convert to dict
# Find which problem and resolution we have to run
# Run resolution
# Save results to json


def main():
    global driver
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    login()

    try:
        resolutions = read_resolutions()
        start_problem = len(resolutions) - 1
        start_resolution = len(resolutions[-1]["resolutions"])
    except:
        resolutions = []
        start_problem = 0
        start_resolution = 0

    if start_resolution == max_resolutions:
        start_problem += 1
        start_resolution = 0

    # for i in range(25):
    #    fu = FakeUser(problemas25[i])
    #    print(f"{i+1}: {fu.problem.name}")
    # quit()
    # Skipped:
    # start = 19
    # problemas = problemas25[problemas25.index(start):]
    indice = 6  # Debe ser igual al número problemas resueltos (names) en resolutions
    problemas = problemas25[start_problem:]
    for p in problemas:
        fu = FakeUser(p)
        problem = {
            "name": fu.problem.name,
            "id": fu.problem.id,
            "graph_length": fu.gs,
            "unknown_quantities": fu.uq,
            "resolutions": (
                [] if start_resolution == 0 else read_resolutions()[-1]["resolutions"]
            ),
        }
        for r in range(start_resolution, max_resolutions):
            resolutions = read_resolutions()
            print(f"PROBLEM {p} (index={problemas25.index(p)}) | RESOLUTION {r}")
            fu.solve_problem()
            resolution = {
                "state": fu.finish_state,
                "steps": fu.steps,
                "helps": fu.helps,
                "variables": fu.nb,
                "equations": fu.eq,
            }
            # print(resolution)
            problem["resolutions"].append(resolution)
            resolutions[-1] = problem
            write_resolutions(resolutions)
            time.sleep(5)
        resolutions.append(problem)
        write_resolutions(resolutions)
        start_resolution = 0
    driver.quit()


if __name__ == "__main__":
    main()
