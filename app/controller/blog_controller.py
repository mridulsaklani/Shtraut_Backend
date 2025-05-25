from fastapi import HTTPException, Response, status
from app.config.database import db
from app.model.blog_model import Blog


blog_collection = db["blogs"]



async def add_blog(blog:Blog, response: Response, user_data: dict):
    if not blog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog data not found")
    
    userId = user_data.get('userid')
    if not userId:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User")
    
    
    blogs = blog.model_dump()
    
    blogs.update({"createdBy": userId})
    
    create = await blog_collection.insert_one(blogs)
    
    if not create:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog collection not created")
    
    response.status_code = status.HTTP_200_OK
    return {"message": "Blog created successfully"}
    
    