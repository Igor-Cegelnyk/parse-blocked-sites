from backend.repositories.domain import DomainRepository
from backend.services.base_service import BaseService


class DomainService(BaseService):
    repository: DomainRepository
