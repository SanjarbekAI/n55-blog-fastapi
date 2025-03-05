from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["lala"]
)


@router.get('/tests')
async def get_test():
    return "Hello"
