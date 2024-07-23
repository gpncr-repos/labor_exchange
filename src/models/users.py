import datetime

from sqlalchemy.orm import relationship

from db_settings import Base
import sqlalchemy as sa


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор пользователя")
    email = sa.Column(sa.String, comment="Email адрес", unique=True)
    name = sa.Column(sa.String, comment="Имя пользователя")
    hashed_password = sa.Column(sa.String, comment="Зашифрованный пароль", unique=True)
    is_company = sa.Column(sa.Boolean, comment="Флаг компании(является ли пользователь компанией)")
    created_at = sa.Column(sa.DateTime, comment="Дата создания записи", default=datetime.datetime.utcnow)

    jobs = relationship("Job", back_populates="users")
    responses = relationship("Response", back_populates="users")
