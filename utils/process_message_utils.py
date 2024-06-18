import json
import re
from time import sleep
from main import token

from requests import session
import requests
from models.problem import Problem
from constants import BASE_URL
from utils.generate_response import get_message_for_choice, get_message_for_suggestion
from utils.intention_analyzer import is_last_message_a_suggestion, is_message_a_choice
from utils.llm_handler import LlmHandler

def process_message(room_uuid: str, problem: Problem):

    # TODO: check if sender is different from the username assigned to agent
    # print(problem.chat[-1]["message"])
    if problem.chat[-1]["sender"] == "agent": # if last message is from the agent, do nothing until tutor answers back
        return

    llm_handler: LlmHandler = LlmHandler(problem)

    if is_message_a_choice(problem):
        response = get_message_for_choice(problem)
    elif is_last_message_a_suggestion(problem):
        response = get_message_for_suggestion(problem)
        if response == "<CALL LLM>": response = llm_handler.call()
    else: # a different message is assumed
        response = llm_handler.call()

    print(f"AGENT RESPONSE: {response}")
    # opt = input("Please, enter the response that should be sent by agent (if empty, the response will be the generated by the agent: ")
    # if opt != "":
    #     response = opt
    # print(f"IM GOING TO SEND A MESSAGE {response.strip()}")
    send_message(room_uuid, response.strip())


def login(self, username, password):
    while True:
        if (
            self.session.post(
                f"{BASE_URL}/api/login",
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

def send_message(room_uuid: str, message):
    print("IM SENDING MESSAGE")
    requests.put(
        f"{BASE_URL}/api/chat/{room_uuid}",
        json={"message": message, "variable": "variable"},
        headers={
            "Authorization": token
        }
    )

def __del__(self):
    while True:
        if (
            self.session.delete(
                f"{BASE_URL}/api/users/{self.user.username}"
            ).status_code
            == 200
        ):
            break
    print("AGENT DELETED")
