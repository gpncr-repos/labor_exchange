import factory
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory
from models import Job


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    title = factory.Faker("job")
    description = factory.Faker("text")
    salary_from = factory.Faker("random_number", digits=7)
    salary_to = factory.Faker("random_number", digits=7)
    is_active = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)
