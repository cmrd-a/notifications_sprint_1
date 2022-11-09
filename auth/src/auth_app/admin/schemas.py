from apiflask import Schema
from apiflask.fields import String, List, Integer, Nested, Email


class CreateRoleIn(Schema):
    role_name = String(required=True)
    permissions = List(String(required=True))


class CreateRoleOut(Schema):
    role_id = Integer(required=True)
    role_name = String(required=True)


class DeleteRoleIn(Schema):
    role_name = String(required=True)


class ChangeRoleIn(Schema):
    old_role_name = String(required=True)
    new_role_name = String(required=True)
    new_role_permissions = List(String(required=True))


class Permissions(Schema):
    name = String(required=True)


class GetAllRolesOut(Schema):
    name = String(required=True)
    permissions = List(Nested(Permissions))


class SetUserRoleIn(Schema):
    email = Email(required=True)
    role = String(required=True)
