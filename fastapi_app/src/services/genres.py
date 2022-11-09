from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.api_models import GenreDescripted, GenresDescripted
from services.common import ElasticService, RedisCache, Cache


class GenresService(ElasticService):
    def __init__(self, cache: Cache, elastic: AsyncElasticsearch):
        self.cache = cache
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> GenreDescripted | None:
        cache_key = f"genres::genre_id::{genre_id}"
        genre = await self.cache.get(cache_key, GenreDescripted)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return
            await self.cache.put(cache_key, genre)

        return genre

    async def get_list(self) -> GenresDescripted | None:
        genres = await self.cache.get("genres", GenresDescripted)

        if not genres:
            resp = await self.elastic.search(index="genres", size=999)
            total, hits = self.get_total_and_hits(resp)

            if not hits:
                return

            _genres = [GenreDescripted(**hit["_source"]) for hit in hits]
            genres = GenresDescripted(genres=_genres)
            await self.cache.put("genres", genres)

        return genres

    async def _get_genre_from_elastic(self, genre_id: str) -> GenreDescripted | None:
        try:
            doc = await self.elastic.get(index="genres", id=genre_id)
        except NotFoundError:
            return
        return GenreDescripted(**doc.body["_source"])


@lru_cache()
def get_genres_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenresService:
    return GenresService(RedisCache(redis), elastic)
