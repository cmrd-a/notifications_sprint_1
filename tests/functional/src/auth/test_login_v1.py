from http import HTTPStatus

import pytest
from settings import settings
from utils.data_gen import gen_email


@pytest.mark.asyncio
async def test_login_v1(make_request):
    # arrange
    email = gen_email()
    await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/register",
        json={"email": email, "password": "password_test_user"},
    )

    # act
    response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/login",
        json={"email": email, "password": "password_test_user"},
    )

    # assert
    assert response.status == HTTPStatus.OK
    assert "access_token" in response.body


@pytest.mark.asyncio
async def test_login_v1__bad_password__return_401(make_request):
    # arrange
    email = gen_email()
    await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/register",
        json={"email": email, "password": "password_test_user"},
    )

    # act
    response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/login",
        json={"email": email, "password": "bad_password_test_user"},
    )

    # assert
    assert response.status == HTTPStatus.UNAUTHORIZED
    assert response.body["message"] == "Bad username or password"
