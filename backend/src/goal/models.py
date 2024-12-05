from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.models import Habit

if TYPE_CHECKING:
    from src.auth.models import User


class Goal(Base):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="goals")
    habits: Mapped[List["Habit"]] = relationship(back_populates="goal", cascade='save-update, merge, delete',
                                                 passive_deletes=True)
