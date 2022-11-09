from http import HTTPStatus

import pytest
from settings import settings


@pytest.mark.asyncio
async def test_register_v1(make_request):
    # act
    response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/register",
        json={"email": "test_user@gmail.com", "password": "password_test_user"},
    )

    # assert
    assert response.status == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_register_v1__short_password__return_status_400(make_request):
    # act
    response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/register",
        json={"email": "user@gmail.com", "password": "user"},
    )

    # assert
    assert response.body["detail"]["json"]["password"][0] == "Length must be between 8 and 128."
    assert response.status == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_register_v1__existent_email__return_status_400(make_request):
    # arrange
    await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/register",
        json={"email": "existent_user@gmail.com", "password": "test_user"},
    )

    # act
    response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/register",
        json={"email": "existent_user@gmail.com", "password": "test_user"},
    )

    # assert
    assert response.body["message"] == "Bad username or password"
    assert response.status == HTTPStatus.BAD_REQUEST
