import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.project import ProjectRepository
from app.schemas.project import CreateProjectRequest, UpdateProjectRequest
from app.models.project import Project
from app.core.exceptions import ResourceNotFoundException

class ProjectService:
    def __init__(self, db: AsyncSession):
        self.repo = ProjectRepository(db)

    async def create_project(self, schema: CreateProjectRequest) -> Project:
        return await self.repo.create(schema.model_dump())

    async def get_project(self, project_id: uuid.UUID) -> Project:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise ResourceNotFoundException(
                message=f"Project with ID '{project_id}' was not found."
            )
        return project

    async def list_projects(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        skip = (page - 1) * limit
        items = await self.repo.list_all(skip=skip, limit=limit)
        total = await self.repo.count_all()
        total_pages = (total + limit - 1) // limit if limit > 0 else 1

        return {
            "items": items,
            "meta": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages
            }
        }

    async def update_project(self, project_id: uuid.UUID, schema: UpdateProjectRequest) -> Project:
        project = await self.get_project(project_id)
        update_data = schema.model_dump(exclude_unset=True)
        return await self.repo.update(project, update_data)

    async def delete_project(self, project_id: uuid.UUID) -> None:
        project = await self.get_project(project_id)
        await self.repo.delete(project)
