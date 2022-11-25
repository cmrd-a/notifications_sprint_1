from datetime import datetime

from entities.notification_category import NotificationCategoryV1
from entities.notification_channel import NotificationChannelV1
from entities.notification_statuses import NotificationStatusesV1
from models.common import Base


class NotificationTaskV1(Base):
    users_ids: list[int]
    template_name: str
    variables: dict
    status: NotificationStatusesV1
    channel: NotificationChannelV1
    category: NotificationCategoryV1
    send_time: datetime
