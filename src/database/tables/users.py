import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.database.engine import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор пользователя", unique=True)
    email = sa.Column(sa.String(255), comment="Email адрес", nullable=False, unique=True)
    name = sa.Column(sa.String(255), comment="Имя пользователя", nullable=False)
    hashed_password = sa.Column(sa.String, comment="Хэш пароля", nullable=False)
    is_company = sa.Column(
        sa.Boolean, comment="Признак, является ли юзер компанией", server_default="f", nullable=False
    )
    created_at = sa.Column(
        sa.DateTime, comment="Время создания записи", server_default=sa.text("TIMEZONE('utc', now())"), nullable=False
    )

    jobs = relationship("Job", back_populates="user")
    responses = relationship("Response", back_populates="user")
