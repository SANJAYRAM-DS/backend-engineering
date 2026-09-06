import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserMinimalResponse

# 1. CREATE REQUEST DTO (Input payload for POST /api/v1/projects)
class CreateProjectRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Project title",
        example="ResourceHub Platform"
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Detailed project description",
        example="Enterprise task management system backend API"
    )
    visibility: str = Field(
        "PRIVATE",
        pattern="^(PUBLIC|PRIVATE|INTERNAL)$",
        description="Visibility scope: PUBLIC, PRIVATE, or INTERNAL",
        example="PRIVATE"
    )
    owner_id: uuid.UUID = Field(
        ...,
        description="UUID of the project owner",
        example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )

# 2. UPDATE REQUEST DTO (Input payload for PUT /api/v1/projects/{id})
class UpdateProjectRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    visibility: Optional[str] = Field(None, pattern="^(PUBLIC|PRIVATE|INTERNAL)$")

# 3. SINGLE PROJECT RESPONSE DTO (Output payload with nested owner summary)
class ProjectResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    visibility: str
    owner_id: uuid.UUID
    owner: Optional[UserMinimalResponse] = None # Nested Schema
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# PAGINATION METADATA DTO
class PaginationMeta(BaseModel):
    page: int = Field(..., example=1)
    limit: int = Field(..., example=20)
    total: int = Field(..., example=100)
    total_pages: int = Field(..., example=5)

# 4. PAGINATED PROJECT LIST RESPONSE DTO
class ProjectListResponse(BaseModel):
    items: List[ProjectResponse]
    meta: PaginationMeta
