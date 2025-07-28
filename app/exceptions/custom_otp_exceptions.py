
from fastapi import HTTPException, status
        
class OTPNotFountException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OTP is expired, please regenerate OPT"
        )
        


class invalidOtpException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid otp, please try again"
        )
        