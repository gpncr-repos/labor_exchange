import factory
from models import Response
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class ResponseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Response
    id = factory.Sequence(lambda n: n)
    user_id = factory.Faker('pyint')
    job_id = factory.Faker('pyint')
    massage = factory.Faker("pystr")
    created_at= factory.LazyFunction(datetime.utcnow)
