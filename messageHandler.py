import time
import json
import random
import sys

import stomp

from agent import Agent


class MyListener(stomp.ConnectionListener):
    def __init__(self, connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = connection
        self.agents = {}

    def on_error(self, frame):
        print(f"ERROR: {frame.body}")

    def on_message(self, frame):
        if frame.body.startswith("ROOM_CREATED"):
            room_id = frame.body.split(":")[1]
            self.conn.subscribe(
                destination="/topic/room-" + room_id, id=room_id, ack="auto"
            )
            self.agents[room_id] = Agent(frame)
        elif frame.body == "reset":
            room_id = frame.headers["subscription"]
            del self.agents[room_id]
        else:
            #print(json.dumps(json.loads(frame.body), indent=2))
            room_id = frame.headers["subscription"]
            self.agents[room_id].process_message(frame)
            return
            try:
                room_id = frame.headers["subscription"]
                self.agents[room_id].process_message(frame)
            except:
                print(
                    f"UNEXPECTED ERROR FROM SUBSCRIPTION {frame.headers['subscription']}"
                )
                print(frame)
                ...


def main():
    conn = stomp.Connection([("localhost", 61613)], heartbeats=(4000, 4000))
    conn.set_listener("", MyListener(conn))
    conn.connect("admin", "admin", wait=True)
    conn.subscribe(destination="/topic/agents", id=0, ack="auto")
    while True:
        time.sleep(120)
    conn.disconnect()


if __name__ == "__main__":
    main()
