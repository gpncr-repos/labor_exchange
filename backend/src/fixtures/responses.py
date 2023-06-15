from factory.base import BaseFactory
import factory
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory

from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from models import Response


class ResponseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = factory.Sequence(lambda n: n)
    message = factory.Faker("text")