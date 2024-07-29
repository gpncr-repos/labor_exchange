from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.jobs import JobEntity
from infra.repositories.alchemy_models.base import TimedBaseModel

if TYPE_CHECKING:
    from infra.repositories.alchemy_models.responses import Response
    from infra.repositories.alchemy_models.users import User


class Job(TimedBaseModel):
    title: Mapped[str] = mapped_column(String(100), comment="Название вакансии")
    description: Mapped[str] = mapped_column(Text, comment="Описание вакансии")
    salary_from: Mapped[float] = mapped_column(comment="Зарплата от")
    salary_to: Mapped[float] = mapped_column(comment="Зарплата до")
    is_active: Mapped[bool] = mapped_column(comment="Активна ли вакансия ")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), comment="Идентификатор пользователя")

    user: Mapped['User'] = relationship(back_populates="jobs", )
    responses: Mapped[list['Response']] = relationship(back_populates="job")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r}"

    def __repr__(self):
        return str(self)

    def to_entity(self) -> JobEntity:
        return JobEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            salary_from=self.salary_from,
            salary_to=self.salary_to,
            is_active=self.is_active,
            user_id=self.user_id,
            created_at=self.created_at,
        )
