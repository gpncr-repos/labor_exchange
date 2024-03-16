import factory
from models import User, Job, Response
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class UserFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("pystr")
    email = factory.Faker("email")
    hashed_password = factory.Faker("password")
    is_company = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    title = factory.Faker('job')
    description = factory.Faker('paragraph', nb_sentences=3)
    # salary_from = factory.Faker('pyint', min_value=1, max_value=50)
    salary_from = factory.Faker('pydecimal', min_value=1, max_value=50)
    salary_to = factory.LazyAttribute(lambda x: x.salary_from + 10)
    is_active = factory.Faker('pybool')
    created_at = factory.LazyFunction(datetime.utcnow)

class ResponseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = factory.Sequence(lambda n: n)
    message = factory.Faker('paragraph', nb_sentences=2)
