from enum import StrEnum, auto


class NotificationCategoryV1(StrEnum):
    service = auto()
    content_updates = auto()
    recommendations = auto()
