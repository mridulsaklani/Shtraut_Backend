from pydantic import BaseModel, EmailStr


class login_Schema(BaseModel):
    email: EmailStr
    password: str
    
class update_email_schema(BaseModel):
    email: EmailStr