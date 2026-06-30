from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models.user import UserRole


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    phone: str | None = Field(default=None, min_length=10, max_length=20)
    profile_image: str | None = None


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone: str
    role: UserRole
    profile_image: str | None
    is_active: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)