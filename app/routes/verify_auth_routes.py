from fastapi import HTTPException, Response, status, APIRouter, Depends
from app.middleware.verify_jwt import verify_jwt
from app.controller.verify_auth_controller import verify_auth


router = APIRouter()

@router.get('/verify-auth')
async def handle_verify_auth(response: Response, user_data: dict = Depends(dependency=verify_jwt)):
    return await verify_auth(response, user_data)
