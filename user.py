class User:
    username = ""
    email = ""
    password = ""
    sex = ""

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
