import json
import logging
import os
import uuid
from collections import namedtuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

import backoff
import httpx
import pika
import psycopg2
from jinja2 import Environment, FileSystemLoader
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import NamedTupleCursor

from config import settings

logger = logging.getLogger(__name__)


env = Environment(loader=FileSystemLoader(f"{os.path.dirname(__file__)}/templates"))


@dataclass
class EmailMessageParams:
    to: list[str]
    subject: str
    body: str


class NotificationCategoryV1(Enum):
    service = "service"
    content_updates = "content_updates"
    recommendations = "recommendations"


class NotificationChannelV1(Enum):
    email = "email"
    push = "push"
    sms = "sms"


class NotificationStatusesV1(Enum):
    created = "created"
    processed = "processed"
    error = "error"


CHANNEL_QUEUE_MAP = {NotificationChannelV1.email: "email-channel.v1"}


def make_email_message(to: list[str], template_name: str, variables: dict):
    template = env.get_template(template_name)
    output = template.render(variables)

    message = json.dumps(asdict(EmailMessageParams(to, variables["subject"], output)))
    return message.encode()


def get_conn() -> pg_connection:
    return psycopg2.connect(**settings.pg_connection_params, cursor_factory=NamedTupleCursor)


class TaskService:
    def __init__(self):
        self.pg_conn: pg_connection | None = None
        self.restore_pg_connection()

        self.rabbit_conn = pika.BlockingConnection(pika.ConnectionParameters(settings.rabbit_host))
        self.channel = self.rabbit_conn.channel()
        self.channel.queue_declare(queue=CHANNEL_QUEUE_MAP[NotificationChannelV1.email], durable=True)
        self.channel.exchange_declare(exchange="logs", exchange_type="fanout")

    def __del__(self):
        self.pg_conn.close()
        self.rabbit_conn.close()

    @backoff.on_exception(backoff.expo, (psycopg2.InterfaceError, psycopg2.OperationalError))
    def restore_pg_connection(self):
        if isinstance(self, dict):
            _self: TaskService = self["args"][0]
            _self.pg_conn = get_conn()
        else:
            self.pg_conn = get_conn()

    @backoff.on_exception(
        backoff.expo,
        (psycopg2.InterfaceError, psycopg2.OperationalError),
        on_backoff=restore_pg_connection,
        logger=logger,
    )
    def check_tasks(self):
        with self.pg_conn.cursor() as cur:
            cur.execute(
                f"SELECT * FROM notifications WHERE status ='{NotificationStatusesV1.created.name}'"
                f" AND send_time <= '{datetime.now()}' ORDER BY send_time"
            )
            tasks: list[namedtuple] = cur.fetchall()
        for task in tasks:
            match task.channel:
                case NotificationChannelV1.email.name:
                    self.process_email_task(
                        task.task_id, task.users_ids, task.template_name, task.variables, task.category
                    )

    def process_email_task(
        self, task_id: uuid, users_ids: list[int], template_name: str, variables: dict, category: str
    ):
        users = httpx.post("http://auth:9000/auth/admin/v1/get-users-info", json={"users_ids": users_ids}).json()
        for user in users:
            if category not in user["enabled_notifications"]:
                continue

            variables = variables | user
            body = make_email_message(
                [user["email"]],
                template_name,
                variables,
            )

            self.channel.basic_publish(
                exchange="",
                routing_key=CHANNEL_QUEUE_MAP[NotificationChannelV1.email],
                body=body,
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
            )

            with self.pg_conn.cursor() as cur:
                cur.execute(f"UPDATE notifications SET status='processed' WHERE task_id='{str(task_id)}'")
                self.pg_conn.commit()
