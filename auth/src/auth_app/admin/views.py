from http import HTTPStatus

from apiflask import APIBlueprint, abort
from auth_app.admin.schemas import (
    CreateRoleIn,
    CreateRoleOut,
    DeleteRoleIn,
    ChangeRoleIn,
    GetAllRolesOut,
    SetUserRoleIn,
    GetUsersInfoIn,
    GetUsersInfoOut,
)
from auth_app.db.models import Role, Permission, User
from auth_app.extensions import db
from auth_app.tracing import trace, loging
from auth_app.user.utils import permissions_required
from flask import jsonify, Response
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

blueprint = APIBlueprint("admin", __name__, url_prefix="/auth/admin")


@permissions_required(["manage_users"])
@blueprint.post("/v1/create-role")
@blueprint.input(CreateRoleIn)
@blueprint.output(CreateRoleOut)
@jwt_required()
@blueprint.doc(security="BearerAuth")
@trace
@loging
def create_role(body):
    role_name = body["role_name"]
    role = Role(name=role_name)
    permissions = body["permissions"]

    try:
        for permission in permissions:
            role.permissions.append(db.session().query(Permission).filter(Permission.name == permission).first())
        db.session.add(role)
        db.session.commit()
    except IntegrityError:
        return abort(HTTPStatus.BAD_REQUEST, message=f"Роль {role_name} уже существует.")

    return jsonify(role_id=role.id, role_name=role_name), HTTPStatus.CREATED


@permissions_required(["manage_users"])
@blueprint.delete("/v1/delete-role")
@blueprint.input(DeleteRoleIn)
@jwt_required()
@blueprint.doc(security="BearerAuth")
@trace
@loging
def delete_role(body):
    role_name = body["role_name"]

    try:
        role = db.session().query(Role).filter(Role.name == role_name).first()

        if not role:
            return abort(HTTPStatus.BAD_REQUEST, f"Роль {role_name} не найдена.")

        db.session.delete(role)
        db.session.commit()
    except IntegrityError:
        return abort(HTTPStatus.INTERNAL_SERVER_ERROR, f"Ошибка при удалении роли {role_name}.")

    return Response(status=HTTPStatus.OK)


@permissions_required(["manage_users"])
@blueprint.post("/v1/change-role")
@blueprint.input(ChangeRoleIn)
@jwt_required()
@blueprint.doc(security="BearerAuth")
@trace
@loging
def change_role(body):
    old_role_name = body["old_role_name"]
    new_role_name = body["new_role_name"]
    new_role_permissions = body["new_role_permissions"]

    try:
        old_role = db.session().query(Role).filter(Role.name == old_role_name).first()
        if not old_role:
            return abort(HTTPStatus.BAD_REQUEST, f"Роль {old_role_name} не найдена.")

        old_role_id = old_role.id
        db.session.delete(old_role)
        changed_role = Role(name=new_role_name, id=old_role_id)

        for permission in new_role_permissions:
            changed_role.permissions.append(
                db.session().query(Permission).filter(Permission.name == permission).first()
            )
        db.session.add(changed_role)
        db.session.commit()
    except IntegrityError:
        return abort(HTTPStatus.INTERNAL_SERVER_ERROR, f"Ошибка при изменении роли {old_role_name}.")

    return Response(status=HTTPStatus.OK)


@permissions_required(["manage_users"])
@blueprint.get("/v1/get-all-roles")
@blueprint.doc(security="BearerAuth")
@jwt_required()
@blueprint.output(GetAllRolesOut(many=True))
@trace
@loging
def get_all_roles():
    response = []
    all_roles = db.session().query(Role).all()
    for role in all_roles:
        response.append({"name": role.name, "permissions": [permission.name for permission in role.permissions]})

    return jsonify(response)


@permissions_required(["manage_users"])
@blueprint.post("/v1/set-user-role")
@blueprint.input(SetUserRoleIn)
@jwt_required()
@blueprint.doc(security="BearerAuth")
@trace
@loging
def set_user_role(body):

    user_email = body["email"]
    new_user_role = body["role"]

    try:
        user = db.session().query(User).filter(User.email == user_email).first()
        role = db.session().query(Role).filter(Role.name == new_user_role).first()

        if not user:
            return abort(HTTPStatus.BAD_REQUEST, f"Пользователь с почтой {user_email} не найден.")

        user.role = role

        db.session.add(user)
        db.session.commit()

    except IntegrityError:
        return abort(HTTPStatus.INTERNAL_SERVER_ERROR, f"Ошибка при назначении роли {new_user_role}.")

    return Response(status=HTTPStatus.OK)


@blueprint.post("/v1/get-users-info")
@blueprint.input(GetUsersInfoIn)
@blueprint.output(GetUsersInfoOut(many=True))
@trace
@loging
def get_users_info(body):
    # noinspection PyUnresolvedReferences
    users = db.session().query(User).filter(User.id.in_(body["users_ids"])).all()
    result = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "is_active": user.is_active,
            "role": user.role.name,
            "enabled_notifications": user.enabled_notifications,
        }
        for user in users
    ]

    return jsonify(result)
