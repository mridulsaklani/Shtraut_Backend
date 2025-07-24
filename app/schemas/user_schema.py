from pydantic import BaseModel, EmailStr, Field
from app.model.enums import OccupationEnum, RoleEnum


class login_Schema(BaseModel):
    email: EmailStr
    password: str
    
class update_email_schema(BaseModel):
    email: EmailStr
    
    
class user_register_schema(BaseModel):
    name: str = Field(..., min_length=8)
    username: str = Field(..., min_length=8)
    email: EmailStr = Field(..., min_length=8)
    password: str = Field(..., min_length=8)
    occupation: OccupationEnum
    