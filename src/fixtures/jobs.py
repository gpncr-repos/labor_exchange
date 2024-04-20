from datetime import datetime

import factory
from factory_boy_extra.async_sqlalchemy_factory import \
    AsyncSQLAlchemyModelFactory

from models import Job


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(int)
    title = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("paragraph", nb_sentences=3)
    salary_from = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )
    salary_to = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    is_active = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)
