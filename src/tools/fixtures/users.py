from datetime import datetime

import factory

from storage.sqlalchemy.tables import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("pystr")
    email = factory.Faker("email")
    hashed_password = factory.Faker("password")
    is_company = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)
