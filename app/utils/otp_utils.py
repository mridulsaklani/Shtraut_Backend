import math
import random 
from fastapi import HTTPException

def generate_otp()-> int:
    otp = math.floor(100000 + random.random() * 900000)
    return otp

def compare_otp(db_otp, user_otp)-> bool:
    if(int(db_otp) != int(user_otp)):
        raise HTTPException(status_code=401, detail="OTP Does not matched")
    
    return True