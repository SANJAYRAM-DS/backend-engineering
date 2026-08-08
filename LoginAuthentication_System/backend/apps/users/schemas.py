from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_email_verified: bool
    is_staff: bool
    is_superuser: bool
    roles: List[str] = []
    created_at: str

class EmailVerificationSchema(BaseModel):
    token: str

class PasswordResetRequestSchema(BaseModel):
    email: EmailStr

class PasswordResetConfirmSchema(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
