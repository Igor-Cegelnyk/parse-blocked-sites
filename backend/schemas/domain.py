from typing import Optional

from pydantic import BaseModel, Field

from backend.models import BlockListEnum


class DomainBase(BaseModel):
    domain_name: str = Field(..., description="Домен", examples=["weissbetwins.online"])
    ip_address: Optional[str] = Field(
        ..., description="IP адреса", examples=["92.60.74.121"]
    )
    block_list: BlockListEnum = Field(
        ...,
        description="Список блокування",
        examples=[BlockListEnum.WEBSITE.value],
    )


class DomainCreate(DomainBase):
    ip_address: Optional[str] = None


class DomainRead(DomainBase):
    id: int = Field(..., description="id запису в БД", examples=[2])


class DomainExcel(DomainBase):

    model_config = {"from_attributes": True}
