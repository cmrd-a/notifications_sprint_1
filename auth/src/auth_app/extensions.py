from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from opentelemetry.instrumentation.flask import FlaskInstrumentor

db = SQLAlchemy()
jwt = JWTManager()
redis_client = FlaskRedis()
flask_instrumentator = FlaskInstrumentor()
limiter = Limiter(key_func=get_remote_address)
