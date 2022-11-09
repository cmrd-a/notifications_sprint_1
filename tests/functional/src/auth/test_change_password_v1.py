from http import HTTPStatus

import pytest
from settings import settings
from utils.data_gen import gen_email


@pytest.mark.asyncio
async def test_change_password_v1(make_request):
    # arrange
    email = gen_email()
    await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/register",
        json={"email": email, "password": "password_test_user"},
    )
    login_response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/login",
        json={"email": email, "password": "password_test_user"},
    )

    # act
    change_password_response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/change-password",
        headers={"authorization": f"Bearer {login_response.body.get('access_token')}"},
        json={"current_password": "password_test_user", "new_password": "changed_test_user"},
    )
    login_response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/login",
        json={"email": email, "password": "changed_test_user"},
    )

    # assert
    assert change_password_response.status == HTTPStatus.NO_CONTENT
    assert login_response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_change_password_v1__bad_password__return_status_400(make_request):
    # arrange
    email = gen_email()
    await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/register",
        json={"email": email, "password": "password_test_user"},
    )
    login_response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/login",
        json={"email": email, "password": "password_test_user"},
    )

    # act
    change_password_response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/change-password",
        headers={"authorization": f"Bearer {login_response.body.get('access_token')}"},
        json={"current_password": "wrong_password_test_user", "new_password": "changed_test_user"},
    )

    # assert
    assert change_password_response.status == HTTPStatus.BAD_REQUEST
    assert change_password_response.body["message"] == "Bad Request"


@pytest.mark.asyncio
async def test_change_password_v1__refresh_access_token__return_status_401(make_request):
    # arrange
    email = gen_email()
    await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/register",
        json={"email": email, "password": "password_test_user"},
    )
    login_response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/login",
        json={"email": email, "password": "password_test_user"},
    )
    refresh_response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/refresh",
        headers={"authorization": f"Bearer {login_response.body.get('refresh_token')}"},
    )
    access_token = refresh_response.body.get("access_token")

    # act
    change_password_response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/change-password",
        headers={"authorization": f"Bearer {access_token}"},
        json={"current_password": "password_test_user", "new_password": "new_password"},
    )

    # assert
    assert change_password_response.status == HTTPStatus.UNAUTHORIZED
    assert change_password_response.body["msg"] == "Fresh token required"
