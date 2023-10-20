import json
import requests

from unidecode import unidecode

from llmHandler import LlmHandler


base_url = "http://localhost:8080"

'''
TODO:
    - Ignore (do not process) message if agent sent the last message.
    - Do while status!=200 for all requests
    - Try to change frontend other-user icon
'''

class Agent:
    def __init__(self, frame):
        self.room_id = frame.body.split(":")[1]
        self.session = requests.Session()
        self.problem_id = -1
        self.llm_handler = LlmHandler()
        self.create_user()

    def create_user(self):
        login_response = self.session.post(
            f"{base_url}/api/login",
            json={"username": "admin", "password": "admin", "timeZone": "UTC"},
        )
        if login_response.status_code != 200:
            print("ADMIN LOGIN FAILED")
            return
        else:
            user_info_response = self.session.get(
                "https://randomuser.me/api/1.4/?nat=es"
            )
            if user_info_response.status_code != 200:
                print("FAILED GET RANDOM USER")
                return

            user_dict = json.loads(user_info_response.text)["results"][0]
            self.user = {}
            self.user["username"] = unidecode(
                f"{user_dict['name']['first']}_{user_dict['name']['last']}".lower()
            )
            self.user["email"] = user_dict["email"]
            self.user["password"] = user_dict["login"]["sha256"]
            self.user["sex"] = user_dict["gender"].title()

            new_user_response = self.session.post(
                f"{base_url}/api/signup",
                json={
                    "massive": False,
                    "birth": "0001-01-01",
                    "email": self.user["email"],
                    "group": None,
                    "language": "spanish",
                    "name": "dummy",
                    "password": self.user["password"],
                    "role": "admin",
                    "sex": self.user["sex"],
                    "surname": "dummy",
                    "username": self.user["username"],
                },
            )

            login_response = self.session.post(
                f"{base_url}/api/login",
                json={
                    "username": self.user["username"],
                    "password": self.user["password"],
                    "timeZone": "UTC",
                },
            )
            if login_response.status_code != 200:
                print("NEW USER LOGIN FAILED")

    def __del__(self):
        login_response = self.session.post(
            f"{base_url}/api/login",
            json={"username": "admin", "password": "admin", "timeZone": "UTC"},
        )
        if login_response.status_code != 200:
            print("ADMIN LOGIN FAILED")
            return
        else:
            delete_user_response = self.session.delete(f"{base_url}/api/users/{self.user['username']}")
            if delete_user_response.status_code != 200:
                print("FAILED DELETING USER")
        print("AGENT DELETED")




    def process_message(self, frame):
        # print("\n\n\n\n")
        # print(json.dump(frame.body, 2))
        body = json.loads(frame.body)
        new_problem_id = body["problem"]["id"]
        self.get_resolution_info(body)

        if self.problem_id != new_problem_id:
            self.get_problem_info(body)
        else:
            self.handle_chat_message()

    def get_problem_info(self, body):
        problem_id = body["problem"]["id"]

        problem_response = self.session.get(
            f"{base_url}/api/problems/{str(problem_id)}"
        )

        if problem_response.status_code != 200:
            print("ERROR GETTING PROBLEM DETAILS")
        else:
            self.problem_id = problem_id
            problem_dict = json.loads(problem_response.text)
            # self.problem_text = problem_json["text"]
            self.problem_known_quantities = problem_dict["knownQuantities"]
            self.problem_unknown_quantities = problem_dict["unknownQuantities"]
            self.problem_graphs = problem_dict["graphs"]

    def get_resolution_info(self, body):
        # This should be in get_problem_info but the endpoint returns null
        self.problem_text = body["problem"]["text"]
        self.problem_notebook = body["notebook"]
        self.problem_equations = body["equations"]

    def __str__(self):
        return self.room_id

    def handle_chat_message(self):
        self.llm_handler.set_problem_info(
            self.problem_text,
            self.problem_known_quantities,
            self.problem_unknown_quantities,
            self.problem_graphs,
        )
        self.llm_handler.set_resolution_info(
            self.problem_notebook, self.problem_equations
        )
        response = self.llm_handler.call()
        # print(response)
        # Decide wether to output it to the chat or not
        output = True
        # Output to the chat
        if output:
            chat_response = self.session.put(
                f"{base_url}/api/chat/{self.room_id}",
                json={"message": response, "variable": "variable"},
            )
            if chat_response.status_code != 200:
                print("CHAT MESSAGE FAILED")
