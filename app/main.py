from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config.database import connect_to_mongo

# ROUTES
from app.routes.user_routes import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],  
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)

app.include_router(user_router, prefix='/api/user')

@app.get("/")
def welcome():
    return {"message": "Welcome to Shtraut Backend!"}
