from backend.models import Domain
from backend.repositories import SqlAlchemyRepository


class DomainRepository(SqlAlchemyRepository):
    model = Domain
