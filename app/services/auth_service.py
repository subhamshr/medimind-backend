from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,HTTPException,status
from app.core.database import get_db
from app.services.user_service import get_user_by_email
from app.utils.auth_utils import verify_password
from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated
from app.schema.token import TokenData
from jose import jwt, JWTError
from app.models.user import User
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

bearer_schema = HTTPBearer(auto_error=False)

async def authenticate_user(email:str,password:str,session: AsyncSession):
    user= await get_user_by_email(session,email)
    if not user:
        return False
    if not verify_password(password,user.password):
        return False
    return user

def create_access_token(data:dict,expires_delta:timedelta|None=None):
    to_encode = data.copy()
    if expires_delta:
       expire = datetime.now(timezone.utc) + expires_delta
    else:
       expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    
    authorization: HTTPAuthorizationCredentials = Depends(bearer_schema),
    Session = Depends(get_db)
):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
    try:
        if not authorization:
            raise HTTPException(status_code=401,detail="Token not available")
        token=authorization.credentials
        
        if not token:
           raise HTTPException(status_code=401,detail="Token not available")
       
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user =await  get_user_by_email(Session, email=token_data.email)
    if user is None:
        raise credentials_exception          

    return user


async def check_admin_user(
    
    authorization: HTTPAuthorizationCredentials = Depends(bearer_schema),
    Session = Depends(get_db)
):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
    try:
        if not authorization:
            raise HTTPException(status_code=401,detail="Token not available")
        token=authorization.credentials
        
        if not token:
           raise HTTPException(status_code=401,detail="Token not available")
       
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get("sub")
        role=payload.get("role")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        if role != "admin":
            raise HTTPException(status_code=401,detail="Your not an admin")
            
    except JWTError:
        raise credentials_exception
    user =await  get_user_by_email(Session, email=token_data.email)
    if user is None:
        raise credentials_exception          

    return user
