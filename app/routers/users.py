from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import MessageSchema, MessageType, FastMail
from jinja2 import Template
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.schemas import UserIn, UserOut, Token, EmailSchema
from app.services.users import authenticate_user
from app.utils.auth_validations import AuthValidation
from app.utils.hash_password import get_password_hash
from app.utils.jwt_token import create_access_token
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, conf
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

    hashed_password = get_password_hash(password=user.password1)
    new_user = User(
        first_name=user.first_name, last_name=user.last__name,
        username=user.username, password=hashed_password,
        email=user.email
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
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


@router.post('/email')
async def send_in_background(
        background_tasks: BackgroundTasks,
        email: EmailSchema
) -> JSONResponse:
    with open("templates/email_template.html", "r") as file:
        html_template = file.read()

    template = Template(html_template)
    html_content = template.render(name="John Doe")

    message = MessageSchema(
        subject="FastAPI-Mail HTML Email",
        recipients=email.email,
        body=html_content,
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    # Send email as a background task
    background_tasks.add_task(fm.send_message, message, template_name=None)

    return JSONResponse(status_code=200, content={"message": "HTML Email sent successfully"})
