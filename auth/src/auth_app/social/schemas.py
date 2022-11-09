from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import OneOf


class ProviderIn(Schema):
    provider = String(required=True, validate=OneOf(["google"]))


class CallbackOut(Schema):
    access_token = String(required=True)
    refresh_token = String(required=True)
    password_to_change = String()
