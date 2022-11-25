from enum import Enum


class NotificationChannelV1(Enum):
    email = "email"
    push = "push"
    sms = "sms"
