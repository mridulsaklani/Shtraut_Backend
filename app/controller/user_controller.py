from fastapi import HTTPException, Response, status
from app.model.user_model import User, verifyOPT
from app.config.database import db
from app.utils.manage_password import hash_password, verify_password
from app.utils.verification_otp import send_otp_email
from app.schemas.user_schema import login_Schema
from bson import ObjectId
import random
import math


user_collection = db["users"]

def generate_otp():
    otp = math.floor(100000 + random.random() * 900000)
    return otp


async def get_all_users(response: Response):
    users = await user_collection.find().to_list(length=100)

    for user in users:
        user["_id"] = str(user["_id"])

    response.status_code = status.HTTP_200_OK
    return {"message": "All users get successfully", "users": users}

async def user_register(user: User, response: Response):
    user_exist = await user_collection.find_one({"email": user.email})
    
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exist, use different email" 
        )
    user_name_exist = await user_collection.find_one({"username": user.username})  
    if user_name_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username already exist, use different one"
        )
    otp = generate_otp()
    user_dict = user.model_dump()
    user_dict['password'] = hash_password(user_dict['password']) 
    user_dict['otp'] = otp
    user_dict["status"] = False
    sending_email = send_otp_email(user.email, otp)
    
    if "error" in sending_email:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email is not send and account is not created"
        )
        
    
    await user_collection.insert_one(user_dict)
    response.status_code = status.HTTP_201_CREATED
    return {"message": "User registered successfully"}

async def login(user: User, response: Response):
    
    user_exist = await user_collection.find_one({"email": user.email})
    if not user_exist:
        raise HTTPException(status_code=400, detail="User does not exist")
    
    if(user_exist['email_verified'] == False):
        return HTTPException(status_code=401, detail="OTP is not verified")
    
    if not verify_password(user.password, user_exist["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    user_exist["_id"] = str(user_exist["_id"])
    
    await user_collection.update_one(
        {"email": user.email},
        {"$set": {"status": "active"}}
    )

    response.status_code = status.HTTP_200_OK
    return {"message": "Login successful", "user": user_exist}



async def verify_OTP(user: verifyOPT, response: Response):
    new_user = await user_collection.find_one({"email": user.email})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    otp = new_user['otp']
    
    if not otp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User OTP not fetched from db")
    
    if(int(otp) != int(user.otp)):
        raise HTTPException(status_code=401, detail="OTP Does not matched")
    
    await user_collection.update_one({"email": user.email}, {"$set":{"email_verified": True}, "$unset": {"otp": ""}})
    
    response.status_code = status.HTTP_200_OK
    return {"message": "OTP verified successfully"}


async def login_user(user: login_Schema, response: Response):
    user_exist = await user_collection.find_one({"email": user.email})
    
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email Id, please check you mail")
    
    check_password = verify_password(user.password, user_exist['password'])
    
    if not check_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password does not match, please try again")
    
    
        