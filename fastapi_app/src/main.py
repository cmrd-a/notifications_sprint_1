import logging

import aioredis
import sentry_sdk
import uvicorn as uvicorn
from aiokafka import AIOKafkaProducer
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons, analytics
from core.config import config
from core.logger import LOGGING
from db import elastic, redis, kafka_client

app = FastAPI(
    title=config.project_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis.redis = await aioredis.from_url(config.redis_url)
    elastic.es = AsyncElasticsearch(hosts=[f"{config.es_host}:{config.es_port}"])
    kafka_client.kafka = AIOKafkaProducer(bootstrap_servers=[config.kafka_server])
    if config.sentry_enabled:
        sentry_sdk.init(dsn=config.sentry_dsn)


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()
    await kafka_client.kafka.stop()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.INFO,
    )
