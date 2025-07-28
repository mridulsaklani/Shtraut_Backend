import stat
from fastapi import HTTPException, status


class UserAlreadyExistsException(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            
            detail=f"User already exists with this {email} email please use different one"
        )
        
class UserNameAlreadyExist(HTTPException):
    def __init__(self, name:str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{name} username already exist, please use different Username"
        )
        
class EmailVerificationException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your email is not verified"
        )
