from fastapi import HTTPException, status

from app.model.otp_model import Verify_otp_model
from datetime import UTC, datetime, timedelta
from app.config.database import otp_collection




async def save_otp(email: str, otp: int, value: str, expiry_minute: int = 10, session=None)-> bool:
    expiration = datetime.now(UTC) + timedelta(minutes=expiry_minute)
    
    otp_data = Verify_otp_model(email=email, otp=otp, type=value, expiration=expiration, created_at=datetime.now(UTC))
    try:
        result =  await otp_collection.insert_one(otp_data.model_dump(), session=session)
        print(result.acknowledged)
        return result.acknowledged
    
    except Exception:
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not created")
    
