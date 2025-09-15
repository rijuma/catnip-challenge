from contextlib import asynccontextmanager
from typing import Union, AsyncGenerator

from fastapi import FastAPI
from .db import db_init

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    db_init()
    yield

def get_app() -> FastAPI:
    app = FastAPI(title="Catnip Solutions", lifespan=lifespan)
    return app

app = get_app()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}