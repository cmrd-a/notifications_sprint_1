import logging

import psycopg
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
    docs_url="/notifier/docs",
    openapi_url="/notifier/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    postgres.pg = await psycopg.AsyncConnection.connect(**config.pg_connection_params)


@app.on_event("shutdown")
async def shutdown():
    await postgres.pg.close()


app.include_router(notifications.router, prefix="/notifier/v1/notifications", tags=["notifications"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8020,
        log_config=LOGGING,
        log_level=logging.INFO,
    )
