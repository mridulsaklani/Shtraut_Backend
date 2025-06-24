from fastapi import Response, HTTPException, APIRouter, Depends
from app.model.blog_model import Blog
from app.controller.blog_controller import add_blog, get_all_blogs, user_blog_count, like, handle_unlike
from app.middleware.verify_jwt import verify_jwt
from app.model.blog_model import Like_Request

router = APIRouter()


@router.post('/add')
async def handle_blog_upload(blog: Blog, response: Response, user_data: dict = Depends(verify_jwt)):
    return await add_blog(blog, response, user_data)


@router.get('/get-all-blogs')
async def handle_all_blog_fetch( response:Response, user_data:dict = Depends(verify_jwt)):
    return await get_all_blogs( response, user_data)

@router.get('/get_blog_count')
async def handle_blog_count(response: Response, user_data: dict = Depends(verify_jwt)):
    return await user_blog_count(response, user_data)

@router.patch('/like')
async def handle_like(data: Like_Request, response: Response, user_data: dict = Depends(verify_jwt)):
    return await like(data, response, user_data)

@router.patch('/unlike')
async def handle_unliked(data: Like_Request, response:Response, user_data: dict = Depends(verify_jwt)):
    return await handle_unlike(data, response, user_data)