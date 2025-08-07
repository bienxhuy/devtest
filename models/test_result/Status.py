from enum import Enum

class Status(Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"

    # Override the __str__ method to return the value of the enum
    # i.e: Instead of Status.SUCCESS, it will return "Success"
    def __str__(self):
        return self.value