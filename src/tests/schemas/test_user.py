import pytest
from pydantic import ValidationError

from queries import user as user_query
from schemas import UserCreateSchema


@pytest.mark.asyncio
async def test_create_password_mismatch(sa_session):
    with pytest.raises(ValidationError):
        user = UserCreateSchema(
            name="Uchpochmak",
            email="bashkort@example.com",
            password="eshkere!",
            password2="eshkero",
            is_company=False,
        )
        await user_query.create(sa_session, user_schema=user)
