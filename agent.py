import json
import requests

from llmHandler import LlmHandler


base_url = "http://localhost:8080/api"


class Agent:
    def __init__(self, frame):
        self.room_id = frame.body.split(":")[1]
        self.session = requests.Session()
        self.problem_id = -1
        self.llm_handler = LlmHandler()
        login_response = self.session.post(
            base_url + "/login",
            json={"username": "admin", "password": "admin", "timeZone": "UTC"},
        )
        if login_response.status_code != 200:
            print("LOGIN FAILED")

    def process_message(self, frame):
        body = json.loads(frame.body)
        new_problem_id = body["problem"]["id"]
        self.get_resolution_info(body)

        if self.problem_id != new_problem_id:
            self.get_problem_info(body)
        else:
            self.handle_chat_message()

    def get_problem_info(self, body):
        problem_id = body["problem"]["id"]

        problem_response = self.session.get(base_url + "/problems/" + str(problem_id))

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
                f"{base_url}/chat/{self.room_id}",
                json={"message": response, "variable": "variable"},
            )
            if chat_response.status_code != 200:
                print("CHAT MESSAGE FAILED")
