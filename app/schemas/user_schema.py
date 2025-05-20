from pydantic import BaseModel, EmailStr


class login_Schema(BaseModel):
    email: EmailStr
    password: str