from uuid import UUID

from pydantic import BaseModel, Field


class UserIn(BaseModel):
    username: str = Field(max_length=128)
    email: str = Field(max_length=128)
    password1: str = Field(max_length=128)
    password2: str = Field(max_length=128)
    first_name: str | None = None
    last__name: str | None = None


class UserOut(BaseModel):
    uuid: UUID
    username: str
    email: str = Field(max_length=128)
    first_name: str | None = None
    last_name: str | None = None
