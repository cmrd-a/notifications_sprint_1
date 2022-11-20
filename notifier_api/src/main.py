import logging

import psycopg2
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from psycopg2.extras import NamedTupleCursor

from api.v1 import notifications
from core.config import config
from core.logger import LOGGING
from db import postgres


app = FastAPI(
    title=config.project_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    postgres.pg = psycopg2.connect(**config.pg_connection_params, cursor_factory=NamedTupleCursor)


app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.INFO,
    )
