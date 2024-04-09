import factory
from faker import Faker

from models import Job
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    title = factory.Faker("pystr")
    description = factory.Faker("pystr")
    salary_from = Faker.pydecimal(left_digits=None, right_digits=None, positive=False)
    salary_to = Faker.pydecimal(left_digits=None, right_digits=None, positive=False)
    is_active = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)
