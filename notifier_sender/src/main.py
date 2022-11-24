import json
import os
import sys

import pika

from email_service import EmailService, EmailMessageParams
from config import settings

email_service = None


def send_email(ch, method, properties, body: bytes):
    message_params = EmailMessageParams(**json.loads(body))
    email_service.send_message(message_params)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(settings.rabbit_host))
    channel = connection.channel()

    result = channel.queue_declare(queue="email-channel.v1", durable=True)
    # result = channel.queue_declare(queue='', exclusive=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=result.method.queue, on_message_callback=send_email)
    channel.start_consuming()


if __name__ == "__main__":
    email_service = EmailService()
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        del email_service
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)  # noqa
