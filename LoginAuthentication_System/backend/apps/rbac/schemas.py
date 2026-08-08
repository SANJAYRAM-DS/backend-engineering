from typing import Optional, List
from pydantic import BaseModel

class PermissionSchema(BaseModel):
    id: str
    code: str
    description: str

class RoleSchema(BaseModel):
    id: str
    name: str
    description: str
    permissions: List[PermissionSchema] = []

class AssignRoleSchema(BaseModel):
    user_id: str
    role_name: str
