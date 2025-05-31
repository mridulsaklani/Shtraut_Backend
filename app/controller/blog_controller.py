from fastapi import HTTPException, Response, status
from app.config.database import db
from app.model.blog_model import Blog
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