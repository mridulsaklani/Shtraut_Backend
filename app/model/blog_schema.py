from pydantic import BaseModel,Field
from typing import List, Dict
from datetime import datetime


class Blog(BaseModel):
   
    name: str = Field(...,min_length=3, max_length=45, description="Employee Name")
    content: str = Field(...,max_length=35)
    is_active: bool = Field(default=False)
    category: List[str] = "nothing"
    created_at: datetime.utcnow
  
    