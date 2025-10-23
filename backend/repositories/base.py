from typing import TypeVar, TYPE_CHECKING, Annotated, Any, List

from sqlalchemy import select, delete, desc
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Base)


class SqlAlchemyRepository:
    model = None

    def __init__(self, session: "AsyncSession"):
        self.session = session

    async def create(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(
        self,
        instance: ModelType,
        instance_update: dict,
    ) -> ModelType:
        for name, value in instance_update.items():
            setattr(instance, name, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        await self.session.delete(instance)
        await self.session.commit()

    async def get_by_id(self, id: int) -> Annotated[ModelType, None]:
        stmt = select(self.model).filter_by(id=id)
        result = await self.session.scalar(stmt)
        return result

    async def get_all(
        self,
        filters: dict | None = None,
        order_by: str | None = "id",
        desc_order: bool = False,
        limit: int | None = None,
        offset: int | None = None,
    ) -> List[ModelType]:
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        if order_by:
            column = getattr(self.model, order_by)
            if desc_order:
                column = desc(column)
            stmt = stmt.order_by(column)
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def bulk_create(self, instances: List[ModelType]) -> list[ModelType]:
        self.session.add_all(instances)
        await self.session.commit()
        for instance in instances:
            await self.session.refresh(instance)
        return instances

    async def bulk_delete_by_ids(self, ids: List[int]) -> int:
        if not ids:
            return 0
        stmt = delete(self.model).where(self.model.id.in_(ids))
        await self.session.execute(stmt)
        await self.session.commit()
        return len(ids)
