import random
from typing import Generator
from uuid import uuid4

from faker import Faker
from models import ElasticMoviesSchemaModel

fake = Faker()


def gen_films(quantity=100) -> Generator[dict, None, None]:
    for _ in range(quantity):
        title = fake.sentence(nb_words=random.randint(1, 10)).title()[:-1]
        doc = ElasticMoviesSchemaModel(id=str(uuid4()), imdb_rating=round(random.uniform(0.0, 10.0), 1), title=title)
        yield {
            "_index": "movies",
            "_source": doc.json(),
        }


def gen_email() -> str:
    return f"{fake.word()}@gmail.com"
