from enum import Enum, auto


class NotificationCategoryV1(Enum):
    service = auto()
    content_updates = auto()
    recommendations = auto()
