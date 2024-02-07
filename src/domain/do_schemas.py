from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class DOJob:
    user_id: Optional[int] = field(default_factory=int)
    title: Optional[str] = field(default_factory=str)
    description: Optional[str] = field(default_factory=str)
    salary_from: Optional[Decimal] = field(default_factory=Decimal)
    salary_to: Optional[Decimal] = field(default_factory=Decimal)
    is_active: Optional[bool] = field(default=True)
    created_at: Optional[datetime] = None

@dataclass
class DOJobEdit:
    title: Optional[str] = field(default_factory=str)
    description: Optional[str] = field(default_factory=str)
    salary_from: Optional[Decimal] = field(default_factory=Decimal)
    salary_to: Optional[Decimal] = field(default_factory=Decimal)
    is_active: Optional[bool] = field(default=True)

@dataclass
class DOResponse:
    id: Optional[int] = field(default_factory=int)
    user_id: Optional[int] = field(default_factory=int)
    job_id: Optional[int] = field(default_factory=int)
    message: Optional[str] = field(default_factory=str)

@dataclass
class DOUser:
    id: Optional[int] = field(default_factory=int)
    email: Optional[str] = field(default_factory=str)
    name: Optional[str] = field(default_factory=str)
    hashed_password: Optional[str] = field(default_factory=str)
    is_company: Optional[bool] = True
    created_at: Optional[datetime] = None
