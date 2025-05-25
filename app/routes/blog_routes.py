from fastapi import Response, HTTPException, APIRouter, Depends
from app.model.blog_model import Blog
from app.controller.blog_controller import add_blog
from app.middleware.verify_jwt import verify_jwt

router = APIRouter()


@router.post('/add')
async def handle_blog_upload(blog: Blog, response: Response, user_data: dict = Depends(verify_jwt)):
    return await add_blog(blog, response, user_data)