from db_settings import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class Response(Base):
    """Отклик"""
    __tablename__ = "responses"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор отклика")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), comment="Идентификатор пользователя")
    job_id = sa.Column(sa.Integer, sa.ForeignKey('jobs.id'), comment="Идентификатор вакансии")

    message = sa.Column(sa.String, comment="Сопроводительное письмо", nullable=True)

    user = relationship("User", back_populates="responses")
    job = relationship("Job", back_populates="responses")
