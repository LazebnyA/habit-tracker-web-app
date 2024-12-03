from datetime import datetime
from typing import List

from sqlalchemy import String, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Goal(Base):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    userID: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="goals")
    habits: Mapped[List["Habit"]] = relationship(back_populates="goal", cascade='save-update, merge, delete',
                                                 passive_deletes=True)


class Habit(Base):
    __tablename__ = "habit"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    goalID: Mapped[int] = mapped_column(ForeignKey("goal.id", ondelete='CASCADE'), nullable=False)
    goal: Mapped["Goal"] = relationship(back_populates="habits")
    habitTracks: Mapped[List["HabitTrack"]] = relationship(back_populates="habit", cascade='save-update, merge, delete',
                                                           passive_deletes=True)


class HabitTrack(Base):
    __tablename__ = "habit_track"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    date: Mapped[str] = mapped_column(String(20), nullable=False)
    is_checked: Mapped[bool]
    habitID: Mapped[int] = mapped_column(ForeignKey("habit.id", ondelete='CASCADE', ), nullable=False)
    habit: Mapped["Habit"] = relationship(back_populates="habitTracks")


class NewsPost(Base):
    __tablename__ = "news_post"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    userID: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="news_posts")
