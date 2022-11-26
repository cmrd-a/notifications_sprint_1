import json
from functools import lru_cache

import pytz
from fastapi import Depends
from psycopg import AsyncConnection

from db.postgres import get_postgres
from models.notification import NotificationTaskV1


class PGService:
    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def save_notification(self, notification: NotificationTaskV1) -> None:
        async with self.conn.cursor() as cur:
            sql = """
                INSERT INTO notifications 
                (users_ids, template_name, variables, status, channel, category, send_time) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            args = (
                notification.users_ids,
                notification.template_name,
                json.dumps(notification.variables),
                notification.status.name,
                notification.channel.name,
                notification.category.name,
                notification.send_time.replace(tzinfo=pytz.utc).isoformat(),
            )
            await cur.execute(sql, args)
            await self.conn.commit()


@lru_cache()
def get_postgres_service(
    postgres_connection: AsyncConnection = Depends(get_postgres),
) -> PGService:
    return PGService(postgres_connection)
