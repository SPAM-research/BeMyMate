import time
import json
import re
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from llmHandler import LlmHandler
from problem import Problem
from user import User
from utils import last_message_is_clarification, get_message_for_clarification, last_message_is_suggestion, get_message_for_suggestion

base_url = "https://betatutorchat.uv.es"
agents_collection = 15
default_sleep = 2

# Message passed as suggestion to LLM should be the last suggestion (after ayuda)
class FakeUser:
    problem = Problem()
    llm_handler = LlmHandler(problem)
    #driver = webdriver.Firefox(options=Options())
    driver = webdriver.Chrome()
    session = requests.Session()
    finished = False
    steps = 0
    helps = 0

    def __init__(self, problem_id):
        self.driver.delete_all_cookies()
        self.get_additional_problem_info(problem_id)
        self.login()
        time.sleep(default_sleep)
        self.enter_problem(problem_id)

        while not self.finished:
            print("ITERATION")
            self.get_problem_state()
            if not self.finished:
                self.send_message(self.get_message())
                time.sleep(default_sleep)
            print("\n")

        print("\n\n\n\n")
        print(f"STEPS: {self.steps}\tHELPS: {self.helps}\tVARS: {len(self.problem.notebook)}/{len(self.problem.unknown_quantities)}\t EQS: {len(self.problem.equations)}/{len(self.problem.graphs[0]['paths'])}")
    
        self.driver.quit()

    def get_message(self):
        if last_message_is_clarification(self.problem):
            #self.send_message(get_message_for_clarification(self.problem))
            response = get_message_for_clarification(self.problem)
        elif last_message_is_suggestion(self.problem):
            #self.send_message(get_message_for_suggestion(self.problem))
            response = get_message_for_suggestion(self.problem)
            if response == "<CALL LLM>": response = self.llm_handler.call()
        else:
            response = self.llm_handler.call()

        print(f"AGENT RESPONSE: {response}")
        opt = input("DEFAULT?")
        if opt != "":
            response = opt

        response = response.strip()

        if not re.search(r"[0-9]|si", response.lower()): self.steps+=1
        if re.search(r"ayuda", response.lower()): self.helps+=1

        return response
            
    def last_message_is_from_tutor(self):
        return self.problem.chat[-1]["sender"] == "system"

    def clean_chat_message(self, message):
        message = message.replace("\r", "")
        message = re.sub(r"</?br/?>", "\n", message)
        message = re.sub(r"&gt;", ">", message)
        return message

    def login(self):
        self.driver.get("https://betatutorchat.uv.es")
    
        while True:
            try: username_input = self.driver.find_element(By.ID, "username")
            except: time.sleep(1)
            else: break
        
        username_input.clear()
        username_input.send_keys("agent")
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys("agent")
        
        password_input.send_keys(Keys.ENTER)
    
    def reset_current_problem(self):
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Reiniciar')]").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".accept").click()
        
    def go_to_problem(self):
        while True:
            try: self.driver.find_element(By.CSS_SELECTOR, ".message_input_collection.message_input.form-control")
            except:
                self.driver.get(f"https://betatutorchat.uv.es/collections")
                time.sleep(default_sleep)
                while True:
                    try: collection = self.driver.find_element(By.ID, f"row-{str(agents_collection)}")
                    except:
                        self.driver.find_element(By.ID, "pagination-next-page").click()
                        time.sleep(1)
                    else: break
                collection.click()
                time.sleep(5)
            else: break
    
    def set_problem(self, problem_index):
        collection_dict = json.loads(open("collection_all_problems.json", "r").read())
        all_problems = collection_dict["problems"]
        number_of_problems = len(all_problems)
        #if problem_index >= number_of_problems: problem_index = number_of_problems
        collection_dict["problems"] = [all_problems[problem_index]]
        self.login_backend()
        while True:
            if (
                self.session.put(
                    f"https://betatutorchat.uv.es/api/wrapper/{str(agents_collection)}",
                    json=json.loads(json.dumps(collection_dict)),
                ).status_code
                == 200
            ):
                break

    def enter_problem(self, problem_index):
        self.set_problem(problem_index)
        time.sleep(default_sleep)
        self.go_to_problem()
        time.sleep(default_sleep)
        self.reset_current_problem()
        time.sleep(default_sleep)
        self.go_to_problem()
        #while True:
        #    try: self.driver.find_element(By.CSS_SELECTOR, ".message_input_collection.message_input.form-control")
        #    except:
        #        self.driver.get(f"https://betatutorchat.uv.es/collections/{str(agents_collection)}/problem/{problem_id}")
        #        time.sleep(5)
        #    else: break
        
    def send_message(self, message):
        chat_input = self.driver.find_element(By.CSS_SELECTOR, ".message_input_collection.message_input.form-control")
        chat_input.clear()
        chat_input.send_keys(message)
        chat_input.send_keys(Keys.ENTER)
    
    def check_if_finished(self):
        try:
            self.driver.find_element(By.XPATH, "//button[contains(text(), '¡Felicidades! Has resuelto el problema (Presiona para continuar)')]")
            self.finished = True
            print("FINISHED")
        except:
            ...
            print("NOT FINISHED")

    def get_problem_state(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        self.check_if_finished()
        self.problem.text = soup.find("p", class_="card-text").text
        self.problem.notebook = [note.text for note in soup.find_all("div", id="Notebook")[0].find_all("div") if not note.input]
        self.problem.equations = [note.text for note in soup.find_all("div", id="Notebook")[1].find_all("div") if not note.input]
        boxes = soup.find("ul", id="chatMessages").find_all("div", class_="box")
        self.problem.chat = [{"sender": ("system" if "left" in box.li["class"] else "user"), "message": self.clean_chat_message(box.find("div",class_="text").decode_contents())} for box in boxes]

    def login_backend(self):
        while True:
            if (
                self.session.post(
                    f"{base_url}/api/login",
                    json={
                        "username": "agent",
                        "password": "agent",
                        "timeZone": "Europe/Madrid",
                        "lastConnection": 0,
                    },
                ).status_code
                == 200
            ):
                break
        
    def get_additional_problem_info(self, problem_in_wrapper):
        self.login_backend()
        
        while True:
            wrapper_response = self.session.get(
                f"{base_url}/api/wrapper/{str(agents_collection)}/problems"
            )
            if wrapper_response.status_code == 200:
                break
            
        problem_id = json.loads(wrapper_response.text)["wrapperProblems"][problem_in_wrapper]["id"]
        
        while True:
            problem_response = self.session.get(
                f"{base_url}/api/problems/{str(problem_id)}"
            )
            if problem_response.status_code == 200:
                break
            
        problem_dict = json.loads(problem_response.text)
        self.problem.known_quantities = problem_dict["knownQuantities"]
        self.problem.unknown_quantities = problem_dict["unknownQuantities"]
        self.problem.graphs = problem_dict["graphs"]
            


def main():
    FakeUser(0)
    
if __name__ == "__main__":
    main()