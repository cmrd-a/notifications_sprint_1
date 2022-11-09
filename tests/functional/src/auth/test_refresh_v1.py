from http import HTTPStatus

import pytest
from settings import settings
from utils.data_gen import gen_email


@pytest.mark.asyncio
async def test_refresh_v1(make_request):
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
    refresh_token = login_response.body.get("refresh_token")

    # act
    refresh_response = await make_request(
        "POST",
        f"{settings.flask_url}/users/v1/refresh",
        headers={"authorization": f"Bearer {refresh_token}"},
    )
    access_token = refresh_response.body["access_token"]
    login_history_response = await make_request(
        "GET",
        f"{settings.flask_url}/users/v1/login-history",
        headers={"authorization": f"Bearer {access_token}"},
    )

    # assert
    assert refresh_response.status == HTTPStatus.OK
    assert "access_token" in refresh_response.body
    assert login_history_response.status == HTTPStatus.OK
    assert "ip_address" in login_history_response.body[0]
    assert "login_time" in login_history_response.body[0]
