from fastapi import Depends
from punq import Container

from di import get_container
from logic.services.responses.base import BaseResponseService


def get_response_service(container: Container = Depends(get_container)) -> BaseResponseService:
    service: BaseResponseService = container.resolve(BaseResponseService)
    return service
