import datetime

from db_settings import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = "jobs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор вакансии")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), comment="Идентификатор пользователя")
    title = sa.Column(sa.String, comment="Название вакансии")
    description = sa.Column(sa.String, comment="Описание вакансии")
    salary_from = sa.Column(sa.Numeric, comment="Зарплата от")
    salary_to = sa.Column(sa.Numeric, comment="Зарплата до")
    is_active = sa.Column(sa.Boolean, comment="Активна ли вакансия")
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, comment="Дата создания записи")

    user = relationship("User", back_populates="jobs", cascade="all, delete")
    responses = relationship("Response", back_populates="job", cascade="all, delete")
