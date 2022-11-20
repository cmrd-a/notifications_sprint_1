from datetime import datetime

from entities.notification_category import NotificationCategoryV1
from entities.notification_channel import NotificationChannelV1
from entities.notification_statuses import NotificationStatusesV1
from models.common import Base


class NotificationTaskV1(Base):
    task_id: str
    content_id: str
    users_ids: list[int]
    message: str
    notification_subject: str
    template_name: str
    status: NotificationStatusesV1
    notification_channel: NotificationChannelV1
    notification_category: NotificationCategoryV1
    send_time: datetime
