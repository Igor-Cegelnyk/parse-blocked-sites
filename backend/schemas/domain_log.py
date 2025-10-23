from typing import Optional

from pydantic import BaseModel, field_validator, Field

from backend.models import LogStatusEnum, BlockListEnum
from backend.utils.convert_date import date_int_to_str, time_int_to_str


class DomainLogParam(BaseModel):
    block_list: str


class DomainLogBase(BaseModel):
    parse_domain_quantity: int = Field(
        ...,
        description="Кількість виявлених доменів",
        examples=[3345],
    )
    new_domain_quantity: int = Field(
        ...,
        description="Кількість нових доменів",
        examples=[8],
    )
    remove_domain_quantity: int = Field(
        ...,
        description="Кількість видалених",
        examples=[0],
    )
    log_status: LogStatusEnum = Field(
        ...,
        description="Статус завантаження",
        examples=[LogStatusEnum.OK.value],
    )
    block_list: BlockListEnum = Field(
        ...,
        description="Список блокування",
        examples=[BlockListEnum.WEBSITE.value],
    )


class DomainLogCreate(DomainLogBase):
    parse_domain_quantity: Optional[int] = Field(
        None,
        description="Кількість виявлених доменів",
        examples=[3345],
    )
    new_domain_quantity: Optional[int] = Field(
        None,
        description="Кількість нових доменів",
        examples=[8],
    )
    remove_domain_quantity: Optional[int] = Field(
        None,
        description="Кількість видалених",
        examples=[0],
    )


class DomainLogRead(DomainLogBase):
    id: int = Field(
        ...,
        description="id запису в БД",
        examples=[1],
    )
    created_date: str = Field(
        ...,
        description="Дата запису в БД",
        examples=["2025-10-23"],
    )
    created_time: str = Field(
        ...,
        description="Чвс запису в БД",
        examples=["18:52:00"],
    )

    @field_validator("created_date", mode="before")
    @classmethod
    def parse_date(cls, v) -> str:
        if isinstance(v, int):
            return date_int_to_str(v)
        return v

    @field_validator("created_time", mode="before")
    @classmethod
    def parse_time(cls, v) -> str:
        if isinstance(v, int):
            return time_int_to_str(v)
        return v
