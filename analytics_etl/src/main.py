from uuid import uuid4

import orjson
from clickhouse_driver import Client
from kafka import KafkaConsumer

from logger import get_logger
from settings import setting

logger = get_logger(__name__)


class ETL:
    def __init__(self, kafka_consumer: KafkaConsumer, ch_client: Client):
        self.kafka_consumer = kafka_consumer
        self.ch_client = ch_client

    def transform(self):
        for message in self.kafka_consumer:
            user_id, film_id = message.key.split("+")
            yield str(uuid4()), int(user_id), film_id, message.value["film_position_ms"], message.timestamp

    def load(self):
        for values in self.transform():
            query = f"INSERT INTO movies.views (id, user_id, film_id, film_position_ms, event_dt) VALUES {values}"
            self.ch_client.execute(query)
            self.kafka_consumer.commit()


def main_loop():
    kafka_consumer = KafkaConsumer(
        "views",
        bootstrap_servers=[setting.kafka_server],
        auto_offset_reset="earliest",
        group_id="analytics-etl",
        value_deserializer=orjson.loads,
        key_deserializer=lambda k: k.decode(),
        enable_auto_commit=False,
    )
    ch_client = Client(host=setting.ch_server, user=setting.ch_user, password=setting.ch_password)

    etl = ETL(kafka_consumer, ch_client)
    logger.info("ETL up")
    etl.load()


if __name__ == "__main__":
    main_loop()
