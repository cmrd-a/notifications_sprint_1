import json
from http import HTTPStatus

import pytest
from settings import settings


@pytest.mark.asyncio
@pytest.mark.parametrize("page_size", (1, 2, 50, 99))
async def test_films_list__page_size_parameter__return_correct_result(create_films, make_request, page_size):
    # arrange
    await create_films(100)

    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/films", params={"page[size]": page_size})

    # assert
    assert response.status == HTTPStatus.OK
    assert len(response.body["results"]) == page_size


@pytest.mark.asyncio
async def test_films_list__sort_by_rating__return_correct_films(create_movies, make_request):
    # arrange
    expected_result = {
        "total": 6,
        "results": [
            {"id": "1", "title": "Test film 1 title", "imdb_rating": 1.5},
            {"id": "2", "title": "Test film 2 title", "imdb_rating": 3.5},
            {"id": "3", "title": "Test film 3 title", "imdb_rating": 5.5},
            {"id": "4", "title": "Test film 4 title", "imdb_rating": 6.5},
            {"id": "5", "title": "Test film 5 title", "imdb_rating": 7.5},
            {"id": "6", "title": "Original name", "imdb_rating": 8.5},
        ],
    }

    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/films", params={"sort": "imdb"})

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_films_list__filter_by_genre__return_correct_films(create_movies, make_request):
    # arrange
    expected_result = {"total": 1, "results": [{"id": "4", "title": "Test film 4 title", "imdb_rating": 6.5}]}

    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/films", params={"filter[genre]": "4"})

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_films_list__get_model_from_cash__return_correct_films(create_movies, make_request, redis_client):
    # arrange
    redis_key = (
        "movies::search_str::None::sort::None::filter_genre::"
        "None::filter_person::None::page_size::50::page_number::1"
    )
    expected_result = {
        "total": 6,
        "results": [
            {
                "id": "1",
                "title": "Test film 1 title",
                "description": "test description",
                "imdb_rating": 1.5,
                "genres": [{"id": "1", "name": "action"}],
                "actors_names": ["Pablo", "Victor"],
                "writers_names": [],
                "writers": [{"id": "11", "name": "Igor Presnyakov"}],
                "actors": [
                    {"id": "1", "name": "Pablo Escobar"},
                    {"id": "2", "name": "Victor Andrey"},
                    {"id": "9", "name": "Igor Rastvorov"},
                ],
                "directors": [],
            },
            {
                "id": "2",
                "title": "Test film 2 title",
                "description": "test description",
                "imdb_rating": 3.5,
                "genres": [{"id": "2", "name": "for_adults"}],
                "actors_names": ["Igor", "Jessica"],
                "writers_names": [],
                "writers": [{"id": "9", "name": "Igor Rastvorov"}],
                "actors": [{"id": "9", "name": "Igor Rastvorov"}, {"id": "10", "name": "Jessica Secretic"}],
                "directors": [],
            },
            {
                "id": "3",
                "title": "Test film 3 title",
                "description": "test description",
                "imdb_rating": 5.5,
                "genres": [{"id": "3", "name": "cartoons"}],
                "actors_names": [],
                "writers_names": [],
                "writers": [],
                "actors": [{"id": "9", "name": "Igor Rastvorov"}],
                "directors": [],
            },
            {
                "id": "4",
                "title": "Test film 4 title",
                "description": "test description",
                "imdb_rating": 6.5,
                "genres": [{"id": "4", "name": "horror"}],
                "actors_names": ["Boris"],
                "writers_names": ["Pablo", "Boris"],
                "writers": [
                    {"id": "1", "name": "Pablo Escobar"},
                    {"id": "4", "name": "Boris Britva"},
                    {"id": "12", "name": "Igor Net"},
                ],
                "actors": [{"id": "4", "name": "Boris Britva"}, {"id": "9", "name": "Igor Rastvorov"}],
                "directors": [{"id": "4", "name": "Boris Britva"}],
            },
            {
                "id": "5",
                "title": "Test film 5 title",
                "description": "test description",
                "imdb_rating": 7.5,
                "genres": [{"id": "5", "name": "comedy"}],
                "actors_names": ["Sherlock", "Inna"],
                "writers_names": ["Black", "Nicol"],
                "writers": [{"id": "7", "name": "Black Master"}, {"id": "8", "name": "Nicol Burateeno"}],
                "actors": [{"id": "5", "name": "Sherlock Holmes"}, {"id": "6", "name": "Inna Druz"}],
                "directors": [{"id": "3", "name": "Evil Cat"}, {"id": "9", "name": "Igor Rastvorov"}],
            },
            {
                "id": "6",
                "title": "Original name",
                "description": "test description",
                "imdb_rating": 8.5,
                "genres": [{"id": "5", "name": "comedy"}],
                "actors_names": ["Sherlock", "Inna"],
                "writers_names": ["Black", "Nicol"],
                "writers": [{"id": "7", "name": "Black Master"}, {"id": "8", "name": "Nicol Burateeno"}],
                "actors": [{"id": "6", "name": "Inna Druz"}],
                "directors": [{"id": "3", "name": "Evil Cat"}],
            },
        ],
    }

    # act
    await make_request("GET", f"{settings.fastapi_url}/api/v1/films")
    result = await redis_client.get(redis_key)

    # assert
    assert json.loads(result.decode()) == expected_result


@pytest.mark.asyncio
async def test_films_list__filter_by_person__return_correct_films(create_movies, make_request):
    # arrange
    expected_result = {"total": 1, "results": [{"id": "2", "title": "Test film 2 title", "imdb_rating": 3.5}]}

    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/films", params={"filter[person]": "10"})

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_films_list__no_films__return_status_404(make_request):
    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/films")

    # assert
    assert response.body["detail"] == "films not found"
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_films_search__search_by_title__return_correct_films(create_movies, make_request):
    # arrange
    expected_result = {"total": 1, "results": [{"id": "6", "title": "Original name", "imdb_rating": 8.5}]}

    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/films/search", params={"query": "original"})

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_films_search__no_films__return_status_404(create_movies, make_request):
    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/films/search", params={"query": "korpiklaani"})

    # assert
    assert response.body["detail"] == "films not found"
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize("page_size", (1, 2, 3))
async def test_films_search__send_page_size__return_correct_lens(make_request, create_movies, page_size):
    response = await make_request(
        "GET",
        f"{settings.fastapi_url}/api/v1/films/search",
        params={"query": "test", "page[size]": page_size},
    )

    assert response.status == HTTPStatus.OK
    assert len(response.body["results"]) == page_size


@pytest.mark.asyncio
async def test_film_details__search_by_title__return_correct_film(create_movies, make_request):
    # arrange
    expected_result = {
        "id": "1",
        "title": "Test film 1 title",
        "imdb_rating": 1.5,
        "description": "test description",
        "genres": [{"id": "1", "name": "action"}],
        "actors": [
            {"id": "1", "name": "Pablo Escobar"},
            {"id": "2", "name": "Victor Andrey"},
            {"id": "9", "name": "Igor Rastvorov"},
        ],
        "writers": [{"id": "11", "name": "Igor Presnyakov"}],
        "directors": [],
    }

    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/films/1")

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_film_details__no_film__return_status_404(create_movies, make_request):
    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/films/100")

    # assert
    assert response.body["detail"] == "film not found"
    assert response.status == HTTPStatus.NOT_FOUND
