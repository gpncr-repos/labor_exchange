import factory

from fixtures.users import UserFactory
from models import Job
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n+5)
    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute('user.id')
    title = factory.Faker("pystr")
    description = factory.Faker("pystr")
    salary_from = factory.Faker("pydecimal")
    salary_to = factory.Faker("pydecimal")
    is_active = factory.Faker("pybool")

