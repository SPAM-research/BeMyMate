from typing import Any, Dict, List
import signal
import sys
import stomp
from stomp.utils import Frame
import os
import asyncio
from cmd import Cmd
import time
import multiprocessing

def demo(room_id: str):
    print("ADIOS")
    time.sleep(10)
    print("HOOOOOOLAA")

def signal_handler(signal, frame):
    pass
class RoomCreatedListener(stomp.ConnectionListener):
    agent_map: Dict[str, multiprocessing.Process]
    connection: stomp.Connection11
    def __init__(self, connection):
        super().__init__()
        self.agent_map = {}
        self.connection = connection


    def on_message(self, frame: Frame):
        if frame.headers["destination"] == "/topic/agents":
            if frame.body.startswith("ROOM_CREATED"):
                room_id = frame.body.split(":")[1]
                self.connection.subscribe(f"/topic/room-{room_id}", len(self.agent_map) + 1)
                self.agent_map[f"/topic/room-{room_id}"] = None
                print(frame.headers)
                return
        subscription_id = int(frame.headers["subscription"]) - 1
        print(frame)
        if self.agent_map[frame.headers["destination"]] != None:
            self.agent_map[frame.headers["destination"]].terminate()
            
        p = multiprocessing.Process(target=demo, args=("",))
        p.start()
        self.agent_map[frame.headers["destination"]] = p


def main():
    conn = stomp.Connection([("localhost", 61613)])
    conn.set_listener('', RoomCreatedListener(conn ))
    conn.connect("admin", "admin", wait=True)
    conn.subscribe("/topic/agents", 0)
    cmd = Cmd()
    signal.signal(signal.SIGINT, lambda x,y: conn.disconnect())
    cmd.cmdloop()

if __name__ == "__main__":
    main()