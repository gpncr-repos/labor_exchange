import datetime

from db_settings import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class Job(Base):
    """Вакансия работы"""
    __tablename__ = "jobs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор вакансии")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), comment="Идентификатор пользователя")

    title = sa.Column(sa.String, comment="Назначение вакансии")
    description = sa.Column(sa.String, comment="Описание вакансии", nullable=True)
    salary_from = sa.Column(sa.Integer, comment="Зарплата от", nullable=True)
    salary_to = sa.Column(sa.Integer, comment="Зарплата до", nullable=True)
    is_active = sa.Column(sa.Boolean, comment="Активность вакансии", default=True)
    created_at = sa.Column(sa.DateTime, comment="Дата создания", default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="jobs")
    responses = relationship("Response", back_populates="job")
