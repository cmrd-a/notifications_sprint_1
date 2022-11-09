from enum import Enum
from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.es_models import Film, Films
from services.common import ElasticService, RedisCache, Cache


class ApiSortOptions(str, Enum):
    rating_asc = "imdb"
    rating_desc = "-imdb"


ELASTIC_SORT_MAP = {
    ApiSortOptions.rating_asc: {"imdb_rating": {"order": "asc"}},
    ApiSortOptions.rating_desc: {"imdb_rating": {"order": "desc"}},
}


class FilmService(ElasticService):
    def __init__(self, cache: Cache, elastic: AsyncElasticsearch):
        self.cache = cache
        self.elastic = elastic

    async def get_film(self, film_id: str) -> Film | None:
        cache_key = f"movies::film_id::{film_id}"
        film = await self.cache.get(cache_key, Film)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return
            await self.cache.put(cache_key, film)

        return film

    async def get_films(
        self,
        search_str: str = None,
        sort: ApiSortOptions = None,
        filter_genre: str = None,
        filter_person: str = None,
        page_size: int = 50,
        page_number: int = 1,
    ) -> Films | None:
        redis_key = (
            f"movies::search_str::{search_str}::sort::{sort}::filter_genre::{filter_genre}::filter_person"
            f"::{filter_person}::page_size::{page_size}::page_number::{page_number}"
        )
        films = await self.cache.get(redis_key, Films)
        if not films:
            films = await self._get_films_from_elastic(
                search_str, sort, filter_genre, filter_person, page_size, page_number
            )
            if not films:
                return

            await self.cache.put(redis_key, films)
        return films

    async def _get_film_from_elastic(self, film_id: str) -> Film | None:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return
        return Film(**doc.body["_source"])

    async def _get_films_from_elastic(
        self,
        search_str: str = None,
        sort: ApiSortOptions = None,
        filter_genre: str = None,
        filter_person: str = None,
        page_size: int = 50,
        page_number: int = 1,
    ) -> Films | None:
        filters = []
        if filter_genre:
            filters.append(
                {"nested": {"path": "genres", "query": {"bool": {"must": {"term": {"genres.id": filter_genre}}}}}}
            )
        if filter_person:
            filters.append(
                {
                    "bool": {
                        "should": [
                            {
                                "nested": {
                                    "path": "actors",
                                    "query": {"bool": {"must": {"term": {"actors.id": filter_person}}}},
                                }
                            },
                            {
                                "nested": {
                                    "path": "writers",
                                    "query": {"bool": {"must": {"term": {"writers.id": filter_person}}}},
                                }
                            },
                            {
                                "nested": {
                                    "path": "directors",
                                    "query": {"bool": {"must": {"term": {"directors.id": filter_person}}}},
                                }
                            },
                        ]
                    }
                }
            )
        query = None
        if search_str:
            query = {"multi_match": {"query": search_str, "fields": ["title^10", "description"]}}
        if filters:
            query = {"bool": {"must": filters}}
        resp = await self.elastic.search(
            index="movies",
            query=query,
            sort=ELASTIC_SORT_MAP[sort] if sort else None,
            size=page_size,
            from_=(page_number - 1) * page_size if page_number > 1 else 0,
        )
        total, hits = self.get_total_and_hits(resp)
        if not hits:
            return
        results = [Film(**hit["_source"]) for hit in hits]
        return Films(total=total, results=results)


@lru_cache
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(RedisCache(redis), elastic)
