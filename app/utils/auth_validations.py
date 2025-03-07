import random

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserIn
from app.services.users import get_user_by_email, get_user_by_username, delete_verification_code
from core.models import User, Verification


class AuthValidation(object):
    def __init__(self, user: UserIn, db: AsyncSession):
        self.user = user
        self.db = db

    async def validate(self):
        await self.match_passwords()
        await self.validate_email()
        await self.validate_username()

    async def match_passwords(self):
        if self.user.password1 != self.user.password2:
            raise HTTPException(status_code=400, detail="Passwords does not match")

    async def validate_email(self):
        user = await get_user_by_email(email=self.user.email, db=self.db)
        if user:
            raise HTTPException(status_code=400, detail="User with this email is already exists")
        if not self.user.email.endswith('@gmail.com'):
            raise HTTPException(status_code=400, detail="Email is not valid")

    async def validate_username(self):
        user = await get_user_by_username(username=self.user.username, db=self.db)
        if user:
            raise HTTPException(status_code=400, detail="User with this username is already exists")


async def generate_verification_code(db: AsyncSession, user: User):
    verification = user.verification
    if verification:
        await delete_verification_code(db=db, verification=verification)

    random_code = str(random.randint(100000, 999999))
    new_code = Verification(
        code=random_code, user_id=user.id, lifetime=2
    )
    db.add(new_code)
    await db.commit()
    await db.refresh(new_code)
    return new_code
