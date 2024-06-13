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

""" Callback function. The function does 'nothing'. It is implemented because it's mandatory to 
pass a callback function on tasks"""
def pass_callback(*args, **kwargs):
    return

token = requests.post(
    f"{BASE_URL}/api/login",
    #"https://tutorchat.uv.es/api/login",
    json={
        "username": "agent",
        "password": "agent",
        "timeZone": "Europe/Madrid",
        "lastConnection": 0,
    },
).json()["access_token"]


def get_problem(frame):
    problem_chat_data = json.loads(frame.body)
    problem_chat = Problem.from_dict(problem_chat_data["problem"]) # Retrieve Problem object (text, notebooks, etc.)

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
        video=problem_chat.video
    )

    return problem

class RoomListener(stomp.ConnectionListener):
    agent_map: Dict[str, asyncio.Task]
    connection: stomp.Connection12
    loop: asyncio.AbstractEventLoop

    def __init__(self, connection, loop):
        super().__init__()
        self.agent_map = {}
        self.connection = connection
        self.loop = loop

    def on_error(self, frame):
        print(f"ERROR: {frame.body}")

    def on_message(self, frame: Frame):
        message_topic_destination = frame.headers["destination"]
        
        print(frame.body)

        if message_topic_destination == "/topic/agents":
            if frame.body.startswith(ROOM_CREATED):
                room_uuid = frame.body.split(":")[1]
                self.connection.subscribe(f"/topic/room-{room_uuid}", len(self.agent_map) + 1)
                self.agent_map[f"/topic/room-{room_uuid}"] = None

        if re.match(r"/topic/room-", message_topic_destination):
            room_uuid = message_topic_destination.split("-", 1)[1]
            if frame.body == RESET:
                self.connection.unsubscribe(message_topic_destination) # room is deleted. Unsubscribe from such room
            # else: process message
            problem: Problem = get_problem(frame)
            task = asyncio.Task(process_message_utils.process_message(room_uuid, problem), loop=self.loop, eager_start=True)
            task.add_done_callback(pass_callback)



def main():
    config.install_argostranslate_language_packages()
    loop = asyncio.new_event_loop()
    conn = stomp.Connection([("localhost", 61613)])
    conn.set_listener('', RoomListener(conn, loop ))
    conn.connect("admin", "admin", wait=True)
    conn.subscribe("/topic/agents", 0)
    # Cmd is used to ensure the app keeps running 
    # Otherwise, stomp connections would be closed
    cmd = Cmd()
    signal.signal(signal.SIGINT, lambda x,y: conn.disconnect())
    Thread(target=loop.run_forever).start()
    cmd.cmdloop()

if __name__ == "__main__":
    main()