from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.sqlalchemy.client import Base


class Response(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(primary_key=True, comment="Идентификатор отклика")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), comment="Идентификатор пользователя"
    )
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), comment="Идентификатор вакансии")

    # добавьте ваши колонки сюда

    user: Mapped["User"] = relationship(back_populates="responses")  # noqa
    job: Mapped["Job"] = relationship(back_populates="responses")  # noqa
