import logging

import backoff
import psycopg2
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import DictCursor, DictRow
from enum import Enum, auto
from config import settings

logger = logging.getLogger(__name__)


class NotificationStatusesV1(Enum):
    created = auto()
    processed = auto()
    error = auto()


def get_conn() -> pg_connection:
    return psycopg2.connect(**settings.pg_connection_params, cursor_factory=DictCursor)


class PostgresService:
    def __init__(self):
        self.pg_conn: pg_connection | None = None
        self.make_connection()

    def __del__(self):
        self.pg_conn.close()

    @backoff.on_exception(backoff.expo, (psycopg2.InterfaceError, psycopg2.OperationalError), logger=logger)
    def make_connection(self):
        logging.info("Выполняется соединение с БД.")
        if isinstance(self, dict):
            _self: PostgresService = self["args"][0]
            _self.pg_conn = get_conn()
        else:
            self.pg_conn = get_conn()

    @backoff.on_exception(
        backoff.expo, (psycopg2.InterfaceError, psycopg2.OperationalError), on_backoff=make_connection, logger=logger
    )
    def make_select(self, query: str) -> list[DictRow]:

        with self.pg_conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def check_tasks(self):
        query = f"SELECT * FROM notifications WHERE status ='{NotificationStatusesV1.created.name}'"
        tasks = self.make_select(query)
        pass
