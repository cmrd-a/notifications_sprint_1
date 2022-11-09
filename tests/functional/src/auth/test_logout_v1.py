from http import HTTPStatus

import pytest
from settings import settings
from utils.data_gen import gen_email


@pytest.mark.asyncio
async def test_logout_v1(make_request):
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
    access_token = login_response.body.get("access_token")

    # act
    logout_response = await make_request(
        "DELETE",
        f"{settings.flask_url}/users/v1/logout",
        headers={"authorization": f"Bearer {access_token}"},
    )
    login_history_response = await make_request(
        "GET",
        f"{settings.flask_url}/users/v1/login-history",
        headers={"authorization": f"Bearer {access_token}"},
    )

    # assert
    assert logout_response.status == HTTPStatus.OK
    assert logout_response.body["msg"] == "Access token successfully revoked"
    assert login_history_response.status == HTTPStatus.UNAUTHORIZED
    assert login_history_response.body["msg"] == "Token has been revoked"
