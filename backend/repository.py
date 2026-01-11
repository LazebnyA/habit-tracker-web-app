from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from starlette import status

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from models.database import User, Goal, Habit, HabitTrack, NewsPost

from schemas import (
    UserRegScheme,
    UserSignInScheme,
    GoalOrmScheme,
    UserEmail,
    GoalID,
    NewsScheme,
)

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class UserNotFoundException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def verify_email(self, email: str) -> bool:
        query = select(User).filter(User.email == email)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()

        return bool(user)

    async def add_user(self, data: UserRegScheme):
        if not await self.verify_email(data.email):
            user_dict = data.model_dump()
            user_dict.popitem()

            user = User(**user_dict)

            user_dict.popitem()

            self.session.add(user)

            await self.session.flush()
            await self.session.commit()

            user_info = {
                "firstName": user_dict["firstName"],
                "lastName": user_dict["lastName"],
                "email": user_dict["email"],
            }

            return user_info
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with the provided email already exists",
            )

    async def verify_account(self, data: UserSignInScheme):
        query = select(User).filter(User.email == data.email)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()

        if user and data.password == user.password:
            user_info = {
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email,
            }
            return user_info
        elif user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with the provided email and password does not exist",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with the provided email does not exist",
            )


class GoalRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    async def get_goals(cls, user: UserEmail):
        async with new_session() as session:
            fetch_id = select(User.id).where(user.email == User.email)
            result = await session.execute(fetch_id)
            user_id = result.scalars().one_or_none()

            goals_query = select(Goal).where(Goal.userID == user_id)
            result = await session.execute(goals_query)
            goal_models = result.scalars().all()

            return goal_models

    @classmethod
    async def add_goal(cls, user_data: UserEmail, goal_data: GoalOrmScheme):
        async with new_session() as session:
            fetch_id = select(User.id).where(user_data.email == User.email)
            result = await session.execute(fetch_id)
            user_id = result.scalars().one_or_none()

            goal = Goal(name=goal_data.name, userID=user_id)

            session.add(goal)

            await session.flush()
            await session.commit()

            return goal

    @classmethod
    async def update_goal(cls, goal_id: GoalID, goal_data: GoalOrmScheme):
        async with new_session() as session:
            updated = (
                update(Goal).where(Goal.id == goal_id.id).values(name=goal_data.name)
            )
            updated_val = await session.execute(updated)

            await session.flush()
            await session.commit()

            return updated_val

    @classmethod
    async def delete_goal(cls, goal_id: GoalID):
        async with new_session() as session:
            delete_statement = delete(Goal).where(Goal.id == goal_id.id)
            deleted_val = await session.execute(delete_statement)

            await session.flush()
            await session.commit()

            return deleted_val


class HabitsRepository:
    @classmethod
    async def get_habits(cls, goal_id: GoalID):
        async with new_session() as session:
            fetch_habits = select(Habit).where(goal_id.id == Habit.goalID)
            result = await session.execute(fetch_habits)
            habits = result.scalars().all()

            return habits

    @classmethod
    async def get_habit(cls, habit_id: int):
        async with new_session() as session:
            fetch_habits = select(Habit).where(Habit.id == habit_id)
            result = await session.execute(fetch_habits)
            habits = result.scalars().one_or_none()

            return habits

    @classmethod
    async def add_habit(cls, goal_id: GoalID, habit_name: str):
        async with new_session() as session:
            habit = Habit(name=habit_name, goalID=goal_id.id)

            session.add(habit)

            await session.flush()
            await session.commit()

            return habit

    @classmethod
    async def update_habit(cls, habit_id: int, new_habit_name: str):
        async with new_session() as session:
            updated = (
                update(Habit).where(Habit.id == habit_id).values(name=new_habit_name)
            )
            updated_val = await session.execute(updated)

            await session.flush()
            await session.commit()

            return updated_val

    @classmethod
    async def delete_habit(cls, habit_id: int):
        async with new_session() as session:
            delete_statement = delete(Habit).where(Habit.id == habit_id)
            deleted_val = await session.execute(delete_statement)

            await session.flush()
            await session.commit()

            return deleted_val


class HabitTrackRepository:
    @classmethod
    async def track_habit(cls, habit_id: int, date: str):
        async with new_session() as session:
            existing_habit = select(HabitTrack).filter_by(habitID=habit_id, date=date)
            result = await session.execute(existing_habit)
            habit = result.scalars().one_or_none()

            if habit:
                updated_stmt = (
                    update(HabitTrack)
                    .where((HabitTrack.habitID == habit_id) & (HabitTrack.date == date))
                    .values({"is_checked": True})
                )
                await session.execute(updated_stmt)
                await session.commit()
                return habit
            else:
                habit_track_orm = HabitTrack(
                    habitID=habit_id, date=date, is_checked=True
                )
                session.add(habit_track_orm)
                await session.commit()
                return habit_track_orm

    @classmethod
    async def untrack_habit(cls, habit_id: int, date: str):
        async with new_session() as session:
            updated_stmt = (
                update(HabitTrack)
                .where((HabitTrack.habitID == habit_id) & (HabitTrack.date == date))
                .values(is_checked=False)
            )

            await session.execute(updated_stmt)

            await session.commit()

            result_proxy = await session.execute(
                select(HabitTrack).where(
                    (HabitTrack.habitID == habit_id) & (HabitTrack.date == date)
                )
            )

            result = result_proxy.scalars().one_or_none()

            return result

    @classmethod
    async def get_habits_by_date(cls, goal_id: int, date: str):
        async with new_session() as session:
            stmt = (
                select(Habit.id)
                .join(HabitTrack)
                .where(
                    (Habit.goalID == goal_id)
                    & (HabitTrack.date == date)
                    & HabitTrack.is_checked
                )
            )
            result = await session.execute(stmt)

            habits_ids = result.scalars().all()

            # goals_query = select(Goal).where(Goal.userID == user_id)
            # result = await session.execute(goals_query)
            # goal_models = result.scalars().all()
            #
            return habits_ids

    @classmethod
    async def get_dates_by_habit(cls, habit_id: int):
        async with new_session() as session:
            stmt = select(HabitTrack.date).where(
                (HabitTrack.habitID == habit_id) & HabitTrack.is_checked
            )
            result = await session.execute(stmt)

            habits_ids = result.scalars().all()

            # goals_query = select(Goal).where(Goal.userID == user_id)
            # result = await session.execute(goals_query)
            # goal_models = result.scalars().all()
            #
            return habits_ids


class NewsRepository:
    @classmethod
    async def post_news(cls, post_data: NewsScheme):
        async with new_session() as session:
            post = NewsPost(
                title=post_data.title,
                content=post_data.content,
                userID=post_data.user_id,
            )

            session.add(post)

            await session.flush()
            await session.commit()

            return post

    @classmethod
    async def get_news(cls):
        async with new_session() as session:
            fetch_posts = select(NewsPost)
            result = await session.execute(fetch_posts)
            response = result.scalars().all()

            return response
