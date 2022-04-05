from app.api.endpoints import hello
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(hello.router, tags=["hello"])
