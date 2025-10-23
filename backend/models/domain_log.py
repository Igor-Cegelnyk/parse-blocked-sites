from sqlalchemy import Enum, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from backend.models import Base
from backend.models.enums import LogStatusEnum, BlockListEnum
from backend.models.mixins import IdIntPkMixin
from backend.utils.convert_date import current_date_int, current_time_int


class DomainLog(Base, IdIntPkMixin):
    parse_domain_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )

    new_domain_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )

    remove_domain_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )

    log_status: Mapped[LogStatusEnum] = mapped_column(
        Enum(LogStatusEnum),
        nullable=False,
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
