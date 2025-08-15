from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import get_user_by_email
from app.core.database import get_db
from app.services.auth_service import create_access_token,get_current_user,authenticate_user
from fastapi.security import OAuth2PasswordRequestForm
from app.schema.token import Token
from typing import Annotated

token_router = APIRouter(tags=['token']) 


@token_router.get("/login")
async def login(email: str, password: str, session: AsyncSession = Depends(get_db)):
    user = await authenticate_user(email,password,session)
    if user is False:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={
        "sub": user.email,
        "role": user.role  # Assuming 'user.role' exists
    })
    return {"access_token": access_token, "token_type": "bearer"}


