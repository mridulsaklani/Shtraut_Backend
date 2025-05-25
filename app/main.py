from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config.database import connect_to_mongo

# ROUTES
from app.routes.user_routes import router as user_router
from app.routes.verify_auth_routes import router as auth_router
from app.routes.blog_routes import router as blog_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",  
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)

app.include_router(user_router, prefix='/api/user')
app.include_router(auth_router, prefix='/api/auth')
app.include_router(blog_router, prefix="/api/blog")

@app.get("/")
def welcome():
    return {"message": "Welcome to Shtraut Backend!"}
