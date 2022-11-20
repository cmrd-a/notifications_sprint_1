from functools import lru_cache

import pytz
from fastapi import Depends
from psycopg2.extensions import connection

from db.postgres import get_postgres
from models.notification import NotificationTaskV1


class PGService:
    def __init__(self, conn: connection):
        self.conn = conn

    def save_notification(self, notification: NotificationTaskV1) -> None:
        with self.conn.cursor() as cur:
            sql = """
                INSERT INTO notifications (task_id, users_ids, message, status, channel, category, send_time) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            args = (
                notification.task_id,
                notification.users_ids,
                notification.message,
                notification.status.value,
                notification.notification_channel.value,
                notification.notification_category.value,
                notification.send_time.replace(tzinfo=pytz.utc).isoformat(),
            )
            cur.execute(sql, args)
            self.conn.commit()


@lru_cache()
def get_postgres_service(
    postgres_connection: connection = Depends(get_postgres),
) -> PGService:
    return PGService(postgres_connection)
