from fastapi import HTTPException, status
from sympy import det
from app.repositories.otp_repository import save_otp
from app.utils.otp_utils import generate_otp
from app.utils.email_utils import send_otp_email
from app.utils.encryption_utils import incrept_email


async def verify_email(email: str, session)-> bool:
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ID is not found")
    
    encrypted_email = incrept_email(email)
    otp = generate_otp()
    
    
    is_saved = await save_otp(encrypted_email, otp, "email_verification", 10, session)
    if not is_saved:
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not created")
    
    sending_email = send_otp_email(email, otp)
    if "error" in sending_email:
        await session.abort_transaction()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email is not send and account is not created"
        )
        
    return True
    
    