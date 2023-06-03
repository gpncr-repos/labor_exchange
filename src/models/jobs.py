import datetime
from db_settings import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = "jobs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор вакансии")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), comment="Идентификатор пользователя")

    title = sa.Column(sa.String, comment="Название вакансии", nullable=False)
    description = sa.Column(sa.String, comment="Описание вакансии", nullable=False)
    salary_from = sa.Column(sa.Float, comment="Зарплата от", nullable=True)
    salary_to = sa.Column(sa.Float, comment="Зарплата до", nullable=True)
    is_active = sa.Column(sa.Boolean, comment="Активна ли вакансия", nullable=False)
    created_at = sa.Column(sa.DateTime, comment="Дата создания вакансии", default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="jobs")
    responses = relationship("Response", back_populates="job")
