import factory

from fixtures.users import UserFactory
from models import Job
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    title = factory.Faker("name")
    description = factory.Faker("text")
    salary_from = factory.Faker("pyint")
    salary_to = factory.Faker("pyint")
    created_at = factory.LazyFunction(datetime.utcnow)
    user = factory.SubFactory(UserFactory)
    user_id = factory.LazyAttribute(lambda o: o.user.id)

