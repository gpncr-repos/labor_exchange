from db_settings import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = "jobs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор вакансии")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), comment="Идентификатор пользователя")

    # добавьте ваши колонки сюда

    user = relationship("User", back_populates="jobs")
    responses = relationship("Response", back_populates="job")
