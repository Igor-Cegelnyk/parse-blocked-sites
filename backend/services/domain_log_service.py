from backend.repositories.domain_log import DomainLogRepository
from backend.services.base_service import BaseService


class DomainLogService(BaseService):
    repository: DomainLogRepository
