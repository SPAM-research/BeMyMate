import json
import requests
import time
import re

from llmHandler import LlmHandler
from problem import Problem
from user import User
from utils import last_message_is_clarification, get_message_for_clarification, last_message_is_suggestion, get_message_for_suggestion


base_url = "https://betatutorchat.uv.es"

"""
TODO:
    - Change frontend other-user icon
    - The agent should never solve the problem ?? but if it did the problem should end
"""


class Agent:
    session = requests.Session()
    problem = Problem()
    llm_handler = LlmHandler(problem)
    have_processed_first = False

    def __init__(self, frame):
        self.room_id = frame.body.split(":")[1]
        self.create_user()

    def __str__(self):
        return self.room_id

    def process_message(self, frame):
        body = json.loads(frame.body)

        self.get_resolution_info(body)

        new_problem_id = body["problem"]["id"]

        if self.problem.id != new_problem_id:
            self.get_problem_info(body)
        

        #time.sleep(3)
        response = "LOL NO"
        #if not self.have_processed_first:
        #    self.send_message("Hola")
        if not self.last_message_is_from_tutor():
            ...
        elif last_message_is_clarification(self.problem):
            #self.send_message(get_message_for_clarification(self.problem))
            response = get_message_for_clarification(self.problem)
        elif last_message_is_suggestion(self.problem):
            #self.send_message(get_message_for_suggestion(self.problem))
            response = get_message_for_suggestion(self.problem)
        else:
            #response = self.llm_handler.call()
            response = "NOPE"
            #self.send_message(response)
            #print("###############################")

        print(f"LLM RESPONSE: {response}")
        opt = input("DEFAULT?")
        if opt == "":
            self.send_message(response)
        else:
            self.send_message(opt)

        print("\n\n\n\n\n\n\n\n")
        #self.have_processed_first = True
        #print("DONE PROCESSING MESSAGE")
            
    def last_message_is_from_tutor(self):
        return self.problem.chat[-1]["sender"] == "system"

    def login(self, username, password):
        while True:
            if (
                self.session.post(
                    f"{base_url}/api/login",
                    json={
                        "username": username,
                        "password": password,
                        "timeZone": "Europe/Madrid",
                        "lastConnection": 0,
                    },
                ).status_code
                == 200
            ):
                break
        #print(f"LOGGED IN AS {username}")

    def get_problem_info(self, body):
        problem_id = body["problem"]["id"]

        while True:
            problem_response = self.session.get(
                f"{base_url}/api/problems/{str(problem_id)}"
            )
            if problem_response.status_code == 200:
                break

        self.problem.id = problem_id
        problem_dict = json.loads(problem_response.text)
        # self.problem.text = problem_json["text"]
        self.problem.known_quantities = problem_dict["knownQuantities"]
        self.problem.unknown_quantities = problem_dict["unknownQuantities"]
        self.problem.graphs = problem_dict["graphs"]

    def get_resolution_info(self, body):
        # This should be in get_problem_info but the endpoint returns null
        self.problem.text = body["problem"]["text"]
        self.problem.notebook = body["notebook"]
        self.problem.equations = body["equations"]
        self.problem.chat = [{"sender": c["sender"], "message": self.clean_chat_message(c["message"])} for c in body["chat"]]
        last_clean_message = self.problem.chat[-1]['message']
        last_original_message = body['chat'][-1]['message'].replace('\r','')
        print(f"LAST ORIGINAL MESSAGE: {last_original_message}")
        print(f"LAST CLEAN MESSAGE: {last_clean_message}")
    
    def clean_chat_message(self, message):
        print(f"INCLEAN ORIG: {message}")
        message = message.replace("\r", "")
        print(f"INCLEAN AFTER: {message}")
        message = re.sub(r"<br.*?>", "\n", message)
        return message

    def send_message(self, message):
        while True:
            if (
                self.session.put(
                    f"{base_url}/api/chat/{self.room_id}",
                    json={"message": message, "variable": "variable"},
                ).status_code
                == 200
            ):
                break
        #print("AGENT SENT MESSAGE")

    def create_user(self):
        self.login("agent", "agent")
        return

        # Create random user
        self.user = User(self.session)

        # Register the new user and login
        while True:
            if (
                self.session.post(
                    f"{base_url}/api/signup", json=self.user.for_backend()
                ).status_code
                == 200
            ):
                break
        #print("CREATED NEW TEMPORARY USER")
        self.login(self.user.username, self.user.password)

    def __del__(self):
        while True:
            if (
                self.session.delete(
                    f"{base_url}/api/users/{self.user.username}"
                ).status_code
                == 200
            ):
                break
        print("AGENT DELETED")
