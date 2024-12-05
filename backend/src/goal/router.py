from datetime import datetime

from fastapi import Depends, APIRouter
from redis.asyncio.client import Redis
from starlette.responses import JSONResponse

from src.auth.dependencies import UserGetterByToken, ACCESS_TOKEN_TYPE
from src.auth.schemas import UserSchema
from src.goal.repository import GoalRepository
from src.goal.schemas import GoalCreateSchema, GoalRetrieveSchema

router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)

redis = Redis()


def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {obj.__class__.__name__} not serializable")


# @router.get("/get", response_model=list[GoalDatabaseModel])
# async def get_goals(user: UserEmail = Depends()):
#     try:
#         cache = await redis.get(user.email)
#         if cache:
#             print("cache found")
#             return json.loads(cache)
#         else:
#             print("cache not found")
#             goals_list = await GoalRepository.get_goals(user)
#             await redis.set(user.email, json.dumps([goal.dict() for goal in goals_list], default=custom_serializer))
#             return goals_list
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@router.get("", response_model=list[GoalRetrieveSchema])
async def get_goals(
        user: UserSchema = Depends(UserGetterByToken(ACCESS_TOKEN_TYPE)),
) -> list[GoalRetrieveSchema]:
    goals_data = await GoalRepository.get_list(user)
    return goals_data


@router.post("", response_model=GoalRetrieveSchema)
async def create_goal(
        goal_data: GoalCreateSchema,
        user: UserSchema = Depends(UserGetterByToken(ACCESS_TOKEN_TYPE))
) -> GoalRetrieveSchema:
    goal_data = await GoalRepository.create(user, goal_data)
    return goal_data


@router.put("/{goal_id}", response_model=GoalRetrieveSchema)
async def update_goal(
        goal_id: int,
        goal_data: GoalCreateSchema,
        user: UserSchema = Depends(UserGetterByToken(ACCESS_TOKEN_TYPE)),
) -> GoalRetrieveSchema:
    goal_data = await GoalRepository.update(user, goal_id, goal_data)
    return goal_data


@router.delete("/{goal_id}", response_model=GoalRetrieveSchema)
async def delete_goal(
        goal_id: int,
        user: UserSchema = Depends(UserGetterByToken(ACCESS_TOKEN_TYPE)),
) -> JSONResponse:
    await GoalRepository.delete(goal_id, user)

    return JSONResponse(
        content={"detail": "Goal was successfully deleted"},
        status_code=200
    )

# @router.post("/create")
# async def add_goal(
#         user: UserEmail = Depends(),
#         goal: GoalOrmScheme = Depends()
# ):
#     try:
#         goal_to_add = await GoalRepository.add_goal(user, goal)
#         key = user.email
#         await redis.delete(key)
#         return goal_to_add
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
#
#
# @router.put("/update")
# async def update_goal(
#         goal_id: GoalID = Depends(),
#         new_goal_name: GoalOrmScheme = Depends()
# ):
#     try:
#         response = await GoalRepository.update_goal(goal_id, new_goal_name)
#         user_email = await GoalRepository.get_user_email_by_goal_id(goal_id)
#         key = user_email
#         await redis.delete(key)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
#
#
# @router.delete("/delete")
# async def delete_goal(goal_id: GoalID = Depends()):
#     try:
#         user_email = await GoalRepository.get_user_email_by_goal_id(goal_id)
#         response = await GoalRepository.delete_goal(goal_id)
#         key = user_email
#         await redis.delete(key)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
