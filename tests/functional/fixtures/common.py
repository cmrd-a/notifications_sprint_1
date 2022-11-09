import asyncio

import aioredis
import pytest_asyncio
from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch
from settings import settings
from testdata.es_indexes import INDEXES
from utils.requests import HTTPResponse, http_request


@pytest_asyncio.fixture(name="redis_client", scope="session")
async def _redis_client():
    redis = await aioredis.from_url(settings.redis_url)
    yield redis
    await redis.close()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="es_client", scope="session")
async def _es_client():
    client = AsyncElasticsearch(hosts=settings.es_url)
    yield client
    await client.close()


@pytest_asyncio.fixture(name="http_session", scope="session")
async def _http_session():
    session = ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(autouse=True)
async def clear_redis_cache(redis_client):
    await redis_client.flushall()
    yield
    await redis_client.flushall()


@pytest_asyncio.fixture(autouse=True)
async def create_indexes(es_client):
    for index, body in INDEXES.items():
        exist = await es_client.indices.exists(index=index)
        if not exist:
            await es_client.indices.create(index=index, **body)

    yield

    for index in INDEXES:
        exist = await es_client.indices.exists(index=index)
        if exist:
            await es_client.indices.delete(index=index)


@pytest_asyncio.fixture
def make_request(http_session):
    async def inner(method: str, url: str, **kwargs) -> HTTPResponse:
        return await http_request(http_session, method, url, **kwargs)

    return inner
