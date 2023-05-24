import factory
from models import Response
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class ResponseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = factory.Sequence(lambda n: n)
    user_id = factory.Faker("pyint")
    job_id = factory.Faker("pyint")
    message = factory.Faker("pystr")
