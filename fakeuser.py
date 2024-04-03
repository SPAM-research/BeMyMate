import time
import re

from llmHandler import LlmHandler
from problem import Problem
from user import User
from utils import last_message_is_clarification, get_message_for_clarification, last_message_is_suggestion, get_message_for_suggestion


class FakeUser:
    problem = Problem()
    llm_handler = LlmHandler(problem)
    have_processed_first = False
    steps = 0
    helps = 0

    def process_message(self):
        self.get_resolution_info()
        response = self.llm_handler.call()
        print(f"##################\n{response}\n##################")

        #if not self.last_message_is_from_tutor():
        #    ...
        #elif last_message_is_clarification(self.problem):
        #    #self.send_message(get_message_for_clarification(self.problem))
        #    response = get_message_for_clarification(self.problem)
        #elif last_message_is_suggestion(self.problem):
        #    #self.send_message(get_message_for_suggestion(self.problem))
        #    response = get_message_for_suggestion(self.problem)
        #    if response == "<CALL LLM>": response = self.llm_handler.call()
        #else:
        #    response = self.llm_handler.call()

        #print(f"AGENT RESPONSE: {response}")
        #opt = input("DEFAULT?")
        #if opt != "":
        #    response = opt
        #self.send_message(response.strip())

        #if not re.search(r"[0-9]|si", response.lower()): self.steps+=1
        #if re.search(r"ayuda", response.lower()): self.helps+=1
        #print("\n\n\n\n\n\n\n")
        #print(f"STEPS: {self.steps}\tHELPS: {self.helps}\tVARS: {len(self.problem.notebook)}/{len(self.problem.unknown_quantities)}\t EQS: {len(self.problem.equations)}/{len(self.problem.graphs[0]['paths'])}")
            
    def last_message_is_from_tutor(self):
        return self.problem.chat[-1]["sender"] == "system"

    def get_resolution_info(self):
        self.problem.text = input("Problem text: ")
        #self.problem.notebook = body["notebook"]
        #self.problem.equations = body["equations"]
        #self.problem.chat = [{"sender": c["sender"], "message": self.clean_chat_message(c["message"])} for c in body["chat"]]
        #last_clean_message = self.problem.chat[-1]['message']
        last_message = self.clean_chat_message(input("Last message: "))
        self.problem.chat.append({"sender": "system", "message": last_message})
    
    def clean_chat_message(self, message):
        message = message.replace("\r", "")
        message = re.sub(r"<br.*?>", "\n", message)
        return message

#fu = FakeUser()
#fu.process_message()






from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


def login():
    global driver
    #driver = webdriver.Firefox(options=Options())
    driver = webdriver.Chrome()
    driver.get('https://betatutorchat.uv.es')

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
    time.sleep(3)

def reset_current_problem():
    driver.find_element(By.XPATH, "//button[contains(text(), 'Reiniciar')]").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".accept").click()
    time.sleep(3)
    
def go_to_problem(problem_id):
    while True:
        try: chat_input = driver.find_element(By.CSS_SELECTOR, ".message_input_collection.message_input.form-control")
        except:
            driver.get(f'https://betatutorchat.uv.es/collections/15/problem/{problem_id}')
            time.sleep(5)
        else: break

def enter_problem(problem_id):
    ## Enters the session
    #go_to_problem(problem_id)
    ## Resets the session
    #reset_current_problem()
    # Enters problem
    go_to_problem(problem_id)
    
def send_message(message):
    chat_input = driver.find_element(By.CSS_SELECTOR, ".message_input_collection.message_input.form-control")
    chat_input.clear()
    chat_input.send_keys(message)
    chat_input.send_keys(Keys.ENTER)

def get_problem_state():
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = soup.find("p", class_="card-text").text
    notebook = [note.text for note in soup.find_all("div", id="Notebook")[0].find_all("div") if not note.input]
    equations = [note.text for note in soup.find_all("div", id="Notebook")[1].find_all("div") if not note.input]
    boxes = soup.find("ul", id="chatMessages").find_all("div", class_="box")
    chat = [{"sender": ("system" if "left" in box.li["class"] else "user"), "message": box.find("div",class_="text").text} for box in boxes]
    print(title)
    print(notebook)
    print(equations)
    print(chat)
    
login()
enter_problem(0)
#send_message("hola")
get_problem_state()

time.sleep(10)
driver.quit()