from fastapi import APIRouter

__all__ = ["router"]

router = APIRouter()


@router.get("/")
@router.get("/ping")
async def ping():
    return "pong"
