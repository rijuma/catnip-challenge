from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import db_init, async_engine
from app.routes import api_router
from app.env import DEVELOPMENT
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    if DEVELOPMENT:
        await db_init()
    yield
    await async_engine.dispose()

app = FastAPI(title="Catnip API", lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:5173", # Frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
