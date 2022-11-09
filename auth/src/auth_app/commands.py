import click

from auth_app.db.models import Permission, Role, User
from auth_app.extensions import db


@click.command()
@click.argument("email")
@click.argument("password")
def create_superuser(email, password):
    base_roles = {
        "registered": ["comment"],
        "superuser": ["comment", "manage_users", "watch_best_movies"],
    }
    for role_name, permissions in base_roles.items():
        permissions_objects = []
        for permission_name in permissions:
            permission = Permission.query.filter_by(name=permission_name).first()
            if not permission:
                permission = Permission(name=permission_name)
                db.session.add(permission)
                db.session.commit()
            permissions_objects.append(permission)
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name, permissions=permissions_objects)
            db.session.add(role)
            db.session.commit()

    user = User.query.filter_by(email=email).first()
    if not user:
        super_role = Role.query.filter_by(name="superuser").first()
        user = User(email=email, password=password, role=super_role)
        db.session.add(user)
        db.session.commit()
