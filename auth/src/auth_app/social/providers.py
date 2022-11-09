import json
from abc import ABC, abstractmethod

import requests
from auth_app.user.utils import get_or_create_user, create_tokens
from flask import current_app
from oauthlib.oauth2 import WebApplicationClient


class AuthProvide(ABC):
    @abstractmethod
    def login(self, request) -> str:
        ...

    @abstractmethod
    def callback(self, request) -> dict | None:
        ...

    @staticmethod
    def get_callback_resp(email: str, social_id: str, name: str) -> dict:
        user, raw_password = get_or_create_user(email, social_id, name)
        response = create_tokens(user)
        if raw_password:
            response["password_to_change"] = raw_password
        return response


class GoogleOAuth(AuthProvide):
    @staticmethod
    def get_google_provider_cfg() -> dict:
        return requests.get(current_app.config["GOOGLE_DISCOVERY_URL"]).json()

    def login(self, request) -> str:
        google_provider_cfg = self.get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        client = WebApplicationClient(current_app.config["GOOGLE_CLIENT_ID"])
        return client.prepare_request_uri(  # noqa
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )

    def callback(self, request) -> dict | None:
        code = request.args.get("code")
        google_provider_cfg = self.get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        client = WebApplicationClient(current_app.config["GOOGLE_CLIENT_ID"])
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(current_app.config["GOOGLE_CLIENT_ID"], current_app.config["GOOGLE_CLIENT_SECRET"]),
        )
        client.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body).json()

        if not userinfo_response.get("email_verified"):
            return

        return self.get_callback_resp(
            userinfo_response["email"], userinfo_response["sub"], userinfo_response["given_name"]
        )
