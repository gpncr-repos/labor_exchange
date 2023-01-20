from models import Job
from queries.base_repository import BaseAsyncRepository


class JobRepository(BaseAsyncRepository):
    model = Job
