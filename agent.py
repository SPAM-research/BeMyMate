import json
import requests

from unidecode import unidecode

from llmHandler import LlmHandler


base_url = "http://localhost:8080"

"""
TODO:
    Maybe Done - Ignore (do not process) message if agent sent the last message.
    - Move user and problem to new classes
    - Change frontend other-user icon
    - Fix having to reaload chat page to show message
"""


class Agent:
    def __init__(self, frame):
        self.room_id = frame.body.split(":")[1]
        self.session = requests.Session()
        self.llm_handler = LlmHandler()
        self.problem = {}
        self.problem["problem_id"] = -1
        self.have_processed_first = False
        self.create_user()

    def __str__(self):
        return self.room_id

    def process_message(self, frame):
        if not self.have_processed_first:
            self.have_processed_first = True
            return

        body = json.loads(frame.body)
        new_problem_id = body["problem"]["id"]
        self.get_resolution_info(body)
        self.llm_handler.set_resolution_info(self.problem)

        if self.last_message_from_agent():
            return

        if self.problem["problem_id"] != new_problem_id:
            self.get_problem_info(body)
            self.llm_handler.set_problem(self.problem)
        else:
            print("CHAT MESSAGE")
            self.handle_chat_message()

    def last_message_from_agent(self):
        if self.problem["chat"][-2]["sender"] == self.user["username"]:
            return True
        else:
            return False

    def login_user(self, username, password):
        while True:
            if (
                self.session.post(
                    f"{base_url}/api/login",
                    json={
                        "username": username,
                        "password": password,
                        "timeZone": "UTC",
                    },
                ).status_code
                == 200
            ):
                break

    def get_problem_info(self, body):
        problem_id = body["problem"]["id"]

        while True:
            problem_response = self.session.get( f"{base_url}/api/problems/{str(problem_id)}")
            if problem_response.status_code == 200:
                break

        self.problem["problem_id"] = problem_id
        problem_dict = json.loads(problem_response.text)
        # self.problem_text = problem_json["text"]
        self.problem["problem_known_quantities"] = problem_dict["knownQuantities"]
        self.problem["problem_unknown_quantities"] = problem_dict["unknownQuantities"]
        self.problem["problem_graphs"] = problem_dict["graphs"]

    def get_resolution_info(self, body):
        # This should be in get_problem_info but the endpoint returns null
        self.problem["problem_text"] = body["problem"]["text"]
        self.problem["problem_notebook"] = body["notebook"]
        self.problem["problem_equations"] = body["equations"]
        self.problem["chat"] = body["chat"]

    def handle_chat_message(self):
        self.llm_handler.set_resolution_info(self.problem)
        response = self.llm_handler.call()
        response = "RESPONSE"
        # response = "2*(x - 4 -6) = x - 6"
        if True:
            while True:
                if (
                    self.session.put(
                        f"{base_url}/api/chat/{self.room_id}",
                        json={"message": response, "variable": "variable"},
                    ).status_code
                    == 200
                ):
                    break
            print("AGENT SENT MESSAGE")

    def create_user(self):
        self.login_user("admin", "admin")

        # Get new user's random info
        while True:
            user_info_response = self.session.get(
                "https://randomuser.me/api/1.4/?nat=es"
            )
            if user_info_response.status_code == 200:
                break
        user_dict = json.loads(user_info_response.text)["results"][0]

        # Create new user
        self.user = {}
        self.user["username"] = unidecode(
            f"{user_dict['name']['first']}_{user_dict['name']['last']}".lower()
        )
        self.user["email"] = user_dict["email"]
        self.user["password"] = user_dict["login"]["sha256"]
        self.user["sex"] = user_dict["gender"].title()
        new_user = {
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
        }

        # Register the new user and login
        while True:
            if (
                self.session.post(f"{base_url}/api/signup", json=new_user).status_code
                == 200
            ):
                break
        self.login_user(self.user["username"], self.user["password"])

    def __del__(self):
        while True:
            if (
                self.session.delete(
                    f"{base_url}/api/users/{self.user['username']}"
                ).status_code
                == 200
            ):
                break

        print("AGENT DELETED")
