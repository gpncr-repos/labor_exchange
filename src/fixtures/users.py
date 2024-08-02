from datetime import datetime

import factory
from factory_boy_extra.async_sqlalchemy_factory import \
    AsyncSQLAlchemyModelFactory

from models import User


class UserFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('pystr')
    email = factory.Faker('email')
    hashed_password = factory.Faker('password')
    is_company = factory.Faker('pybool')
    created_at = factory.LazyFunction(datetime.utcnow)


class UserUpdateFactory:
    def __init__(self) -> None:
        self.name = factory.Faker('pystr')
        self.email = factory.Faker('email')
        self.is_company = factory.Faker('pybool')
