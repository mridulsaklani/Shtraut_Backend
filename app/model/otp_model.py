from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

from app.model.enums import otp_type_enum



    

class Verify_otp_model(BaseModel):
    email: str
    otp: int
    type: otp_type_enum
    expiration: datetime
    created_at: datetime