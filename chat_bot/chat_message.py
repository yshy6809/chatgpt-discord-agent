import enum


class Role(enum.Enum):
    SYSTEM = 1
    USER = 2
    ASSISTANT = 3


class ChatMessage:
    def __init__(self, message: str, role: Role):
        self.message = message
        self.role = role

    def to_dict(self):
        return {
            "role": self.role.name.lower(),
            "content": self.message
        }
