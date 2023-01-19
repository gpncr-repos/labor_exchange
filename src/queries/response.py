from models import Response
from queries.base_repository import BaseAsyncRepository


class ResponseRepository(BaseAsyncRepository):
    model = Response
