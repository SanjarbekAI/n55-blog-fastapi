from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserIn, UserOut, Token
from app.services.users import authenticate_user
from app.utils.auth_validations import AuthValidation, generate_verification_code
from app.utils.email import send_in_background
from app.utils.hash_password import get_password_hash
from app.utils.jwt_token import create_access_token
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.database import get_db
from core.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post('/register/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register(user: UserIn, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    validation = AuthValidation(user=user, db=db)
    await validation.validate()

    hashed_password = get_password_hash(password=user.password1)
    new_user = User(
        first_name=user.first_name, last_name=user.last__name,
        username=user.username, password=hashed_password,
        email=user.email
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    verification = await generate_verification_code(user=new_user, db=db)
    await send_in_background(user=new_user, code=verification.code, background_tasks=background_tasks)

    return new_user


@router.post("/login")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_db)
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please, verify your email, and try again"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
