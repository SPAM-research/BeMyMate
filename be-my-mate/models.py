from typing import Any, List

from pydantic import BaseModel


class Problem(BaseModel):
    id: int
    name: str
    text: str
    chat: List[Any]
    known_quantities: List[str]
    unknown_quantities: List[str]
    last_suggestion: Any
    graphs: List[Any]
    notebook: List[Any]
    equations: List[Any]
    image: str
    initial_help_level: int
    max_resolution_time_in_seconds: int
    uid: str | int
    video: str
    final_report: Any


class Message:
    room_uuid: str
    problem: Problem
