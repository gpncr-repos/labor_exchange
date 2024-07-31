from dataclasses import dataclass, field, asdict
from datetime import datetime
from uuid import uuid4


@dataclass
class BaseEntity:
    id: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )

    def to_not_nullable_values_dict(self):
        return {key: value for key, value in asdict(self).items() if value}
