from backend.models import DomainLog
from backend.repositories import SqlAlchemyRepository


class DomainLogRepository(SqlAlchemyRepository):
    model = DomainLog
