import json
import logging
import os
import time
from dataclasses import dataclass, asdict
from enum import Enum, auto
from config import settings
import pika
from jinja2 import Environment, FileSystemLoader

from pg_service import PostgresService

env = Environment(loader=FileSystemLoader(f"{os.path.dirname(__file__)}/templates"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NotificationChannelV1(Enum):
    email = auto()
    push = auto()
    sms = auto()


@dataclass
class EmailMessageParams:
    to: list[str]
    subject: str
    body: str


def make_email_message(to: list[str], template_name: str, variables: dict):
    template = env.get_template(template_name)
    output = template.render(variables)

    message = json.dumps(asdict(EmailMessageParams(to, variables["subject"], output)))
    return message.encode()


CHANNEL_QUEUE_MAP = {NotificationChannelV1.email: "email-channel.v1"}


def main():
    rabbit_conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = rabbit_conn.channel()

    channel.queue_declare(queue="user-reporting.v1.registered", durable=True)
    channel.exchange_declare(exchange="logs", exchange_type="fanout")

    # долбимся в таблицу, считываем NotificationTableRow
    # выгребаем все данные по content_id user_id и кидаем их в variables

    message = make_email_message(
        ["sensei-92@yandex.ru"],
        "mail.html",
        {
            "subject": "тема письма",
            "title": "title",
            "text": "text",
            "image": "https://mcusercontent.com/597bc5462e8302e1e9db1d857/images/e27b9f2b-08d3-4736-b9b7"
            "-96e1c2d387fa.png",
        },
    )

    channel.basic_publish(
        exchange="",
        routing_key="user-reporting.v1.registered",
        body=message,
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
    )
    rabbit_conn.close()


if __name__ == "__main__":
    svc = PostgresService()
    while True:
        logger.debug("start iter")
        svc.check_tasks()
        time.sleep(settings.polling_frequency)
