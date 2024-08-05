from fastapi import Depends
from punq import Container

from di import get_container

from logic.services.users.base import BaseUserService


def get_user_service(container: Container = Depends(get_container)) -> BaseUserService:
    service: BaseUserService = container.resolve(BaseUserService)
    return service
