import factory
from models import Response
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory

from .users import UserFactory
from .jobs import JobFactory


class ResponseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = factory.Sequence(int)
    message = factory.Faker("pystr")

    user = factory.SubFactory(UserFactory, is_company=False)
    job = factory.SubFactory(JobFactory)
