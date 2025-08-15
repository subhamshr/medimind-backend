from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schema.user import UserCreate, UserUpdate
from datetime import datetime, timezone
from app.utils.auth_utils import get_password_hash

async def get_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def get_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_username(session: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user: UserCreate):
    # Check if user with email or username already exists
    existing_user_email = await get_user_by_email(session, user.email)
    if existing_user_email:
        raise ValueError("User with this email already exists")
    
    existing_user_username = await get_user_by_username(session, user.username)
    if existing_user_username:
        raise ValueError("User with this username already exists")
    
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def update_user(session: AsyncSession, user_id: int, user_update: UserUpdate):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    db_user = result.scalar_one_or_none()
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    # Update the updated_at timestamp
    db_user.updated_at = datetime.now(timezone.utc)
    
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def delete_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    db_user = result.scalar_one_or_none()
    if db_user:
        session.delete(db_user)
        await session.commit()
    return db_user
