from src.database.engine import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class Response(Base):
    __tablename__ = "responses"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор отклика")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), comment="Идентификатор пользователя", nullable=False)
    job_id = sa.Column(sa.Integer, sa.ForeignKey('jobs.id'), comment="Идентификатор вакансии", nullable=False)
    message = sa.Column(sa.String(500), comment="Сопроводительное письмо")

    user = relationship("User", back_populates="responses")
    job = relationship("Job", back_populates="responses")
