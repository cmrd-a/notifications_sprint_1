from datetime import datetime
from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from db import get_mongo


class MongoService:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = self.client.ugc_db
        self.ratings = self.db.ratings
        self.reviews = self.db.reviews
        self.likes = self.db.likes
        self.bookmarks = self.db.bookmarks

    async def set_rating(self, user_id: int, film_id: UUID, rating: int):
        filter = {"user_id": user_id, "film_id": str(film_id)}
        replacement = {"user_id": user_id, "film_id": str(film_id), "rating": rating, "created_at": datetime.now()}
        await self.ratings.replace_one(filter, replacement, True)

    async def delete_rating(self, user_id: int, film_id: UUID):
        find_doc = {}
        if user_id:
            find_doc["user_id"] = user_id
        if film_id:
            find_doc["film_id"] = str(film_id)
        await self.ratings.delete_one(find_doc)

    async def get_rating(self, user_id: int = None, film_id: UUID = None):
        docs = []
        find_doc = {}
        if user_id:
            find_doc["user_id"] = user_id
        if film_id:
            find_doc["film_id"] = str(film_id)
        async for doc in self.ratings.find(find_doc):
            docs.append(doc)
        return docs

    async def add_review(self, user_id: int, film_id: UUID, review: str):
        filter = {"user_id": user_id, "film_id": str(film_id)}
        replacement = {"user_id": user_id, "film_id": str(film_id), "review": review, "created_at": datetime.now()}
        await self.reviews.replace_one(filter, replacement, True)

    async def get_review(self, user_id: int = None, film_id: UUID = None):
        docs = []
        find_doc = {}
        if user_id:
            find_doc["user_id"] = user_id
        if film_id:
            find_doc["film_id"] = str(film_id)
        async for doc in self.reviews.find(find_doc):
            docs.append(doc)
        return docs

    async def delete_review(self, user_id: int, film_id: UUID):
        find_doc = {}
        if user_id:
            find_doc["user_id"] = user_id
        if film_id:
            find_doc["film_id"] = str(film_id)
        await self.reviews.delete_one(find_doc)

    async def add_bookmark(self, user_id: int, film_id: UUID):
        filter = {"user_id": user_id, "film_id": str(film_id)}
        replacement = {"user_id": user_id, "film_id": str(film_id), "created_at": datetime.now()}
        await self.bookmarks.replace_one(filter, replacement, True)

    async def delete_bookmark(self, user_id: int, film_id: UUID):
        find_doc = {"user_id": user_id, "film_id": str(film_id)}
        await self.bookmarks.delete_one(find_doc)

    async def get_users_bookmarks(self, user_id: int):
        docs = []
        find_doc = {"user_id": user_id}
        async for doc in self.bookmarks.find(find_doc):
            docs.append(doc)
        return docs


@lru_cache
def get_mongo_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> MongoService:
    return MongoService(mongo)
