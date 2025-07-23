from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime


class otp_type_enum(str, Enum):
    email_verification = "email_verification",
    password_reset = "password_reset",
    

class Verify_otp_model(BaseModel):
    email: EmailStr
    otp: int
    type: otp_type_enum
    expiration: datetime
    created_at: datetime