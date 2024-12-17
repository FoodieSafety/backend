from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    created_at: datetime

class UserUpdate(UserBase):
    updated_at: datetime

class UserLogin(UserBase):
    password: str

# For validating token
class Token(BaseModel):
    access_token: str
    token_type: str

# The data to embed in the token
class TokenData(BaseModel):
    user_id: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]