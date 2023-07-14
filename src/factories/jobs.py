import factory
import faker
from models import Job
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory

from .users import UserFactory

fake = faker.Faker()
MIN_SALARY = 1
MAX_SALARY = 2_000_000
SALARY_DIGITS = 2


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(int)
    title = factory.Faker("pystr")
    description = factory.Faker("pystr")
    salary_from = factory.Faker(
        "pydecimal",
        min_value=MIN_SALARY,
        max_value=MAX_SALARY,
        right_digits=SALARY_DIGITS
    )

    @factory.lazy_attribute
    def salary_to(self):
        min_val = min(int(self.salary_from) + 1, MAX_SALARY)
        return fake.pydecimal(
            min_value=min_val,
            max_value=MAX_SALARY,
            right_digits=SALARY_DIGITS
        )

    is_active = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)

    user = factory.SubFactory(UserFactory, is_company=True)
