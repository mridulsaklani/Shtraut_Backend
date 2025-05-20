from fastapi import APIRouter, Response, status
from app.model.user_model import User, verifyOPT
from app.controller.user_controller import user_register, get_all_users, verify_OTP

router = APIRouter()


@router.get('/all-users', status_code= status.HTTP_200_OK)
async def fetch_all_users(response: Response):
    return await get_all_users(response)
        

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def handle_user_register(user: User, response: Response):
    return await user_register(user, response)

@router.patch("/verify-otp", status_code=status.HTTP_200_OK)
async def handle_otp_verification(user: verifyOPT, response: Response):
    return await verify_OTP(user, response)