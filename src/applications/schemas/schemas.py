from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class JobDO:
    user_id: int = field(default_factory=int)
    title: Optional[str] = field(default_factory=str)
    description: Optional[str] = field(default_factory=str)
    salary_from: Optional[Decimal] = field(default_factory=Decimal)
    salary_to: Optional[Decimal] = field(default_factory=Decimal)
    is_active: Optional[bool] = field(default_factory=bool)
    created_at: datetime = field(default=datetime.utcnow())
