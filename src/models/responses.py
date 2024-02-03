from db_settings import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class Response(Base):
    __tablename__ = "responses"
    # __table_args__ = {"extend_existing": True}

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор отклика")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), comment="Идентификатор пользователя")
    job_id = sa.Column(sa.Integer, sa.ForeignKey('jobs.id'), comment="Идентификатор вакансии")

    # добавьте ваши колонки сюда
    message = sa.Column(sa.String(2000), default="", comment="Сопроводительное письмо", nullable=True)

    user = relationship("User", back_populates="responses")
    job = relationship("Job", back_populates="responses")

    def __str__(self):
        return "Reponse"
