from apiflask import Schema
from apiflask.fields import String, Email, DateTime, IP, Integer, List
from apiflask.validators import Length

password_validator = Length(8, 128)


class EmailPasswordIn(Schema):
    email = Email(required=True)
    password = String(required=True, validate=password_validator)


class LoginRefreshOut(Schema):
    access_token = String()
    refresh_token = String()


class ChangePasswordIn(Schema):
    current_password = String(required=True, validate=password_validator)
    new_password = String(required=True, validate=password_validator)


class LoginHistoryOut(Schema):
    ip_address = IP()
    login_time = DateTime()


class LoginHistoryIn(Schema):
    page_number = Integer(load_default=1)
    page_size = Integer(load_default=100)


class GetPermissionsOut(Schema):
    permissions = List(String)
