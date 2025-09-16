from fastapi import APIRouter
from . import users, accounts

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(accounts.router)
