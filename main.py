import json
from typing import Dict
import signal
import requests
import stomp
from stomp.utils import Frame
import asyncio
from cmd import Cmd
import time
from threading import Thread
import re
from constants import ROOM_CREATED, RESET, BASE_URL
from models.problem import Problem
import utils.process_message_utils as process_message_utils 
import config.config as config
import multiprocessing as mp
from models.message import Message
import os
def read_message(queue: mp.Queue) -> str:
    while True:
        # print(queue.get().problem.chat[-1]["message"])
        message: Message = queue.get()
        process_message_utils.process_message(message.room_uuid, message.problem)

token = requests.post(
    f"{BASE_URL}/api/login",
    #"https://tutorchat.uv.es/api/login",
    json={
        "username": os.getenv("AGENT_USERNAME"),
        "password": os.getenv("AGENT_PASSWORD"),
        "timeZone": "Europe/Madrid",
        "lastConnection": 0,
    },
).json()["access_token"]


def get_problem(frame):
    problem_chat_data = json.loads(frame.body)
    problem_chat = Problem.from_dict(problem_chat_data["problem"]) # Retrieve Problem object (text, notebooks, etc.)
    problem_chat.final_report = Problem.from_dict(problem_chat_data).final_report
    problem_graph_response = requests.get(
        f"{BASE_URL}/api/problems/{problem_chat.id}",
        headers={
            "Authorization": token
        }
    )
    problem_graph_data = json.loads(problem_graph_response.content)
    problem_graph = Problem.from_dict(problem_graph_data) # Retrieve Problem Graph object (KnownQuantities, UnknownQuantities, etc.)

    problem = Problem(
        id=problem_chat.id,
        name=problem_chat.name,
        text=problem_chat.text,
        chat=problem_chat_data.get("chat", []),
        known_quantities=problem_graph_data.get("knownQuantities", []),
        unknown_quantities=problem_graph_data.get("unknownQuantities", []),
        last_suggestion=problem_chat_data.get("lastSuggestion", ""),
        graphs=problem_graph_data.get("graphs", []),
        notebook=problem_chat_data.get("notebook", []),
        equations=problem_chat_data.get("equations", []),
        image=problem_chat.image,
        initial_help_level=problem_graph_data.get("initialHelpLevel", 0),
        max_resolution_time_in_seconds=problem_chat_data["problem"].get("maxResolutionTimeInSeconds", -100),
        uid=problem_chat_data["problem"].get("uid", ""),
        video=problem_chat.video,
        final_report=problem_chat.final_report
    )

    return problem

class RoomListener(stomp.ConnectionListener):
    agent_map: Dict[str, asyncio.Task]
    connection: stomp.Connection12
    current_exercise = 0
    

    def __init__(self, connection, queue: mp.Queue):
        super().__init__()
        self.agent_map = {}
        self.connection = connection
        self.queue = queue

    

    def on_error(self, frame):
        print(f"ERROR: {frame.body}")

    def on_message(self, frame: Frame):
        
        message_topic_destination = frame.headers["destination"]
    
        if message_topic_destination == "/topic/agents":
            if frame.body.startswith(ROOM_CREATED):
                room_uuid = frame.body.split(":")[1]
                self.connection.subscribe(f"/topic/room-{room_uuid}", len(self.agent_map) + 1)
                self.agent_map[f"/topic/room-{room_uuid}"] = None
                # frame.body = requests.get(
                #     url=f"{BASE_URL}/api/chat/{room_uuid}",
                #     params={
                #         "wrapperId": 5,
                #         "exerciseId": 0,
                #         "next": "false"
                #     },
                #     headers={
                #         "Authorization": token
                #     }
                # ).content
                # problem: Problem = get_problem(frame)
                # message: Message = Message(room_uuid, problem)
                # self.queue.put(message)

        if re.match(r"/topic/room-", message_topic_destination):
            room_uuid = message_topic_destination.split("-", 1)[1]
            if frame.body == RESET:
                while not self.queue.empty():
                    self.queue.get()
                self.connection.unsubscribe(id=frame.headers["subscription"]) # room is deleted. Unsubscribe from such room
                print(f"unsubscribing from {message_topic_destination}")
                return
            problem: Problem = get_problem(frame)
            if problem.final_report is not None: # if problem has been solved
                while not self.queue.empty():
                    self.queue.get()
                self.current_exercise = self.current_exercise + 1
                return
            message: Message = Message(room_uuid, problem)
            while not self.queue.empty(): # agent should only respond to the previous message, otherwise they'd accumulate and give a sensation of delay
                self.queue.get()
            self.queue.put(message)



def main():
    config.install_argostranslate_language_packages()
    queue = mp.Queue()
    read_process: mp.Process = mp.Process(target=read_message, args=(queue,))
    read_process.start()
    conn = stomp.Connection([("localhost", 61613)])
    conn.set_listener('', RoomListener(conn, queue ))
    conn.connect("admin", "admin", wait=True)
    conn.subscribe("/topic/agents", 0)
    # Cmd is used to ensure the app keeps running 
    # Otherwise, the program would finish and stomp connections would be closed
    cmd = Cmd()
    signal.signal(signal.SIGINT, lambda x,y: conn.disconnect())

    cmd.cmdloop()

if __name__ == "__main__":
    main()