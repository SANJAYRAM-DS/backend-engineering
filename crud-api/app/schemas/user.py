import uuid
from pydantic import BaseModel, ConfigDict, EmailStr

class UserMinimalResponse(BaseModel):
    """Minimal user summary embedded inside parent resources (Projects/Tasks)."""
    id: uuid.UUID
    email: EmailStr
    full_name: str

    model_config = ConfigDict(from_attributes=True)
