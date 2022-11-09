import datetime
import random
from datetime import datetime
from uuid import uuid4
import json
from matplotlib import pyplot
from pymongo import MongoClient, ASCENDING
from elasticsearch import Elasticsearch
from logger import logger
from elasticsearch.helpers import bulk


USERS_COUNT = 300_000
REACTIONS_COUNT = 10_000
FILMS_COUNT = 30_000
FIND_ONE_OPERATIONS_COUNT = 100
INSERT_MANY_OPERATIONS_COUNT = 150
GENERATE_CHUNK_SIZE = 100
TEST = "elastic"


if TEST == "elastic":
    es = Elasticsearch("http://localhost:9200")
    if not es.indices.exists(index="test-index"):
        es.indices.create(index="test-index")
else:
    mongo = MongoClient("mongodb://localhost:27017/")
    db = mongo.test_database
    films_with_reactions = db.films_with_reactions
    films_with_reactions.create_index([("film_id", ASCENDING)])


def generate_users_ids(users_count=USERS_COUNT):
    logger.info("Генерация id пользователей...")
    return [str(uuid4()) for _ in range(users_count)]


def generate_reactions(users_ids, reactions_count=REACTIONS_COUNT):
    logger.info("Генерация реакций пользователей...")
    return [uuid for uuid in random.sample(users_ids, k=random.randint(1, reactions_count))]


def generate_films_ids(films_count=FILMS_COUNT):
    logger.info("Генерация id фильмов...")
    return [str(uuid4()) for _ in range(films_count)]


def generate_film_with_reactions(users_ids, films_ids):
    return {
        "film_id": random.choice(films_ids),
        "likes": generate_reactions(users_ids),
        "dislikes": generate_reactions(users_ids),
    }


def generate_average_films_rating(users_ids, films_ids):
    logger.info("Генерация фильмов со средним рейтингом...")
    likes = generate_reactions(users_ids)
    dislikes = generate_reactions(users_ids)
    return {
        "film_id": random.choice(films_ids),
        "user_id": random.choice(users_ids),
        "created": datetime.now(),
        "rating": (len(likes) / (len(likes) + len(dislikes))) * 10,
    }


def generate_films_with_reactions_chunk(users_ids, films_ids, chunk_size=GENERATE_CHUNK_SIZE):
    logger.info(f"Генерация чанка фильмов с реакциями пользователей длиной {chunk_size}...")
    return [generate_film_with_reactions(users_ids, films_ids) for _ in range(chunk_size)]


def generate_average_films_ratings_chunk(users_ids, films_ids, chunk_size=GENERATE_CHUNK_SIZE):
    logger.info(f"Генерация чанка фильмов с реакциями пользователей длиной {chunk_size}...")
    return [generate_average_films_rating(users_ids, films_ids) for _ in range(chunk_size)]


def insertion_films_with_reactions_test(users_ids, films_ids, data_chunks_count=INSERT_MANY_OPERATIONS_COUNT):
    saved_films_ids = []
    plot_coordinates = {"x": [], "y": []}
    logger.info(f"Тестирование вставки данных, будет {data_chunks_count} операций insert...")
    for step in range(data_chunks_count):
        films_with_reactions_chunk = generate_films_with_reactions_chunk(users_ids, films_ids)
        actions = []
        for film in films_with_reactions_chunk:
            saved_films_ids.append(film["film_id"])

            if TEST == "elastic":
                actions.append(
                    {
                        "_index": "test-index",
                        "_id": film["film_id"],
                        "_source": json.dumps(film),
                    }
                )

        logger.info(f"Вставка чанка размером {len(films_with_reactions_chunk)}, операция № {step}...")

        start = datetime.now()
        if TEST == "elastic":
            bulk(actions=actions, client=es)
        else:
            films_with_reactions.insert_many(films_with_reactions_chunk)
        time_delta = datetime.now() - start

        plot_coordinates["x"].append(step)
        plot_coordinates["y"].append(time_delta.total_seconds())

    return saved_films_ids, plot_coordinates


def get_films_with_reactions_test(films_ids, operations_count=FIND_ONE_OPERATIONS_COUNT):
    plot_coordinates = {"x": [], "y": []}
    logger.info(f"Тестирование получения данных, будет выполнено {operations_count} операций find_one...")
    for step in range(operations_count):
        film_id = random.choice(films_ids)

        logger.info(f"Получение данных, операция № {step}...")
        start = datetime.now()
        if TEST == "elastic":
            es.get(index="test-index", id=film_id)
        else:
            films_with_reactions.find_one({"film_id": film_id})
        time_delta = datetime.now() - start

        plot_coordinates["x"].append(step)
        plot_coordinates["y"].append(time_delta.total_seconds())

    return plot_coordinates


def draw_plot(title, x_label, y_label, x, y):
    logger.info(f"Построение графика: {title}")
    pyplot.title(title)
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.plot(x, y)
    pyplot.show()


if __name__ == "__main__":
    users_uuids = generate_users_ids()
    films_uuids = generate_films_ids()
    saved_films_uuids, plot_data = insertion_films_with_reactions_test(users_uuids, films_uuids)
    if TEST == "elastic":
        insert_data_plot_title = "Вставка данных в elasticsearch"
        get_data_plot_title = "Получение строки из elasticsearch"
    else:
        insert_data_plot_title = "Вставка данных в mongodb"
        get_data_plot_title = "Получение строки из mongodb"

    draw_plot(
        title=insert_data_plot_title,
        x_label="Операция вставки №",
        y_label="Время, c",
        x=plot_data["x"],
        y=plot_data["y"],
    )

    plot_data = get_films_with_reactions_test(saved_films_uuids)
    draw_plot(
        title=get_data_plot_title,
        x_label="Операция получения строки №",
        y_label="Время, c",
        x=plot_data["x"],
        y=plot_data["y"],
    )
