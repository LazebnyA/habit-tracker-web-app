from typing import TypeVar, Type, Optional, List, Sequence

from fastapi import HTTPException, Response
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import UserSchema
from src.database import db_session
from src.goal.models import Goal
from src.goal.schemas import GoalCreateSchema, GoalRetrieveSchema

T = TypeVar("T")


async def get_entity_or_404(
        session: AsyncSession,
        entity_id: int,
        EntityModel: Type[T],
        id_field: Optional[str] = "id"
) -> T:
    """
    Asynchronously retrieves an entity by its ID from the database.
    If the entity is not found, raises a 404 HTTP exception.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session used to
            execute the query.
        entity_id (int): The identifier of the entity to retrieve.
        EntityModel (Type[T]): The SQLAlchemy model class representing the
            entity type to query.
        id_field (Optional[str]): The name of the field to use as the identifier
            for the query. Defaults to "id".

    Returns:
        T: The instance of the specified `EntityModel` that matches the
        given `entity_id`.

    Raises:
        ValueError: If the specified `id_field` does not exist in the
            `EntityModel`.
        HTTPException: If no instance of the `EntityModel` is found with the
            specified `entity_id`, a 404 error is raised.
    """
    id_column = getattr(EntityModel, id_field, None)
    if not id_column:
        raise ValueError(f"Model '{EntityModel.__name__}' has no field '{id_field}'.")

    query = select(EntityModel).where(id_column == entity_id)
    result = await session.execute(query)
    instance = result.scalar_one_or_none()

    if not instance:
        raise HTTPException(status_code=404, detail=f"{EntityModel.__name__} not found.")

    return instance


async def get_list_or_404(
        session: AsyncSession,
        entity_id: int,
        EntityModel: Type[T],
        id_field: Optional[str] = "id"
) -> Sequence[T]:
    """
    Asynchronously retrieves a list of instances of a specified entity model
    from the database. If no instances are found, raises a 404 HTTP exception.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session used to
            execute the query.
        entity_id (int): The identifier of the entity to search for.
        EntityModel (Type[T]): The SQLAlchemy model class representing the
            entity type to query.
        id_field (Optional[str]): The name of the field to use as the identifier
            for the query. Defaults to "id".

    Raises:
        ValueError: If the specified `id_field` does not exist in the
            `EntityModel`.
        HTTPException: If no instances of the `EntityModel` are found with the
            specified `entity_id`, a 404 error is raised.

    Returns:
        List[T]: A list of instances of the specified `EntityModel` that match
        the given `entity_id`.
    """
    id_column = getattr(EntityModel, id_field, None)
    if not id_column:
        raise ValueError(f"Model '{EntityModel.__name__}' has no field '{id_field}'.")

    query = select(EntityModel).where(id_column == entity_id)
    result = await session.execute(query)
    instances = result.scalars().all()

    if not instances:
        raise HTTPException(status_code=404, detail=f"{EntityModel.__name__} not found.")

    return instances


class GoalRepository:

    @staticmethod
    async def get_list(user: UserSchema) -> list[GoalRetrieveSchema]:
        async with db_session() as session:
            goals_list = await get_list_or_404(session, user.id, Goal, "user_id")
            return [GoalRetrieveSchema.from_orm(goal) for goal in goals_list]

    @staticmethod
    async def get_by_id(user: UserSchema, goal_id: int) -> GoalRetrieveSchema:
        async with db_session() as session:
            goal = await get_entity_or_404(session, goal_id, Goal, "id")

            if goal.user_id != user.id:
                raise HTTPException(status_code=403, detail="Access denied to this goal.")

            return GoalRetrieveSchema.from_orm(goal)

    @staticmethod
    async def create(
            user: UserSchema, goal: GoalCreateSchema
    ) -> GoalRetrieveSchema:
        async with db_session() as session:
            goal = Goal(name=goal.name, user_id=user.id)

            session.add(goal)

            await session.flush()
            await session.commit()

            return GoalRetrieveSchema.from_orm(goal)

    @staticmethod
    async def update(
            user: UserSchema,
            goal_id: int,
            goal_data: GoalCreateSchema
    ) -> GoalRetrieveSchema:
        async with db_session() as session:
            goal = await get_entity_or_404(session, goal_id, Goal, "id")

            if goal.user_id != user.id:
                raise HTTPException(status_code=403, detail="Access denied to this goal.")

            for key, value in goal_data.model_dump(exclude_unset=True).items():
                setattr(goal, key, value)

            await session.flush()
            await session.commit()

            return GoalRetrieveSchema.from_orm(goal)

    @staticmethod
    async def delete(goal_id: int, user: UserSchema) -> bool:
        async with db_session() as session:
            goal = await get_entity_or_404(session, goal_id, Goal, "id")

            if goal.user_id != user.id:
                raise HTTPException(status_code=403, detail="Access denied to this goal.")

            await session.delete(goal)
            await session.commit()

            return True
