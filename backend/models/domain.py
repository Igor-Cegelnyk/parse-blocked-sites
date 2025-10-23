
from sqlalchemy import String, Enum, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from backend.models import Base
from backend.models.enums import BlockListEnum
from backend.models.mixins import IdIntPkMixin
from backend.utils.convert_date import current_date_int, current_time_int


class Domain(Base, IdIntPkMixin):
    domain_name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )

    ip_address: Mapped[str] = mapped_column(
        String(150),
        nullable=True,
    )

    block_list: Mapped[BlockListEnum] = mapped_column(
        Enum(BlockListEnum),
        nullable=False,
    )

    created_date: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=current_date_int,
        server_default=text("CAST(to_char(now(),'YYYYMMDD') AS INTEGER)"),
    )

    created_time: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=current_time_int,
        server_default=text("CAST(to_char(now(),'HH24MISS') AS INTEGER)"),
    )