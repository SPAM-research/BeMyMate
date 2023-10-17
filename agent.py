import json
import requests


base_url = "http://localhost:8080/api"


class Agent:
    def __init__(self, frame):
        self.room_id = frame.body.split(":")[1]
        self.session = requests.Session()
        self.problem_id = -1
        login_response = self.session.post(
            base_url + "/login",
            json={"username": "admin", "password": "admin", "timeZone": "UTC"},
        )
        if login_response.status_code != 200:
            print("LOGIN FAILED")


    def process_message(self, frame):
        body = json.loads(frame.body)
        new_problem_id = body["problem"]["id"]

        if self.problem_id != new_problem_id:
            self.get_problem_info(body)
            self.get_resolution_info(body)
        else:
            # it's probably? a chat message
            # CALL MODEL
            print("CHAT MESSAGE?")

    def get_problem_info(self, body):
        problem_id = body["problem"]["id"]

        problem_response = self.session.get(
            base_url + "/problems/" + str(problem_id)
        )

        if problem_response.status_code != 200:
            print("ERROR GETTING PROBLEM DETAILS")
        else:
            self.problem_id = problem_id
            problem_json = json.loads(problem_response.text)
            self.problem_graphs = problem_json["graphs"]
            self.problem_known_quantities = problem_json["knownQuantities"]
            self.problem_unknown_quantities = problem_json["unknownQuantities"]
            

    def get_resolution_info(self, body):
        self.problem_text = body["problem"]["text"] # This should be in get_problem_info but the endpoint returns null
        self.problem_notebook = body["notebook"]
        self.problem_equations = body["equations"]


    def __str__(self):
        return self.room_id
