import orjson
from fastapi import Query
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Base(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class IdModel(Base):
    id: str


class Paginated(Base):
    total: int = 0


class Person(IdModel):
    name: str


class Genre(IdModel):
    name: str


class PaginatedParams:
    def __init__(
        self,
        size: int = Query(default=50, alias="page[size]", description="Размер страницы", gt=0, lt=100),
        number: int = Query(default=1, alias="page[number]", description="Номер страницы", gt=0, lt=1000),
    ):
        self.size = size
        self.number = number
