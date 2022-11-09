import json

import pytest_asyncio
from elasticsearch.helpers import async_bulk
from testdata.genres import genres
from testdata.movies import movies
from testdata.persons import persons
from utils.data_gen import gen_films


@pytest_asyncio.fixture()
async def create_films(es_client):
    async def inner(quantity=1000):
        return await async_bulk(client=es_client, actions=gen_films(quantity), refresh=True)

    return inner


@pytest_asyncio.fixture()
async def create_genres(es_client):
    actions = [
        {
            "_index": "genres",
            "_id": genre["id"],
            "_source": json.dumps(genre),
        }
        for genre in genres
    ]

    await async_bulk(client=es_client, actions=actions, refresh=True)


@pytest_asyncio.fixture()
async def create_persons(es_client):
    actions = [
        {
            "_index": "persons",
            "_id": person["id"],
            "_source": json.dumps(person),
        }
        for person in persons
    ]

    await async_bulk(client=es_client, actions=actions, refresh=True)


@pytest_asyncio.fixture()
async def create_movies(es_client):
    actions = [
        {
            "_index": "movies",
            "_id": movie["id"],
            "_source": json.dumps(movie),
        }
        for movie in movies
    ]

    await async_bulk(client=es_client, actions=actions, refresh=True)
