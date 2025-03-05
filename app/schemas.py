from uuid import UUID

from pydantic import BaseModel, Field


class UserIn(BaseModel):
    username: str
    age: int
    phone_number: str | None = Field(max_length=13, min_length=13)


class UserOut(UserIn):
    uuid: UUID
