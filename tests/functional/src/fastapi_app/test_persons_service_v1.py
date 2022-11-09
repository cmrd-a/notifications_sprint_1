from http import HTTPStatus

import pytest
from settings import settings


@pytest.mark.asyncio
async def test_person_by_id__person_present__return_person(make_request, create_persons, create_movies):
    # arrange
    expected_result = {
        "id": "1",
        "full_name": "Pablo Escobar",
        "roles": [
            {"role": "actor", "films_details": [{"id": "1", "title": "Test film 1 title", "imdb_rating": 1.5}]},
            {"role": "writer", "films_details": [{"id": "4", "title": "Test film 4 title", "imdb_rating": 6.5}]},
        ],
    }

    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/persons/1")

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_person_by_id__no_person__return_status_404(make_request, create_persons, create_movies):
    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/persons/100")

    # assert
    assert response.body["detail"] == "person not found"
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_film_details_by_person__films_present__return_details(make_request, create_persons, create_movies):
    # arrange
    expected_result = {
        "films": [
            {"id": "1", "title": "Test film 1 title", "imdb_rating": 1.5},
            {"id": "4", "title": "Test film 4 title", "imdb_rating": 6.5},
        ]
    }

    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/persons/1/film")

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_film_details_by_person__no_films__return_status_404(make_request, create_persons, create_movies):
    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/persons/100/film")

    # assert
    assert response.body["detail"] == "film details not found"
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_persons_search__person_present__return_persons(make_request, create_persons, create_movies):
    # arrange
    expected_result = {
        "total": 3,
        "persons_with_films": [
            {
                "id": "9",
                "full_name": "Igor Rastvorov",
                "roles": [
                    {
                        "role": "actor",
                        "films_details": [
                            {"id": "2", "title": "Test film 2 title", "imdb_rating": 3.5},
                            {"id": "1", "title": "Test film 1 title", "imdb_rating": 1.5},
                            {"id": "3", "title": "Test film 3 title", "imdb_rating": 5.5},
                            {"id": "4", "title": "Test film 4 title", "imdb_rating": 6.5},
                        ],
                    },
                    {
                        "role": "writer",
                        "films_details": [{"id": "2", "title": "Test film 2 title", "imdb_rating": 3.5}],
                    },
                    {
                        "role": "director",
                        "films_details": [{"id": "5", "title": "Test film 5 title", "imdb_rating": 7.5}],
                    },
                ],
            },
            {
                "id": "11",
                "full_name": "Igor Presnyakov",
                "roles": [
                    {"role": "writer", "films_details": [{"id": "1", "title": "Test film 1 title", "imdb_rating": 1.5}]}
                ],
            },
            {
                "id": "12",
                "full_name": "Igor Net",
                "roles": [
                    {"role": "writer", "films_details": [{"id": "4", "title": "Test film 4 title", "imdb_rating": 6.5}]}
                ],
            },
        ],
    }

    # act
    response = await make_request("GET", f"{settings.fastapi_url}/api/v1/persons/search", params={"query": "Igor"})

    # assert
    assert response.body == expected_result


@pytest.mark.asyncio
async def test_persons_search__no_persons__return_status_404(make_request, create_persons, create_movies):
    # act
    response = await make_request(
        "GET", f"{settings.fastapi_url}/api/v1/persons/search", params={"query": "Korpiklaani"}
    )

    # assert
    assert response.body["detail"] == "persons not found"
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize("page_size", (1, 2, 3))
async def test_persons_search__send_page_size__return_correct_lens(
    make_request, create_persons, create_movies, page_size
):
    response = await make_request(
        "GET",
        f"{settings.fastapi_url}/api/v1/persons/search",
        params={"query": "Igor", "page[size]": page_size},
    )

    assert response.status == HTTPStatus.OK
    assert len(response.body["persons_with_films"]) == page_size
