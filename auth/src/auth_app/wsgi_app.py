from gevent import monkey

monkey.patch_all()

from auth_app.app import create_app  # noqa
