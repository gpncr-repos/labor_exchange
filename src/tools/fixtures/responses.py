from datetime import datetime

import factory

from storage.sqlalchemy.tables import Response
from tools.fixtures.jobs import JobFactory
from tools.fixtures.users import UserFactory



class ResponseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = factory.Sequence(lambda n: n)
    job = factory.SubFactory(JobFactory)
    user = factory.SubFactory(UserFactory)
    message = factory.Faker("sentence")
    created_at = factory.LazyFunction(datetime.utcnow)
