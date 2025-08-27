from fastapi import APIRouter

router = APIRouter(prefix="/api/auth")

@router.get("/users")
async def get_users():
    return {"message": "Hello World"}