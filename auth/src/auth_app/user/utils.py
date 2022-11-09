import secrets
import string
from functools import wraps
from http import HTTPStatus

from apiflask import abort
from auth_app.db.models import User, Role
from auth_app.extensions import db, redis_client, jwt
from flask_jwt_extended import create_access_token, create_refresh_token, verify_jwt_in_request, get_jwt


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token_in_redis = redis_client.get(jti)
    return token_in_redis is not None


def permissions_required(permisssions: [str]):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if set(permisssions) & set(claims["permissions"]):
                return fn(*args, **kwargs)
            else:
                return abort(HTTPStatus.FORBIDDEN, message="Not enough permissions")

        return decorator

    return wrapper


def get_or_create_user(email: str, social_id: str, name: str) -> (User, str | None):
    user = User.query.filter_by(email=email).first()
    raw_password = None
    if not user:
        alphabet = string.ascii_letters + string.digits
        raw_password = "".join(secrets.choice(alphabet) for _ in range(8))
        role = Role.query.filter_by(name="registered").first()
        new_user = User(email=email, password=raw_password, role=role, social_id=social_id, name=name)
        db.session.add(new_user)
        db.session.commit()
    return user, raw_password


def create_tokens(user: User) -> dict:
    access_token = create_access_token(
        identity=user.email,
        fresh=True,
        additional_claims={
            "permissions": [p.name for p in user.role.permissions],
            "role": user.role.name,
        },
    )
    refresh_token = create_refresh_token(identity=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}
