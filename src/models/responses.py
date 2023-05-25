from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db_settings import Base
import models


class Response(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор отклика",
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), comment="Идентификатор пользователя"
    )
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id"), comment="Идентификатор вакансии"
    )
    message: Mapped[str] = mapped_column(comment="Сопроводительное письмо")

    user: Mapped[models.users.User] = relationship(
        back_populates="responses"
    )  # соискатель, откликнувшийся на данную вакансию
    job: Mapped[models.jobs.Job] = relationship(
        back_populates="responses"
    )  # вакансия, на которую откликнулся соискатель
