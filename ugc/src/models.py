from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Base(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmUserModel(Base):
    film_id: UUID
    user_id: int


class Rating(FilmUserModel):
    rating: int


class FilmUserOptionalModel(Base):
    film_id: UUID | None = None
    user_id: int | None = None


class Review(FilmUserModel):
    review: str


class Bookmark(FilmUserModel):
    ...
