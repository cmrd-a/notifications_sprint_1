import json
import os
from dataclasses import dataclass, asdict
from enum import Enum, auto
import pika
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(f"{os.path.dirname(__file__)}/templates"))


class NotificationCategory(Enum):
    service = auto()
    content_updates = auto()
    recomendations = auto()


@dataclass
class NotificationTableRow:
    notification_id: int
    content_id: int | None
    user_id: int
    category: NotificationCategory


@dataclass
class EmailMessageParams:
    to: list[str]
    subject: str
    body: str


def make_email_message(to: list[str], subject: str, template_name: str, variables: dict = None):
    template = env.get_template(template_name)
    output = template.render(variables)

    message = json.dumps(asdict(EmailMessageParams(to, subject, output)))
    return message.encode()


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='user-reporting.v1.registered', durable=True)
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    #долбимся в таблицу, считываем NotificationTableRow
    # выгребаем все данные по content_id user_id и кидаем их в variables

    message = make_email_message(["sensei-92@yandex.ru"], "subject", "mail.html", {
        "title": "title",
        "text": "text",
        "image": "https://mcusercontent.com/597bc5462e8302e1e9db1d857/images/e27b9f2b-08d3-4736-b9b7"
                 "-96e1c2d387fa.png",
    })

    channel.basic_publish(
        exchange='',
        routing_key='user-reporting.v1.registered',
        body=message,
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
    )
    connection.close()


if __name__ == "__main__":
    main()
