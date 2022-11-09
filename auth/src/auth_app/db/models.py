from typing import Optional, Type, TypeVar

from auth_app.extensions import db
from sqlalchemy_utils import IPAddressType, PasswordType, force_auto_coercion

T = TypeVar("T", bound="PkModel")
force_auto_coercion()


class PkModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls: Type[T], record_id: int) -> Optional[T]:
        return cls.query.get(record_id)


class CreatedUpdatedModel(PkModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


roles_permissions = db.Table(
    "roles_permissions",
    db.metadata,
    db.Column("permission_id", db.ForeignKey("permissions.id"), primary_key=True),
    db.Column("role_id", db.ForeignKey("roles.id"), primary_key=True),
)


class Permission(CreatedUpdatedModel):
    __tablename__ = "permissions"

    name = db.Column(db.String(128), unique=True, index=True, nullable=False)


class Role(CreatedUpdatedModel):
    __tablename__ = "roles"

    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    permissions = db.relationship("Permission", secondary=roles_permissions, backref="roles")


class User(CreatedUpdatedModel):
    __tablename__ = "users"

    email = db.Column(db.String(80), unique=True, index=True, nullable=False)
    password = db.Column(PasswordType(schemes=["pbkdf2_sha512"]), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    social_id = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64))

    role = db.relationship("Role")


class LoginHistory(PkModel):
    __tablename__ = "login_history"
    __table_args__ = {"postgresql_partition_by": "LIST (user_device_type)"}

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    ip_address = db.Column(IPAddressType)
    login_time = db.Column(db.DateTime, default=db.func.now())
    user_agent = db.Column(db.Text)
    user_device_type = db.Column(db.Text, default="desktop")

    user = db.relationship("User")
