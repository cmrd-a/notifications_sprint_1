import json
from functools import lru_cache
from uuid import UUID

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from db.kafka_client import get_kafka


class KafkaService:
    def __init__(self, kafka: AIOKafkaProducer):
        self.kafka = kafka

    async def put_film_progress(self, user_id: int, film_id: UUID, film_position_ms: int) -> None:
        await self.kafka.send(
            topic="views",
            value=json.dumps({"film_position_ms": film_position_ms}).encode(),
            key=f"{user_id}+{film_id}".encode(),
        )


@lru_cache
def get_kafka_service(
    kafka: AIOKafkaProducer = Depends(get_kafka),
) -> KafkaService:
    return KafkaService(kafka)
