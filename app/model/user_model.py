from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from enum import Enum
import re


class OccupationEnum(str, Enum):
    student = "student"
    employed = "employed"
    unemployed = "unemployed"

class User(BaseModel):
    name: str = Field(..., min_length=6, max_length=32, description="Name")
    username: str = Field(..., min_length=6, max_length=35, description="User name")
    email: EmailStr = Field(..., description="User email ID")
    password: str
    occupation: OccupationEnum
    status: bool = Field(default=False)
    email_verified: bool = Field(default=False)

    @field_validator("username")
    @classmethod
    def no_spaces(cls, v):
        if " " in v:
            raise ValueError("Username cannot contain spaces")
        return v

    @field_validator("password")
    @classmethod
    def strong_password(cls, v):
       
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v
