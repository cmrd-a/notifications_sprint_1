from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel

from models.notification import NotificationTaskV1
from services.services import PGService, get_postgres_service

router = APIRouter()


class Film(BaseModel):
    id: str
    title: str


@router.post("/notification", summary="Создать задачу на рассылку сообщения")
async def create_notification_task(
    body: NotificationTaskV1,
    pg_service: PGService = Depends(get_postgres_service),
):
    await pg_service.save_notification(notification=body)
    return Response(status_code=status.HTTP_201_CREATED)
