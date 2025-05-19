from fastapi import APIRouter, Response, status
from app.model.user_model import User
from app.controller.user_controller import user_register, get_all_users

router = APIRouter()


@router.get('/all-users', status_code= status.HTTP_200_OK)
async def fetch_all_users(response: Response):
    return await get_all_users(response)
        

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def handle_user_register(user: User, response: Response):
    return await user_register(user, response)

