from typing import TYPE_CHECKING

from fastapi import Depends

from backend.database import db_helper
from backend.repositories.domain import DomainRepository
from backend.repositories.domain_log import DomainLogRepository
from backend.services.domain_log_service import DomainLogService
from backend.services.domain_service import DomainService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_domain_service(
    session: "AsyncSession" = Depends(db_helper.session_getter),
) -> DomainService:
    return DomainService(DomainRepository(session=session))


async def get_domain_log_service(
    session: "AsyncSession" = Depends(db_helper.session_getter),
) -> DomainLogService:
    return DomainLogService(DomainLogRepository(session=session))
