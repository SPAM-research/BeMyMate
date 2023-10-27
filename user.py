import json

from unidecode import unidecode


class User:
    username = ""
    email = ""
    password = ""
    sex = ""

    def __init__(self, session):
        # Get new user's random info
        while True:
            user_info_response = session.get(
                "https://randomuser.me/api/1.4/?nat=es"
            )
            if user_info_response.status_code == 200:
                break
        user_dict = json.loads(user_info_response.text)["results"][0]

        # Create new user
        self.username = unidecode(
            f"{user_dict['name']['first']}_{user_dict['name']['last']}".lower()
        )
        self.email = user_dict["email"]
        self.password = user_dict["login"]["sha256"]
        self.sex = user_dict["gender"].title()

    def for_backend(self):
        return {
            "massive": False,
            "birth": "0001-01-01",
            "email": self.email,
            "group": None,
            "language": "spanish",
            "name": "dummy",
            "password": self.password,
            "role": "admin",
            "sex": self.sex,
            "surname": "dummy",
            "username": self.username,
        }
