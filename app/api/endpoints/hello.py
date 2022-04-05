from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get() -> dict[str, str]:
    return {"message": "Hello World!"}
