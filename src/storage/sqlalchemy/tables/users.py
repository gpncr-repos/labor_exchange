from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.sqlalchemy.client import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="Идентификатор пользователя"
    )
    email: Mapped[str] = mapped_column(unique=True, comment="Email адрес")
    name: Mapped[str] = mapped_column(comment="Имя пользователя")
    hashed_password: Mapped[str] = mapped_column(comment="Зашифрованный пароль")
    is_company: Mapped[bool] = mapped_column(comment="Флаг компании")
    created_at: Mapped[datetime] = mapped_column(
        comment="Время создания записи", default=datetime.utcnow
    )

    jobs: Mapped[list["Job"]] = relationship(  # noqa
        back_populates="user", cascade="all, delete-orphan"
    )
    responses: Mapped[list["Response"]] = relationship(  # noqa
        back_populates="user", cascade="all, delete-orphan"
    )
