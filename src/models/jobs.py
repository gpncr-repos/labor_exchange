from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db_settings import Base

class Job(Base):
    __tablename__ = "jobs"
    # __table_args__ = {"extend_existing": True}

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор вакансии")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), comment="Идентификатор пользователя")

    # добавьте ваши колонки сюда
    title = sa.Column(sa.String, default="", comment="Название вакансии", nullable=True)
    description = sa.Column(sa.String(500), default="", comment="Описание вакансии", nullable=True)
    salary_from = sa.Column(sa.Numeric, sa.CheckConstraint("salary_from >= 0"), default=0., comment="Зарплата от", nullable=True)
    salary_to = sa.Column(sa.Numeric, sa.CheckConstraint("salary_from >= 0"), default=0., comment="Зарплата до", nullable=True)
    is_active = sa.Column(sa.Boolean, default=True, comment="Активна ли вакансия", nullable=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, comment="Дата создания записи")

    user = relationship("User", back_populates="jobs")
    responses = relationship("Response", back_populates="job") #, cascade="all, delete")
