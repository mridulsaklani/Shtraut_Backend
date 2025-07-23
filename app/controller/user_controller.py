
from fastapi import HTTPException, Response, status
from app.utils.encryption_utils import incrept_email, decrept_email
from app.model.user_model import User, verifyOPT, UpdateUser
from app.config.database import db
from app.utils.password_utils import hash_password, verify_password
from app.utils.email_utils import send_otp_email
from app.schemas.user_schema import login_Schema, update_email_schema
from app.utils.token_utils import create_access_token, create_refresh_token
from app.utils.otp_utils import generate_otp
from app.services.verify_email_service import verify_email
from app.config.database import client
from bson import ObjectId




user_collection = db["users"]




async def get_all_users(response: Response):
    users = await user_collection.find().to_list(length=100)

    for user in users:
        user["_id"] = str(user["_id"])

    response.status_code = status.HTTP_200_OK
    return {"message": "All users get successfully", "users": users}


async def get_single_user(response: Response, user_data : dict):
    
   if not user_data:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User") 
   
   id = user_data.get('userid')
  
   
   if not id:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User id") 
  
   try:
       id = ObjectId(id)
   except Exception:
       raise HTTPException(status_code=400, detail='User id is not converted into object id')

    
    
   user = await user_collection.find_one({"_id": id}, {'password':0, 'refresh_token': 0})
   
   user['_id'] = str(user['_id'])
   if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User data not found")
   response.status_code = status.HTTP_200_OK
   return {'message': 'User data fetched successfully', 'user': user}

async def get_user_by_id(response: Response, id: str, user_data: dict):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized User')
    
    if not id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=' User ID not found')
    
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=' User ID not transform')
    
    user = await user_collection.find_one({"_id": id}, {'password': 0, 'refresh_token': 0})
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=' User  not found')
    
    user["_id"] = str(user["_id"])
    
    response.status_code = status.HTTP_200_OK
    return {'message': 'user fetched sexfully', "user": user}
    


async def user_register(user: User, response: Response):
    session = await client.start_session()
    try:
        await session.start_transaction()
        
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
    
        
        user_dict = user.model_dump(exclude_none=True)
        user_dict["email"] = incrept_email(user_dict.get("email"))
        user_dict['password'] = hash_password(user_dict['password']) 
        
        await verify_email(user.email, session)
            
        await user_collection.insert_one(user_dict, session=session)
        await session.commit_transaction()
        response.status_code = status.HTTP_201_CREATED
        return {"message": "User registered successfully"}
    except Exception as e:
        await session.abort_transaction()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )
    finally:
        await session.end_session()


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
        "email": user_exist.get("email"),
        'role':user_exist.get('role')
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
    



async def update_user(response: Response,user: UpdateUser,  user_data: dict):
    if not user_data and not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user data and User"
        )
    
    id = user_data.get('userid')
    if not id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID not provided"
        )

    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail='User ID is not a valid ObjectId'
        )
        
    user = user.model_dump(exclude_none=True)

    updated_user = await user_collection.find_one_and_update(
        {"_id": id},
        {"$set": user},
        return_document=True
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not updated"
        )

    updated_user["_id"] = str(updated_user["_id"])  

    response.status_code = status.HTTP_200_OK
    return {
        "message": "User updated successfully",
        "user": updated_user
    }

    
async def change_email_id(data: dict, response: Response, user_data: dict):
   
    
    
    if not user_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")
    
    userId = user_data.get("userid")
    
    try:
        userId: ObjectId(userId)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid object id")
    
    if not userId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")
    
    change_email = data.get("email")
    
    if not change_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email id not found")
    
    
    otp = generate_otp()
    
    
    sending_email = send_otp_email(change_email, otp)
    
    # if()
    
    update_user = await user_collection.update_one({"email", change_email, {"$set":{"otp": otp}}})
    
    
    
    
    
        
    
async def logout_user(response: Response, user: dict):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User data not found")
    
    id = user.get("userid")
    if not id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User id not found")
    
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id is invalid")
    
    
    logged_user = await user_collection.find_one_and_update({"_id": id},{"$set":{"status": False, "refresh_token": None}})
    
    if not logged_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not logged out")
    
    response.delete_cookie(key="access-token", httponly=True, secure=True, samesite="none")
    response.delete_cookie(key='refresh-token', httponly=True, secure=True, samesite="none")
    
    response.status_code = status.HTTP_200_OK
    return {"message": "User logged out successfully"}