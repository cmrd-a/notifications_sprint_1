from uuid import UUID

from fastapi import APIRouter, Response, status, Depends

from models import Review, Rating, Bookmark
from mongo_service import get_mongo_service, MongoService

router = APIRouter()


@router.post("/ratings", summary="Поставить оценку")
async def rate(
    body: Rating,
    mongo_service: MongoService = Depends(get_mongo_service),
):
    await mongo_service.set_rating(body.user_id, body.film_id, body.rating)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/ratings", response_model=list[Rating], summary="Получить оценки")
async def get_rating(
    user_id: int = None,
    film_id: UUID = None,
    mongo_service: MongoService = Depends(get_mongo_service),
):
    ratings = await mongo_service.get_rating(user_id, film_id)
    return ratings


@router.delete("/ratings", summary="Удалить оценку фильма")
async def delete_rating(
    user_id: int = None,
    film_id: UUID = None,
    mongo_service: MongoService = Depends(get_mongo_service),
):
    await mongo_service.delete_rating(user_id, film_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/review", summary="Оставить ревью")
async def review(
    body: Review,
    mongo_service: MongoService = Depends(get_mongo_service),
):
    await mongo_service.add_review(body.user_id, body.film_id, body.review)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/reviews", response_model=list[Review], summary="Получить ревью пользователя к фильму")
async def get_review(
    user_id: int = None,
    film_id: UUID = None,
    mongo_service: MongoService = Depends(get_mongo_service),
):
    review = await mongo_service.get_review(user_id, film_id)
    return review


@router.delete("/reviews", summary="Удалить ревью фильма")
async def delete_review(
    user_id: int = None,
    film_id: UUID = None,
    mongo_service: MongoService = Depends(get_mongo_service),
):
    await mongo_service.delete_review(user_id, film_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/bookmarks", summary="Добавить фильм в закладки")
async def bookmark(
    body: Bookmark,
    mongo_service: MongoService = Depends(get_mongo_service),
):
    await mongo_service.add_bookmark(body.user_id, body.film_id)
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/bookmarks", summary="Удалить фильм из закладок пользователя")
async def delete_bookmark(
    user_id: int,
    film_id: UUID,
    mongo_service: MongoService = Depends(get_mongo_service),
):
    await mongo_service.delete_bookmark(user_id, film_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/bookmarks", response_model=list[Bookmark], summary="Получить закладки пользователя")
async def get_users_bookmarks(
    user_id: int,
    mongo_service: MongoService = Depends(get_mongo_service),
):
    bookmarks = await mongo_service.get_users_bookmarks(user_id)
    return bookmarks
