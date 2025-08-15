from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.schema.user import UserSchema, UserCreate, UserUpdate
from app.services.user_service import get_users, create_user, get_user, delete_user, update_user

user_router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@user_router.get('/', response_model=list[UserSchema])
async def get_users_list(session: AsyncSession = Depends(get_db)):
    db_users = await get_users(session)
    return db_users

@user_router.get('/{user_id}', response_model=UserSchema)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db)):
    db_user = await get_user(session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user

@user_router.delete('/{user_id}')
async def delete_user_by_id(user_id: int, session: AsyncSession = Depends(get_db)):
    db_user = await get_user(session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await delete_user(session, db_user.id)
    return {"message": "User deleted"}


@user_router.put('/{user_id}', response_model=UserSchema)
async def update_user_by_id(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_db)):
    db_user = await update_user(session, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.post("/", response_model=UserSchema)
async def create_new_user(user: UserCreate, session: AsyncSession = Depends(get_db)):
    try:
        return await create_user(session, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
