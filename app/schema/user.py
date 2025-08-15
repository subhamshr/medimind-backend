from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
import uuid


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role:Optional[str] = None

class UserCreate(UserBase):
    password: str
    

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserSchema(UserBase):
    id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)
