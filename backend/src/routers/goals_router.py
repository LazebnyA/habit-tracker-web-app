from fastapi import Depends, APIRouter, HTTPException
from fastapi_cache.decorator import cache
from redis.asyncio.client import Redis

from src.repository import GoalRepository, KeyBuilders
from src.schemas import GoalOrmScheme, UserEmail, GoalID, GoalDatabaseModel

router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)

redis = Redis()


@router.get("/get", response_model=list[GoalDatabaseModel])
@cache(expire=3600, namespace="goals", key_builder=KeyBuilders.custom_key_builder)
async def get_goals(
        user: UserEmail = Depends()
):
    goals_list = await GoalRepository.get_goals(user)
    return goals_list


@router.post("/create")
async def add_goal(
        user: UserEmail = Depends(),
        goal: GoalOrmScheme = Depends()
):
    goal_to_add = await GoalRepository.add_goal(user, goal)

    # Clear cache for the specific user
    pattern = f"goals:get_goals:{user.email}:*"
    async for key in redis.scan_iter(match=pattern):
        await redis.delete(key)

    return goal_to_add


@router.put("/update")
async def update_goal(
        goal_id: GoalID = Depends(),
        new_goal_name: GoalOrmScheme = Depends()
):
    try:
        response = await GoalRepository.update_goal(goal_id, new_goal_name)
        user_email = await GoalRepository.get_user_email_by_goal_id(goal_id)
        # Clear cache for the specific goal
        pattern = f"goals:get_goals:{user_email}:*"
        async for key in redis.scan_iter(match=pattern):
            await redis.delete(key)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete")
async def delete_goal(goal_id: GoalID = Depends()):
    try:
        response = await GoalRepository.delete_goal(goal_id)
        user_email = await GoalRepository.get_user_email_by_goal_id(goal_id)
        # Clear cache for the specific goal
        pattern = f"goals:get_goals:{user_email}:*"
        async for key in redis.scan_iter(match=pattern):
            await redis.delete(key)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))