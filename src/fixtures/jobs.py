import factory
from models import Job
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    user_id = factory.Faker("pyint")
    title = factory.Faker("pystr")
    description = factory.Faker("pystr")
    salary_from = factory.Faker(
        "pydecimal", left_digits=8, right_digits=2, positive=True
    )
    salary_to = factory.Faker("pydecimal", left_digits=8, right_digits=2, positive=True)
    is_active = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)
