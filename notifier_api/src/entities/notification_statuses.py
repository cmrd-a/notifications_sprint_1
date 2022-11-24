from enum import Enum, auto


class NotificationStatusesV1(Enum):
    created = auto()
    processed = auto()
    error = auto()
