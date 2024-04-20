import factory
from factory_boy_extra.async_sqlalchemy_factory import \
    AsyncSQLAlchemyModelFactory

from models import Response

from .jobs import JobFactory
from .users import UserFactory


class ResponseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = factory.Sequence(int)
    message = factory.Faker("sentence")
    user = factory.SubFactory(UserFactory)
    job = factory.SubFactory(JobFactory)
