from typing import Optional, List
from pydantic import BaseModel

class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 900

class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str

class LogoutRequestSchema(BaseModel):
    refresh_token: Optional[str] = None

class DeviceSessionResponseSchema(BaseModel):
    id: str
    session_key: str
    ip_address: str
    user_agent: str
    device_type: str
    is_active: bool
    last_activity_at: str
    created_at: str
