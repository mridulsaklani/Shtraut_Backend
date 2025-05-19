from fastapi import HTTPException, Response, status
from app.model.user_model import User
from app.config.database import db
from app.utils.manage_password import hash_password


user_collection = db["users"]


async def get_all_users(response: Response):
    user = await user_collection.find().to_list(length=100)
    response.status_code = status.HTTP_200_OK
    return {"message": "All users get successfully", "users":user}
    

async def user_register(user: User, response: Response):
    user_exist = await user_collection.find_one({"email": user.email})
    if user_exist:
        raise HTTPException(status_code=400, detail="User already exist")
    
    user_dict = user.model_dump()
    user_dict['password'] = hash_password(user_dict['password']) 
    await user_collection.insert_one(user_dict)
    response.status_code = status.HTTP_201_CREATED
    return {"message": "User registered successfully"}
