

from enum import Enum


class OccupationEnum(str, Enum):
    student = "student"
    employed = "employed"
    unemployed = "unemployed"

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    
class otp_type_enum(str, Enum):
    email_verification = "email_verification",
    password_reset = "password_reset"