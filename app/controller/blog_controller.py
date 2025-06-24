from turtle import update
from fastapi import HTTPException, Response, status
from pymongo import ReplaceOne
from app.config.database import db
from app.model.blog_model import Blog
from app.model.blog_model import Like_Request
from bson import ObjectId


blog_collection = db["blogs"]

def convert_objectid(obj):
    if isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj



async def add_blog(blog:Blog, response: Response, user_data: dict):
    if not blog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog data not found")
    
    userId = user_data.get('userid')
    if not userId:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User")
    
    
    blogs = blog.model_dump()
    
    try:
      userId = ObjectId(userId)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User id is not converted as Object Id id')
    
    blogs.update({"createdBy": userId})
    
    create = await blog_collection.insert_one(blogs)
    
    if not create:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog collection not created")
    
    response.status_code = status.HTTP_200_OK
    return {"message": "Blog created successfully"}
    


async def get_all_blogs(response: Response, user_data: dict):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    
    user_id = user_data.get('userid')
    
    # try:
    #     user_id =  ObjectId(user_id)
    # except Exception:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid ID')

    pipeline = [
        {
            "$addFields": {
                "createdByObjId": {
                    "$toObjectId": "$createdBy"
                }
            }
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "createdByObjId",
                "foreignField": "_id",
                "as": "creator"
            }
        },
        {
            "$unwind": {
                "path": "$creator",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
        "$sort": {
            "created_at": -1  
        }
        }
    ]

    blog_data = await blog_collection.aggregate(pipeline).to_list(length=None)
   

   
    blog_data = [convert_objectid(blog) for blog in blog_data]
    
    for blog in blog_data:
        if "creator" in blog:
            blog["creator"].pop("password", None)
            blog["creator"].pop("refresh_token", None)
        
        blog['isLiked'] = False
        if user_id in blog.get('likedBy'):
           blog['isLiked'] = True
        
            
            

    response.status_code = status.HTTP_200_OK
    return {
        "message": "Blogs with user data fetched successfully",
        "blogdata": blog_data
    }
    
    
async def user_blog_count(response: Response, user_data: dict):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")
    
    id = user_data.get('userid')
    
    
    
    try:
        id = ObjectId(id)
        
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='object id issue')
    
    data = await blog_collection.aggregate([
        
        {
            "$match":{
            "createdBy": id
        }
        },
        {
            "$count": 'blogCount'
        }
    ]).to_list(length=1)
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No blogs found for this user')
 
    
    count = data[0].get('blogCount')
    
    if not count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog count not found')
        
    response.status_code = status.HTTP_200_OK
    return {"message": "Count get successfully", "count": count}


async def like(data: Like_Request, response: Response, user_data:dict):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    data = data.model_dump()
    
    blog_id = data.get('blog_id')
    
    if not blog_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog ID not found")
    
    user_id = user_data.get('userid')
    
    try:
        user_id = ObjectId(user_id)
        blog_id = ObjectId(blog_id)
    except Exception:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid IDs')
     
    blog = await blog_collection.find_one({"_id": blog_id})
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog data not found")
    
    if user_id in blog.get('likedBy'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already like it")
    
    update = await blog_collection.update_one({"_id": blog_id}, {"$addToSet":{"likedBy":user_id}, "$inc": {'likes':1}})
    
    if not update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to like')
    
    response.status_code = status.HTTP_200_OK
    return {"message": "Blog liked successfully"}

async def handle_unlike(data: Like_Request, response: Response, user_data:dict):
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    data = data.model_dump()
    
    blog_id = data.get('blog_id')
    
    if not blog_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog ID not found")
    
    user_id = user_data.get('userid')
    
    try:
        user_id = ObjectId(user_id)
        blog_id = ObjectId(blog_id)
    except Exception:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid IDs')
     
    blog = await blog_collection.find_one({"_id": blog_id})
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog data not found")
    
    if user_id not in blog.get('likedBy'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You have not liked that blog')
    
    update = await blog_collection.update_one({"_id": blog_id}, {"$pull":{"likedBy":user_id}, "$inc": {'likes':-1}})
    
    if not update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to unlike')
    
    response.status_code = status.HTTP_200_OK
    return {"message": "Blog unlike successfully" }
     
     
    