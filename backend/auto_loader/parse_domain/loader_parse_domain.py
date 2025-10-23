import asyncio
from typing import List, TYPE_CHECKING

from backend.config import Logger, settings
from backend.database import db_helper
from backend.models import LogStatusEnum, BlockListEnum
from backend.repositories.domain import DomainRepository
from backend.repositories.domain_log import DomainLogRepository
from backend.schemas.domain_log import DomainLogCreate

# from backend.services.advertising_service import AdvertisingService
from backend.services.domain_log_service import DomainLogService
from backend.services.domain_service import DomainService
from backend.services.parse_service import ParseService

# from backend.services.website_service import WebsiteService
from backend.utils.profile_decorator import profile

if TYPE_CHECKING:
    from backend.config.config import Settings

log = Logger().get_logger()


async def parse_domains(api_settings: "Settings") -> List:
    parse_service = ParseService(api_settings)
    results = await parse_service.get_all_domains()
    return results


@profile(log)
async def loader_parse_domains(api_settings: "Settings") -> None:
    log.info("Початок парсингу доменів по списку: %s..." % api_settings.name)
    domain_log = DomainLogCreate(
        log_status=LogStatusEnum.OK,
        block_list=BlockListEnum(api_settings.name),
    )

    async with db_helper.session_factory() as session:
        domain_service = DomainService(DomainRepository(session=session))
        domain_log_service = DomainLogService(DomainLogRepository(session=session))

        try:
            domains = await parse_domains(api_settings)
            log.info("Знайдено %s заблокованих доменів" % len(domains))

            domains_uniq = []
            domain_names_set = set()
            for domain in domains:
                if domain.domain_name in domain_names_set:
                    continue
                domain_names_set.add(domain.domain_name)
                domains_uniq.append(domain)

            if domains:
                exist_domain = await domain_service.get_all(
                    filters={"block_list": BlockListEnum(api_settings.name)}
                )
                exist_domain_set = {domain.domain_name for domain in exist_domain}

                new_domains = [
                    domain
                    for domain in domains_uniq
                    if domain.domain_name not in exist_domain_set
                ]
                if new_domains:
                    await domain_service.bulk_create(new_domains)

                to_remove_domain_ids = [
                    domain.id
                    for domain in exist_domain
                    if domain.domain_name not in domain_names_set
                ]
                if to_remove_domain_ids:
                    await domain_service.bulk_delete_by_ids(to_remove_domain_ids)

                domain_log.parse_domain_quantity = len(domains)
                domain_log.new_domain_quantity = len(new_domains)
                domain_log.remove_domain_quantity = len(to_remove_domain_ids)

            log.info(
                "Записано: %s нових доменів та видалено: %s доменів"
                % (domain_log.new_domain_quantity, domain_log.remove_domain_quantity)
            )
            await domain_log_service.create(domain_log)
        except Exception as e:
            domain_log.log_status = LogStatusEnum.FAILED
            await domain_log_service.create(domain_log)
            raise e

    return None


if __name__ == "__main__":
    asyncio.run(loader_parse_domains(settings.advertising_api))
