from datetime import datetime

import factory
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory

from models import Response


class ResponseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = factory.Sequence(lambda n: n)
    user_id = factory.Faker("pyint")
    job_id = factory.Faker("pyint")
    message = factory.Faker("pystr")
    created_at = factory.LazyFunction(datetime.utcnow)


class ResponseCreateFactory(factory.BaseDictFactory):
    class Meta:
        model = Response

    message = factory.Faker("pystr")
