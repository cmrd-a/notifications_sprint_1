#!/bin/bash
echo "Waiting for postgres..."
    while ! nc -z "$POSTGRES_DB_HOST" "$POSTGRES_DB_PORT"; do
      sleep 0.1
    done
echo "PostgreSQL started"

alembic -c src/alembic.ini upgrade head
flask --app src/auth_app.app create-superuser "$AUTH_SUPERUSER_EMAIL" "$AUTH_SUPERUSER_PASSWORD"
gunicorn -k gevent -w 8 "auth_app.wsgi_app:create_app()" --chdir src --bind 0.0.0.0:9000