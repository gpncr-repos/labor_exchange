from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.responses import ResponseEntity, ResponseAggregateJobEntity, ResponseAggregateUserEntity
from infra.repositories.alchemy_models.base import TimedBaseModel

if TYPE_CHECKING:
    from infra.repositories.alchemy_models.jobs import Job
    from infra.repositories.alchemy_models.users import User


class Response(TimedBaseModel):
    message: Mapped[str] = mapped_column(Text, comment="Описание вакансии")
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), comment="Идентификатор пользователя")
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"), comment="Идентификатор вакансии")

    user: Mapped["User"] = relationship(back_populates="responses", )
    job: Mapped["Job"] = relationship(back_populates="responses", )

    __table_args__ = (
        UniqueConstraint('user_id', 'job_id', name='uix_user_job'),
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id},"

    def __repr__(self):
        return str(self)

    def to_entity(self) -> ResponseEntity:
        return ResponseEntity(
            id=self.id,
            message=self.message,
            user_id=self.user_id,
            job_id=self.job_id,
            created_at=self.created_at,
        )

    def to_aggregate_job_entity(self) -> ResponseAggregateJobEntity:
        return ResponseAggregateJobEntity(
            id=self.id,
            message=self.message,
            user_id=self.user_id,
            job_id=self.job_id,
            created_at=self.created_at,
            job=self.job.to_entity()
        )

    def to_aggregate_user_entity(self) -> ResponseAggregateUserEntity:
        return ResponseAggregateUserEntity(
            id=self.id,
            message=self.message,
            user_id=self.user_id,
            job_id=self.job_id,
            created_at=self.created_at,
            user=self.user.to_entity()
        )
