from fastapi import Depends
from punq import Container

from di import get_container
from logic.services.jobs.base import BaseJobService


def get_job_service(container: Container = Depends(get_container)) -> BaseJobService:
    service: BaseJobService = container.resolve(BaseJobService)
    return service
