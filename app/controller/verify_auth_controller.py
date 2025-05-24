from fastapi import Response, HTTPException, status
from app.config.database import db
from bson import ObjectId

user_collection = db["users"]


async def verify_auth(response: Response, user_data: dict):
    userId = user_data.get("userid")
    if not userId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id not found")
    
    try:
        userId = ObjectId(userId)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User id not converted into Object Id")
    
    user = await user_collection.find_one({"_id": userId},{"password":0, "refresh_token": 0})
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user["_id"] = str(user["_id"])
    
    response.status_code = status.HTTP_200_OK
    return {"isAuthenticated": True, "user": user}
