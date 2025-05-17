from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from app.config.database import connect_to_mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def welcome():
    return {"message": "welcome"}