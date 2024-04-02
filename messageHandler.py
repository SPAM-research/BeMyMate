import time
import json
import random
import sys
import requests

import stomp

from agent import Agent

token = requests.post(
    "https://betatutorchat.uv.es/api/login",
    #"https://tutorchat.uv.es/api/login",
    json={
        "username": "agent",
        "password": "agent",
        "timeZone": "Europe/Madrid",
        "lastConnection": 0,
    },
).json()["access_token"]

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
            print(f"ROOM CREATED: {room_id}")
            self.conn.subscribe(
                destination=f"/topic/room-{room_id}",
                id=room_id,
                ack="client",
                headers={"Authorization": token},
            )
            self.agents[room_id] = Agent(frame)
        elif frame.body == "reset":
            room_id = frame.headers["subscription"]
            del self.agents[room_id]
        else:
            room_id = frame.headers["subscription"]
            self.agents[room_id].process_message(frame)


def main():
    conn = stomp.WSStompConnection(
        [("betatutorchat.uv.es", 443)],
        #[("tutorchat.uv.es", 443)],
        ws_path="/api/ws",
        keepalive=True,
        heartbeats=(40000, 40000),
        vhost="/",
    )
    conn.transport.__need_ssl = lambda *args, **kwargs: True
    conn.set_listener("", MyListener(conn))
    conn.transport._WSTransport__ssl_params[("betatutorchat.uv.es", 443)] = {}
    #conn.transport._WSTransport__ssl_params[("tutorchat.uv.es", 443)] = {}
    conn.connect("admin", "admin", wait=True)
    conn.transport.set_connected(True)
    conn.subscribe(
        destination="/topic/agents",
        id=0,
        ack="client",
        headers={"Authorization": token},
    )
    while True:
        time.sleep(20)
    conn.disconnect()


if __name__ == "__main__":
    main()