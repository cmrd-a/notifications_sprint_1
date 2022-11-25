from enum import Enum


class NotificationStatusesV1(Enum):
    created = "created"
    processed = "processed"
    error = "error"
