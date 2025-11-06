from typing import TYPE_CHECKING, List

from backend.repositories.domain import DomainRepository
from backend.services.base_service import BaseService

if TYPE_CHECKING:
    from backend.schemas.domain import DomainCreate
    from backend.models.enums.block_list import BlockListEnum


class DomainService(BaseService):
    repository: DomainRepository

    @staticmethod
    def _normalize_key(domain_name: str) -> str:
        return domain_name.strip().lower()

    async def sync_domains_from_parser(
        self,
        block_list: "BlockListEnum",
        parsed_domains: List["DomainCreate"],
    ) -> tuple[int, int, int]:
        """
        Synchronize domains from parsed domains.
        """
        if not parsed_domains:
            return 0, 0, 0

        # Unique parsed domains
        uniq_domains = {self._normalize_key(d.domain_name): d for d in parsed_domains}

        exist_domains = await self.get_all(filters={"block_list": block_list})
        exist_set = {self._normalize_key(d.domain_name): d for d in exist_domains}

        # remove domains
        to_remove_ids = [
            value.id
            for key, value in exist_set.items()
            if not uniq_domains.get(key, None)
        ]
        if to_remove_ids:
            await self.bulk_delete_by_ids(to_remove_ids)

        # New domains
        new_domains = [
            value for key, value in uniq_domains.items() if not exist_set.get(key, None)
        ]
        if new_domains:
            await self.bulk_create(new_domains)

        return len(parsed_domains), len(new_domains), len(to_remove_ids)


# async def main():
#     from backend.database import db_helper
#
#     async with db_helper.session_factory() as session:
#         domain_service = DomainService(DomainRepository(session=session))
#         parsed_domains = await domain_service.get_all(filters={"block_list": "WEBSITE"})
#
#         total, new_count, removed_count = await domain_service.sync_domains_from_parser(
#             block_list="WEBSITE",
#             parsed_domains=parsed_domains,
#         )
#
#     print(f"total: {total}, new count: {new_count}, removed count: {removed_count}")
#
#
# if __name__ == "__main__":
#     import asyncio
#
#     asyncio.run(main())
