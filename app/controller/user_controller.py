from fastapi import HTTPException, Response, status
from app.model.user_model import User, verifyOPT
from app.config.database import db
from app.utils.manage_password import hash_password, verify_password
from app.utils.verification_otp import send_otp_email
from app.schemas.user_schema import login_Schema
from app.utils.generate_token import create_access_token, create_refresh_token
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
    
    missing_field = []
    if not user.email:
        missing_field.append("email")
    if not user.password:
        missing_field.append("password")
        
    if missing_field:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing fields: {", ".join(missing_field)}")
        
        
    user_exist = await user_collection.find_one({"email": user.email})
    
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email Id, please check you mail")
    
    password = user_exist.get("password")
    
    check_password = verify_password(user.password, password)
    
    if not check_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password does not match, please try again")
    
    payload = {
        "_id": str(user_exist.get("_id")),
        "email": user_exist.get("email")
    }
    
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)
    
    email_verified = user_exist.get("email_verified")
    
    if not email_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your email is not verified")
    
    update_user = await user_collection.find_one_and_update(
        {"email": user.email}, {"$set":{"status": True, "refresh_token": refresh_token}}
    )
    
    if not update_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is not logged in')
    
    response.status_code = status.HTTP_200_OK
    response.set_cookie(key="access-token", value=access_token, httponly=True, secure=True, samesite="none")
    response.set_cookie(key="refresh-token", value=refresh_token, httponly=True, secure=True, samesite='none')
    
    return {"message": f"{user.email} User login successfully"}
    
    
async def logout_user(response: Response, user: dict):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User data not found")
    
    id = user.get("userid")
    if not id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User id not found")
    print("secod: ",id)
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id is invalid")
    print(id)
    
    logged_user = await user_collection.find_one_and_update({"_id": id},{"$set":{"status": False, "refresh_token": None}})
    
    if not logged_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not logged out")
    
    response.delete_cookie(key="access-token", httponly=True, secure=True, samesite="none")
    response.delete_cookie(key='refresh-token', httponly=True, secure=True, samesite="none")
    
    response.status_code = status.HTTP_200_OK
    return {"message": "User logged out successfully"}