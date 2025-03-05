from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserIn, UserOut
from app.utils.auth_validations import AuthValidation
from app.utils.hash_password import hash_password
from core.database import get_db
from core.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post('/register/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register(user: UserIn, db: AsyncSession = Depends(get_db)):
    validation = AuthValidation(user=user, db=db)
    await validation.validate()

    hashed_password = hash_password(password=user.password1)
    new_user = User(
        first_name=user.first_name, last_name=user.last__name,
        username=user.username, password=hashed_password,
        email=user.email
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
