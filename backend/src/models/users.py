import datetime

from sqlalchemy.orm import relationship

from db_settings import Base
import sqlalchemy as sa


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор задачи", unique=True)
    email = sa.Column(sa.String, comment="Email адрес", unique=True)
    name = sa.Column(sa.String, comment="Имя пользователя")
    hashed_password = sa.Column(sa.String, comment="Зашифрованный пароль")
    is_company = sa.Column(sa.Boolean, comment="Флаг компании")
    created_at = sa.Column(sa.DateTime, comment="Время создания записи", default=datetime.datetime.utcnow)

    jobs = relationship("Job", back_populates="user")
    responses = relationship("Response", back_populates="user")
