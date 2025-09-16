from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import db_init, async_engine
from app.routes import api_router
from app.env import DEVELOPMENT

@asynccontextmanager
async def lifespan(app: FastAPI):
    if DEVELOPMENT:
        await db_init()
    yield
    await async_engine.dispose()

app = FastAPI(title="Catnip API", lifespan=lifespan)

app.include_router(api_router)
