from __future__ import annotations
from typing import List
import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db_settings import Base
import models


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор задачи",
        unique=True,
    )
    email: Mapped[str] = mapped_column(comment="Email адрес", unique=True)
    name: Mapped[str] = mapped_column(comment="Имя пользователя")
    hashed_password: Mapped[str] = mapped_column(comment="Зашифрованный пароль")
    is_company: Mapped[bool] = mapped_column(comment="Флаг компании")
    created_at: Mapped[datetime.datetime] = mapped_column(
        comment="Время создания записи", default=datetime.datetime.utcnow
    )

    jobs: Mapped[List[models.jobs.Job]] = relationship(
        back_populates="user"
    )  # вакансии, опубликованные пользователем
    responses: Mapped[List[models.responses.Response]] = relationship(
        back_populates="user"
    )  # отклики пользователя
