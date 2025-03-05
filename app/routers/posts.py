from fastapi import APIRouter

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get('/tests')
async def get_test():
    return "Hello"