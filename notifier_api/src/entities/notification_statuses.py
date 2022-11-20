from enum import StrEnum, auto


class NotificationStatusesV1(StrEnum):
    created = auto()
    processed = auto()
    error = auto()
