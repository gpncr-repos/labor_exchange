from pydantic.main import BaseModel

import schemas
from core.security import hash_password
from models import User
from queries.base_repository import BaseAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseAsyncRepository):
    model = User

    async def create_by_schema(
            self,
            db: AsyncSession,
            user_schema: schemas.UserInSchema
    ) -> User:
        user = User(
            name=user_schema.name,
            email=user_schema.email,
            hashed_password=hash_password(user_schema.password),
            is_company=user_schema.is_company
        )
        return await self.create(db, user)
