import asyncio
from typing import List, TYPE_CHECKING

from backend.config import Logger
from backend.database import db_helper
from backend.models import LogStatusEnum, BlockListEnum
from backend.repositories.domain import DomainRepository
from backend.repositories.domain_log import DomainLogRepository
from backend.schemas.domain_log import DomainLogCreate
from backend.services.domain_log_service import DomainLogService
from backend.services.domain_service import DomainService
from backend.services.parse_service import ParseService
from backend.utils.convert_date import datetime_int_to_datetime
from backend.utils.profile_decorator import profile

if TYPE_CHECKING:
    from backend.config.config import Settings
    from backend.models.domain_log import DomainLog

log = Logger().get_logger()


async def parse_domains(
    api_settings: "Settings",
    last_record: List["DomainLog"],
) -> List:
    update_datetime = None
    if last_record:
        update_datetime = datetime_int_to_datetime(
            date_int=last_record[0].created_date,
            time_int=last_record[0].created_time,
        )
    parse_service = ParseService(api_settings, update_datetime)
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
        last_log_record = await domain_log_service.get_all(
            filters=domain_log.model_dump(exclude_unset=True),
            order_by="id",
            desc_order=True,
            limit=1,
        )

        try:
            domains = await parse_domains(api_settings, last_log_record)
            log.info("Знайдено %s заблокованих доменів" % len(domains))

            if len(domains) == 0:
                domain_log.log_status = LogStatusEnum.NO_CHANGES
                await domain_log_service.create(domain_log)
                return None

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
    asyncio.run(loader_parse_domains())
