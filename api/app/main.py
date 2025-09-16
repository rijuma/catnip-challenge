
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db import db_init, async_engine
from .routes import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_init()
    yield
    await async_engine.dispose()

app = FastAPI(title="Catnip API", lifespan=lifespan)

app.include_router(api_router)
