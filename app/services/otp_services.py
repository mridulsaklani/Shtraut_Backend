from fastapi import HTTPException, status
from app.utils.hash_utils import hash_email
from app.config.database import otp_collection
from app.exceptions.custom_otp_exceptions import OTPNotFountException


async def find_email_verification_otp(email: str)-> int:
    email_hash = hash_email(email)
    db_otp = await otp_collection.find_one({"email_hash": email_hash, "type": "email_verification"}, sort=[("created_at", -1)])
    if not db_otp:
        raise OTPNotFountException()
    
    otp = db_otp.get("otp")
    
    return int(otp)
    
    
    