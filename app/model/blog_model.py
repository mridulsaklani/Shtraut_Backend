from pydantic import BaseModel,Field
from typing import List, Dict, Any
from datetime import datetime
from enum import Enum
from bson import ObjectId

class category_enum(str,Enum):
    tech = "tech"
    lifestyle = "lifestyle"
    education = "education"
    travel = "travel"
    

    
    
class Blog(BaseModel):
   
    title: str = Field(...,min_length=3, max_length=45, description="Employee Name")
    content: str = Field(...,max_length=3000)
    is_active: bool = Field(default=True)
    category: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    likes: int = Field(default=0,description="Likes on blog")
    createdBy: str = None
  
    