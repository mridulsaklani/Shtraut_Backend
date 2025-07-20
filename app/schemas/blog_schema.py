from pydantic import BaseModel, EmailStr

class Like_Request(BaseModel):
    blog_id: str
    
