from http.client import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserIn
from app.services.users import get_user_by_email, get_user_by_username


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
            raise HTTPException("Passwords does not match")

    async def validate_email(self):
        user = await get_user_by_email(email=self.user.email, db=self.db)
        if user:
            raise HTTPException("User with this email is already exists")
        if not self.user.email.endswith('@gmail.com'):
            raise HTTPException("Email is not valid")

    async def validate_username(self):
        user = await get_user_by_username(username=self.user.username, db=self.db)
        if user:
            raise HTTPException("User with this username is already exists")
