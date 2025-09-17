from fastapi import APIRouter
from . import users, accounts, transactions

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(accounts.router)
api_router.include_router(transactions.router)
