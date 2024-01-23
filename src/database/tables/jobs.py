import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.database.engine import Base


class Job(Base):
    __tablename__ = "jobs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор вакансии")
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False, comment="Идентификатор пользователя")
    title = sa.Column(sa.String(255), comment="Название вакансии", nullable=False)
    description = sa.Column(sa.String, comment="Описание вакансии", nullable=False)
    salary_from = sa.Column(sa.NUMERIC(scale=2), comment="Нижний порог зарплаты")
    salary_to = sa.Column(sa.NUMERIC(scale=2), comment="Верхний порог запрлаты")
    is_active = sa.Column(sa.Boolean, comment="Признак, активна ли вакансия", server_default="t", nullable=False)
    created_at = sa.Column(
        sa.DateTime, comment="Время создания записи", server_default=sa.text("TIMEZONE('utc', now())")
    )
    # думаю, было бы неплохо добавить еще одну колонку updated_at

    user = relationship("User", back_populates="jobs")
    responses = relationship("Response", back_populates="job")
