from typing import List, Union, TypeVar, Generic

from pydantic import BaseModel

from backend.repositories import SqlAlchemyRepository, ModelType

RepoType = TypeVar("RepoType", bound=SqlAlchemyRepository)


class BaseService(Generic[ModelType, RepoType]):
    repository: RepoType

    def __init__(self, repository: SqlAlchemyRepository) -> None:
        self.repository: SqlAlchemyRepository = repository

    async def create(
        self,
        model: BaseModel,
    ) -> ModelType:
        model = self.repository.model(**model.model_dump())
        return await self.repository.create(instance=model)

    async def update(
        self,
        model: ModelType,
        model_update: BaseModel,
        partial: bool = True,
    ) -> ModelType:
        return await self.repository.update(
            instance=model,
            instance_update=model_update.model_dump(exclude_unset=partial),
        )

    async def get_by_id(self, id: int) -> ModelType:
        return await self.repository.get_by_id(id=id)

    async def get_all(
        self,
        filters: dict | None = None,
        order_by: str | None = None,
        desc_order: bool = False,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Union[List[ModelType]]:
        return await self.repository.get_all(
            filters=filters,
            order_by=order_by,
            desc_order=desc_order,
            limit=limit,
            offset=offset,
        )

    async def delete(
        self,
        model: ModelType,
    ) -> None:
        await self.repository.delete(instance=model)

    async def bulk_create(
        self,
        models: List[BaseModel],
    ) -> List[ModelType]:
        models = [self.repository.model(**model.model_dump()) for model in models]
        return await self.repository.bulk_create(instances=models)

    async def bulk_delete_by_ids(
        self,
        ids: List[int],
    ) -> int:
        rowcount = await self.repository.bulk_delete_by_ids(ids=ids)
        return rowcount
