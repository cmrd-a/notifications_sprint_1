from typing import Optional

from pydantic import BaseModel


class Person(BaseModel):
    """В elastic каждая персона содержит id и full_name."""

    id: str
    name: str


class Genre(BaseModel):
    """В elastic каждый жанр содержит id и full_name."""

    id: str
    name: str


class ElasticMoviesSchemaModel(BaseModel):
    """Модель соответствует схеме индекса movies."""

    id: str
    imdb_rating: float | None = 0.0
    genres: list[Genre] = []
    title: str
    description: Optional[str]
    directors: list[Person] = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    actors: list[Person] = []
    writers: list[Person] = []


class ElasticPersonsSchemaModel(BaseModel):
    """Модель соответствует схеме индекса persons."""

    id: str
    full_name: str


class ElasticGenresSchemaModel(BaseModel):
    """Модель соответствует схеме индекса genres."""

    id: str
    name: str
    description: Optional[str] = ""
