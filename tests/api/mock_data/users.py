import uuid


class UserPayloadBuilder:
    def __init__(self):
        unique = uuid.uuid4().hex[:8]
        self._name = f"Test User {unique}"
        self._email = f"user_{unique}@test.com"
        self._password = "TestPassword123"

    def with_name(self, name):
        self._name = name
        return self

    def with_email(self, email):
        self._email = email
        return self

    def with_password(self, password):
        self._password = password
        return self

    def build(self):
        return {
            "name": self._name,
            "email": self._email,
            "password": self._password,
        }

    def login_payload(self):
        return {"email": self._email, "password": self._password}
