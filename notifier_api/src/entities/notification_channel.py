from enum import StrEnum, auto


class NotificationChannelV1(StrEnum):
    email = auto()
    push = auto()
    sms = auto()
