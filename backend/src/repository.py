from typing import Callable

from sqlalchemy import select, update, delete

from src.database import db_session
from src.models.models import Habit, HabitTrack, NewsPost
from src.schemas import GoalID, NewsScheme, \
    HabitDatabaseModel, NewsDatabaseModel


class KeyBuilders:
    @staticmethod
    def custom_key_builder(func: Callable, namespace: str, *args, **kwargs) -> str:
        key = f"{namespace}:{func.__name__}:{':'.join(map(str, args))}:{':'.join([f'{k}:{v}' for k, v in kwargs.items()])}"
        return key


class HabitsRepository:
    def __init__(self):
        pass

    @staticmethod
    async def get_habits(goal_id: int) -> list[HabitDatabaseModel]:
        async with db_session() as session:
            fetch_habits = select(Habit).where(goal_id == Habit.goalID)
            result = await session.execute(fetch_habits)
            habits = result.scalars().all()

            return [HabitDatabaseModel.model_validate(habit) for habit in habits]

    @staticmethod
    async def get_habit(habit_id: int) -> HabitDatabaseModel:
        async with db_session() as session:
            fetch_habits = select(Habit).where(Habit.id == habit_id)
            result = await session.execute(fetch_habits)
            habit = result.scalars().one_or_none()

            return HabitDatabaseModel.model_validate(habit)

    @staticmethod
    async def add_habit(goal_id: GoalID, habit_name: str):
        async with db_session() as session:
            habit = Habit(name=habit_name, goalID=goal_id.id)

            session.add(habit)

            await session.flush()
            await session.commit()

            return habit

    @staticmethod
    async def update_habit(habit_id: int, new_habit_name: str):
        async with db_session() as session:
            updated = update(Habit).where(Habit.id == habit_id).values(name=new_habit_name)
            updated_val = await session.execute(updated)

            await session.flush()
            await session.commit()

            return updated_val

    @staticmethod
    async def delete_habit(habit_id: int):
        async with db_session() as session:
            delete_statement = delete(Habit).where(Habit.id == habit_id)
            deleted_val = await session.execute(delete_statement)

            await session.flush()
            await session.commit()

            return deleted_val


class HabitTrackRepository:
    def __init__(self):
        pass

    @staticmethod
    async def track_habit(habit_id: int, date: str):
        async with db_session() as session:
            existing_habit = select(HabitTrack).filter_by(habitID=habit_id, date=date)
            result = await session.execute(existing_habit)
            habit = result.scalars().one_or_none()

            if habit:
                updated_stmt = update(HabitTrack).where(
                    (HabitTrack.habitID == habit_id) & (HabitTrack.date == date)
                ).values({'is_checked': True})
                await session.execute(updated_stmt)
                await session.commit()
                return habit
            else:
                habit_track_orm = HabitTrack(habitID=habit_id, date=date, is_checked=True)
                session.add(habit_track_orm)
                await session.commit()
                return habit_track_orm

    @staticmethod
    async def untrack_habit(habit_id: int, date: str):
        async with db_session() as session:
            updated_stmt = (
                update(HabitTrack)
                .where((HabitTrack.habitID == habit_id) & (HabitTrack.date == date))
                .values(is_checked=False)
            )

            await session.execute(updated_stmt)

            await session.commit()

            result_proxy = await session.execute(
                select(HabitTrack)
                .where((HabitTrack.habitID == habit_id) & (HabitTrack.date == date))
            )

            result = result_proxy.scalars().one_or_none()

            return result

    @staticmethod
    async def get_habits_by_date(goal_id: int, date: str) -> list[int]:
        async with db_session() as session:
            stmt = (
                select(Habit.id)
                .join(HabitTrack)
                .where(
                    (Habit.goalID == goal_id) &
                    (HabitTrack.date == date) &
                    HabitTrack.is_checked
                )
            )
            result = await session.execute(stmt)

            habits_ids = result.scalars().all()

            # goals_query = select(Goal).where(Goal.userID == user_id)
            # result = await session.execute(goals_query)
            # goal_models = result.scalars().all()
            #
            return habits_ids

    @staticmethod
    async def get_dates_by_habit(habit_id: int) -> list[str]:
        async with db_session() as session:
            stmt = (
                select(HabitTrack.date)
                .where(
                    (HabitTrack.habitID == habit_id) &
                    HabitTrack.is_checked
                )
            )
            result = await session.execute(stmt)

            habit_dates = result.scalars().all()

            # goals_query = select(Goal).where(Goal.userID == user_id)
            # result = await session.execute(goals_query)
            # goal_models = result.scalars().all()

            return habit_dates


class NewsRepository:
    def __init__(self):
        pass

    @staticmethod
    async def post_news(post_data: NewsScheme):
        async with db_session() as session:
            post = NewsPost(title=post_data.title, content=post_data.content, userID=post_data.user_id)

            session.add(post)

            await session.flush()
            await session.commit()

            return post

    @staticmethod
    async def get_news() -> list[NewsDatabaseModel]:
        async with db_session() as session:
            fetch_posts = select(NewsPost)
            result = await session.execute(fetch_posts)
            response = result.scalars().all()

            return [NewsDatabaseModel.model_validate(news_item) for news_item in response]
