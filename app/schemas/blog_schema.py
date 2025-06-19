from pydantic import BaseModel

class Like_Request(BaseModel):
    blog_id: str