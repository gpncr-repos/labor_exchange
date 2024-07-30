import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, declared_attr, declarative_base

Base = declarative_base()


class TimedBaseModel(Base):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[str] = mapped_column(primary_key=True, comment="Идентификатор", unique=True,)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), comment="Время создания записи",)
