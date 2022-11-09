from fastapi import APIRouter, Depends
from fastapi import Response, status

from models.analytics import FilmProgressView
from services.analytics import KafkaService, get_kafka_service

router = APIRouter()


@router.post("/", summary="Сохранение прогресса просмотра фильма")
async def load_to_kafka(
    request: FilmProgressView,
    kafka_service: KafkaService = Depends(get_kafka_service),
):
    await kafka_service.put_film_progress(
        user_id=request.user_id,
        film_id=request.film_id,
        film_position_ms=request.film_position_ms,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
