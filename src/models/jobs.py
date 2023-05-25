from __future__ import annotations
from typing import List

import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db_settings import Base
import models


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор вакансии",
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        comment="Идентификатор пользователя, опубликовавшего вакансию",
    )

    title: Mapped[str] = mapped_column(comment="Название вакансии")
    description: Mapped[str] = mapped_column(comment="Описание вакансии")
    salary_from: Mapped[Decimal] = mapped_column(comment="Зарплата от")
    salary_to: Mapped[Decimal] = mapped_column(comment="Зарплата до")
    is_active: Mapped[bool] = mapped_column(comment="Активна ли вакансия")
    created_at: Mapped[datetime.datetime] = mapped_column(
        comment="Время создания записи", default=datetime.datetime.utcnow
    )

    user: Mapped[models.users.User] = relationship(
        back_populates="jobs"
    )  # организация, опубликовавшая вакансию
    responses: Mapped[List[models.responses.Response]] = relationship(
        back_populates="job"
    )  # отклики соискателей
