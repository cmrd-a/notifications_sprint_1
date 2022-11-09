from aiokafka import AIOKafkaProducer

kafka: AIOKafkaProducer | None = None


async def get_kafka() -> AIOKafkaProducer:
    return kafka
