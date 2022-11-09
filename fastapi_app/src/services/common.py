from abc import ABC, abstractmethod
from typing import Type, TypeVar

from aioredis import Redis
from elastic_transport import ObjectApiResponse
from elasticsearch import AsyncElasticsearch

from core.config import config
from models.common import Base

BaseTypeVar = TypeVar("BaseTypeVar", bound=Base)


class Cache(ABC):
    @property
    @abstractmethod
    def cache_expire_in_seconds(self):
        ...

    @abstractmethod
    async def put(self, key: str, obj: BaseTypeVar):
        ...

    @abstractmethod
    async def get(self, key: str, model: Type[BaseTypeVar]) -> BaseTypeVar | None:
        ...


class RedisCache(Cache):
    def __init__(self, redis: Redis):
        self.redis = redis
        self._cache_expire_in_seconds = config.redis_cache_expire_in_seconds

    @property
    def cache_expire_in_seconds(self):
        return self._cache_expire_in_seconds

    async def put(self, key: str, obj: BaseTypeVar):
        await self.redis.set(key, obj.json(), ex=self.cache_expire_in_seconds)

    async def get(self, key: str, model: Type[BaseTypeVar]) -> BaseTypeVar | None:
        data = await self.redis.get(key)
        if not data:
            return

        parsed_data = model.parse_raw(data)
        return parsed_data


class ElasticService(ABC):
    cache: Cache
    elastic: AsyncElasticsearch

    @staticmethod
    def get_total_and_hits(resp: ObjectApiResponse) -> (int, list):
        _hits = resp.body.get("hits", {})
        total = _hits["total"]["value"]
        hits = _hits.get("hits", [])
        return total, hits
