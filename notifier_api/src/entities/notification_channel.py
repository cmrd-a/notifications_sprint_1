from enum import Enum, auto


class NotificationChannelV1(Enum):
    email = auto()
    push = auto()
    sms = auto()
