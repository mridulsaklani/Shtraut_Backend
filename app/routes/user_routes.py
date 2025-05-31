from fastapi import APIRouter, Response, status, Depends, Body
from app.model.user_model import User, verifyOPT, UpdateUser
from app.controller.user_controller import user_register, get_all_users, get_single_user, verify_OTP, login_user, logout_user, update_user, get_user_by_id
from app.schemas.user_schema import login_Schema
from app.middleware.verify_jwt import verify_jwt

router = APIRouter()


@router.get('/all-users', status_code= status.HTTP_200_OK)
async def fetch_all_users(response: Response):
    return await get_all_users(response)

@router.get('/single-user')
async def fetch_single_user(response: Response, user_data: dict = Depends(verify_jwt)):
    return await get_single_user(response, user_data)

@router.get('/user-profile/{id}')
async def get_user_by_ids(response: Response, id: str,  user_data: dict = Depends(verify_jwt)):
    return await get_user_by_id(response, id, user_data)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def handle_user_register(user: User, response: Response):
    return await user_register(user, response)

@router.patch("/verify-otp", status_code=status.HTTP_200_OK)
async def handle_otp_verification(user: verifyOPT, response: Response):
    return await verify_OTP(user, response)

@router.post('/login')
async def handle_user_login(user:login_Schema, response: Response):
    return await login_user(user, response)

@router.post('/logout')
async def handle_user_logout(response: Response, user : dict = Depends(dependency=verify_jwt)):
    return await logout_user(response, user)

@router.patch('/update')
async def handle_update_user(
    response: Response,
    user: UpdateUser = Body(...), 
    user_Data: dict = Depends(verify_jwt)):
    return await update_user( response , user, user_Data)


