from pydantic import BaseModel
from typing import List, Dict


class Blog(BaseModel):
    user_id: int
    name: str
    content: str
    is_active: bool
    created_at: datetime
    