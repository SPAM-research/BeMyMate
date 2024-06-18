from models.problem import Problem

""" Message retrieved from message broker. Contains the room_uuid to which the message has been sent to and the problem information"""
class Message:
    def __init__(self, room_uuid: str, problem: Problem):
        self.room_uuid = room_uuid
        self.problem = problem