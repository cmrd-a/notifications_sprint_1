import logging
from logging.config import dictConfig

from auth_client import Configuration, ApiClient, ApiException
from auth_client.api import user_api
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from urllib3.exceptions import RequestError, HTTPError

from core.config import config
from core.logger import LOGGING

router = APIRouter()
oauth2_scheme = HTTPBearer(auto_error=False)

dictConfig(LOGGING)
logger = logging.getLogger(__name__)


async def get_permissions(token: str = Depends(oauth2_scheme)) -> list[str]:
    if not token:
        return []
    configuration = Configuration(host=config.auth_url, access_token=token.credentials)

    with ApiClient(configuration) as api_client:
        api_instance = user_api.UserApi(api_client)
        try:
            api_response = api_instance.auth_users_v1_get_permissions_get()
        except (RequestError, HTTPError, ApiException) as e:
            logger.error("auth-service unaviable", exc_info=e)
            return []
        else:
            return api_response.permissions or []
