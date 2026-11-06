from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, unmapped_dataclass


@unmapped_dataclass
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        init=False,
        server_default=func.now(), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

@unmapped_dataclass
class ActiveMixin:
    is_active: Mapped[bool] = mapped_column(
        init=False,
        nullable=False, 
        server_default="true",
        default=True
    )