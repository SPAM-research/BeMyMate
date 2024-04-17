import time
import json
import re
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from llmHandler import LlmHandler
from problem import Problem
from user import User
from utils import last_message_is_clarification, get_message_for_clarification, last_message_is_suggestion, get_message_for_suggestion, get_definition_block_variable

base_url = "https://betatutorchat.uv.es"
agents_collection = 15
default_sleep = 3
max_consecutive_helps = 10
max_steps = 100
max_resolutions = 10
debug = False


#problemas100 = [0, 2, 5, 19, 20, 21, 22, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 53, 54, 57, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 82, 83, 84, 85, 87, 88, 98, 100, 101, 102, 108, 109, 110, 111, 112, 113, 114, 119, 120, 121, 124, 126, 128, 129, 130, 131, 132, 133, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 161, 171, 174, 180, 181, 182, 183, 184, 185, 186]

problemas25 = [0,2,5,19,20,21,22,27,28,29,30,31,32,34,39,40,57,71,78,79,80,87,120,209,210]




class FakeUser:
    def __init__(self, problem_in_wrapper):
        if debug: print("INIT")
        self.problem = Problem()
        self.session = requests.Session()
        self.set_problem(problem_in_wrapper)
        self.get_additional_problem_info()
        self.problem_in_wrapper = problem_in_wrapper

    def solve_problem(self):
        if debug: print("SOLVE PROBLEM")
        self.llm_handler = LlmHandler(self.problem)
        self.finished = False
        self.consecutive_helps = 0
        self.steps = 0
        self.helps = 0

        self.enter_problem(self.problem_in_wrapper)

        #print("SOLVING NOW")
        while not self.finished:
            self.get_problem_state()
            if not self.finished:
                self.send_message(self.get_message())
                time.sleep(default_sleep)
            #print("\n")

        self.save_statistics()

    def get_message(self):
        if debug: print("GET MESSAGE")
        if self.problem.chat[-1]["message"].startswith("Muy bien"):
            self.problem.last_suggestion = ""

        if last_message_is_clarification(self.problem):
            response = get_message_for_clarification(self.problem)
        elif last_message_is_suggestion(self.problem):
            self.problem.last_suggestion += "\n".join([l for l in self.problem.chat[-1]["message"].splitlines() if l])+"\n\n"
            response = get_message_for_suggestion(self.problem)
            if response == "<CALL LLM>": response = self.llm_handler.call()
        else:
            response = self.llm_handler.call()

        #response = self.ask_for_human_message(response)

        response = response.strip().lower()

        if var:=get_definition_block_variable(self.problem):
            if re.search("[a-z] es .*", response) and not re.search("ayuda", response):
                #print("DEFINITION BLOCK")
                response = f"{var}{response[1:]}"
                #print(response)

        if not re.search(r"^[0-9]+$|^si$", response): self.steps+=1
        file = open("steps","w")
        file.write(str(self.steps))
        file.close()
        if re.search(r"ayuda", response):
            self.helps+=1
            self.consecutive_helps+=1
        else:
            self.consecutive_helps = 0

        return response
    
    def save_statistics(self):
        if debug: print("SAVE STATS")
        self.nb = len(self.problem.notebook)
        self.uq = len(self.problem.unknown_quantities)
        self.eq = len(self.problem.equations)
        self.gs = len(self.problem.graphs[0]["paths"])
        if self.nb>self.uq: self.uq=self.nb
        if self.eq>self.gs: self.gs=self.eq
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
        if debug: print("RESET PROBLEM")
        try: driver.find_element(By.XPATH, "//button[contains(text(), 'Entendido')]").click()
        except: ...
        time.sleep(1)
        try: driver.find_element(By.XPATH, "//button[contains(text(), 'Reiniciar')]").click()
        except: ...
        time.sleep(1)
        try: driver.find_element(By.CSS_SELECTOR, ".accept").click()
        except: ...
        
    def go_to_problem(self):
        if debug: print("GOTO PROBLEM")
        while True:
            try: driver.find_element(By.CSS_SELECTOR, ".message_input_collection.message_input.form-control")
            except:
                driver.get(f"https://betatutorchat.uv.es/collections")
                time.sleep(default_sleep)
                while True:
                    while True:
                        try: driver.find_element(By.ID, "pagination-next-page")
                        except: time.sleep(1)
                        else: break
                    try: collection = driver.find_element(By.ID, f"row-{str(agents_collection)}")
                    except:
                        driver.find_element(By.ID, "pagination-next-page").click()
                        time.sleep(1)
                    else: break
                collection.click()
                time.sleep(5)
            else: break
    
    def set_problem(self, problem_index):
        if debug: print("SET PROBLEM")
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
                ).status_code == 200): break

    def enter_problem(self, problem_index):
        if debug: print("ENTER PROBLEM")
        self.go_to_problem()
        time.sleep(default_sleep)
        self.reset_current_problem()
        time.sleep(default_sleep)
        self.go_to_problem()
        #while True:
        #    try: driver.find_element(By.CSS_SELECTOR, ".message_input_collection.message_input.form-control")
        #    except:
        #        driver.get(f"https://betatutorchat.uv.es/collections/{str(agents_collection)}/problem/{problem_id}")
        #        time.sleep(5)
        #    else: break
        
    def send_message(self, message):
        if debug: print("SEND MESSAGE")
        self.go_to_problem()
        chat_input = driver.find_element(By.CSS_SELECTOR, ".message_input_collection.message_input.form-control")
        time.sleep(1)
        chat_input.clear()
        time.sleep(1)
        chat_input.send_keys(message)
        time.sleep(1)
        chat_input.send_keys(Keys.ENTER)
        time.sleep(1)
    
    def check_if_finished(self):
        if debug: print("CHECK FINISHED")
        try:
            driver.find_element(By.XPATH, "//button[contains(text(), '¡Felicidades! Has resuelto el problema (Presiona para continuar)')]")
            self.finished = True
        except:
            if self.consecutive_helps == max_consecutive_helps or self.steps == max_steps:
                self.finished = True

    def get_problem_state(self):
        if debug: print("GET PROBLEM STATE")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        self.check_if_finished()
        self.problem.text = soup.find("p", class_="card-text").text
        self.problem.notebook = [note.text for note in soup.find_all("div", id="Notebook")[0].find_all("div") if not note.input]
        self.problem.equations = [note.text for note in soup.find_all("div", id="Notebook")[1].find_all("div") if not note.input]
        boxes = soup.find("ul", id="chatMessages").find_all("div", class_="box")
        self.problem.chat = [{"sender": ("system" if "left" in box.li["class"] else "user"), "message": self.clean_chat_message(box.find("div",class_="text").decode_contents())} for box in boxes]

    def login_backend(self):
        if debug: print("LOGIN BACKEND")
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
        
    def get_additional_problem_info(self):
        if debug: print("GET ADD PROB INFO")
        self.login_backend()
        
        while True:
            wrapper_response = self.session.get(
                f"{base_url}/api/wrapper/{str(agents_collection)}/problems"
            )
            if wrapper_response.status_code == 200:
                break
            
        problem_id = json.loads(wrapper_response.text)["wrapperProblems"][0]["id"]
        
        while True:
            problem_response = self.session.get(
                f"{base_url}/api/problems/{str(problem_id)}"
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
    driver.get("https://betatutorchat.uv.es")

    while True:
        try: username_input = driver.find_element(By.ID, "username")
        except: time.sleep(1)
        else: break
    
    username_input.clear()
    username_input.send_keys("agent")
    
    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys("agent")
    
    password_input.send_keys(Keys.ENTER)

def main():
    global driver
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    login()
    results = []
    # Skipped: 
    start = 19
    problemas = problemas25[problemas25.index(start):]
    for p in problemas:
        fu = FakeUser(p)
        problem = {
            "name": fu.problem.name,
            "id": fu.problem.id,
            "graph_length": fu.gs,
            "unknown_quantities": fu.uq,
            "resolutions": []
        }
        for r in range(max_resolutions):
            print(f"PROBLEM {p} | RESOLUTION {r}")
            fu.solve_problem()
            resolution = {
                "state": fu.finish_state,
                "steps": fu.steps,
                "helps": fu.helps,
                "variables": fu.nb,
                "equations": fu.eq
            }
            problem["resolutions"].append(resolution)
            time.sleep(5)
        results.append(problem)
        f = open("resolutions", "a")
        #print(json.dumps(problem))
        f.write(json.dumps(problem))
        f.write(", ")
        f.close()
    #print(results)
    #open("resolutions", "w").write(json.dumps(results))
    driver.quit()
    
if __name__ == "__main__":
    main()
