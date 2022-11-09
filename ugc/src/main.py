import logging

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1 import ugc
from core.config import config
from core.logger import LOGGING
import db

app = FastAPI(
    title=config.project_name,
    docs_url="/ugc/docs",
    openapi_url="/ugc/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    db.mongo = AsyncIOMotorClient(config.mongo_url)


@app.on_event("shutdown")
async def shutdown():
    db.mongo.close()


app.include_router(ugc.router, prefix="/v1/ugc", tags=["ugc"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8010, log_config=LOGGING, log_level=logging.INFO)
