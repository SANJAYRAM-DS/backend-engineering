from typing import Optional, Dict, Any
from pydantic import BaseModel

class AuditLogResponseSchema(BaseModel):
    id: str
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    event_type: str
    ip_address: str
    user_agent: str
    status: str
    details: Dict[str, Any]
    created_at: str
