from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime


class OccupationEnum(str, Enum):
    student = "student"
    employed = "employed"
    unemployed = "unemployed"

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    
class verifyOPT(BaseModel):
    email: EmailStr
    otp: int 
    
    
    
class UpdateUser(BaseModel):
    name: Optional[str] = Field(None, min_length=6, max_length=32)
    username: Optional[str] = Field(None, min_length=6, max_length=35)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    occupation: Optional[OccupationEnum] = None
    status: Optional[bool] = None
    email_verified: Optional[bool] = None
    role: Optional[RoleEnum] = None
    
    refresh_token: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class User(BaseModel):
    name: str = Field(..., min_length=6, max_length=32, description="Name" )
    username: str = Field(..., min_length=6, max_length=35, description="User name")
    email: EmailStr = Field(..., description="User email ID")
    password: str = Field(..., min_length=8)
    occupation: OccupationEnum = Field(..., description="Your occupation")
    status: bool = False
    email_verified: bool = Field(default=False)
    role: RoleEnum = RoleEnum.user
    otp: Optional[int] = Field(default=None)

    refresh_token: str = Field(default=None)
    

   
    @field_validator("username", mode="before")
    @classmethod
    def no_spaces(cls, v):
        if " " in v:
            raise ValueError("Username cannot contain spaces")
        return v

    # @field_validator("password", mode="before")
    # @classmethod
    # def strong_password(cls, v):
    #     if len(v) < 8:
    #         raise ValueError("Password must be at least 8 characters long")
    #     if not re.search(r"[A-Z]", v):
    #         raise ValueError("Password must contain at least one uppercase letter")
    #     if not re.search(r"[0-9]", v):
    #         raise ValueError("Password must contain at least one number")
    #     if not re.search(r"[a-z]", v):
    #         raise ValueError("Password must contain at least one lowercase letter")
    #     return v
