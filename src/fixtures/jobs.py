from datetime import datetime

import factory
from factory_boy_extra.async_sqlalchemy_factory import \
    AsyncSQLAlchemyModelFactory

from models import Job


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    user_id = factory.Faker('pyint')
    title = factory.Faker('pystr')
    discription = factory.Faker('pystr')
    salary_from = factory.Faker('pyint', min_value=0, max_value=500)
    salary_to = factory.Faker('pyint', min_value=600, max_value=1000)
    is_active = factory.Faker('pybool')
    created_at = factory.LazyFunction(datetime.utcnow)
