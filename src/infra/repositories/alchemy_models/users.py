from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.users import UserEntity
from infra.repositories.alchemy_models.base import TimedBaseModel
from infra.repositories.alchemy_models.jobs import Job
from infra.repositories.alchemy_models.responses import Response


class User(TimedBaseModel):
    email: Mapped[str] = mapped_column(comment="Email адрес", unique=True)
    name: Mapped[str] = mapped_column(comment="Имя пользователя")
    hashed_password: Mapped[str] = mapped_column(comment="Зашифрованный пароль")
    is_company: Mapped[bool] = mapped_column(comment="Флаг компании")

    jobs: Mapped[list["Job"]] = relationship(back_populates="user")
    responses: Mapped[list["Response"]] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            email=self.email,
            name=self.name,
            is_company=self.is_company,
            hashed_password=self.hashed_password,
            created_at=self.created_at
        )
