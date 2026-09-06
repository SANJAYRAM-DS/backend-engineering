import uuid
from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.project import Project

class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, project_data: dict) -> Project:
        project = Project(**project_data)
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def get_by_id(self, project_id: uuid.UUID) -> Optional[Project]:
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 20) -> Sequence[Project]:
        result = await self.db.execute(
            select(Project).offset(skip).limit(limit).order_by(Project.created_at.desc())
        )
        return result.scalars().all()

    async def count_all(self) -> int:
        result = await self.db.execute(select(func.count(Project.id)))
        return result.scalar_one()

    async def update(self, project: Project, update_data: dict) -> Project:
        for key, value in update_data.items():
            if value is not None:
                setattr(project, key, value)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def delete(self, project: Project) -> None:
        await self.db.delete(project)
        await self.db.flush()
