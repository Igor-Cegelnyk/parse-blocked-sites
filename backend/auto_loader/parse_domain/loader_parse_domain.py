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
    log.info(f"Початок парсингу доменів по списку: {api_settings.name}...")
    domain_log = DomainLogCreate(
        log_status=LogStatusEnum.OK,
        block_list=BlockListEnum(api_settings.name),
    )

    async with db_helper.session_factory() as session:
        domain_service = DomainService(DomainRepository(session=session))
        domain_log_service = DomainLogService(DomainLogRepository(session=session))

        try:
            last_log = await domain_log_service.get_all(
                filters=domain_log.model_dump(exclude_unset=True),
                order_by="id",
                desc_order=True,
                limit=1,
            )

            parsed_domains = await parse_domains(api_settings, last_log)

            total, new_count, removed_count = (
                await domain_service.sync_domains_from_parser(
                    block_list=BlockListEnum(api_settings.name),
                    parsed_domains=parsed_domains,
                )
            )

            domain_log.parse_domain_quantity = total
            domain_log.new_domain_quantity = new_count
            domain_log.remove_domain_quantity = removed_count
            domain_log.log_status = (
                LogStatusEnum.NO_CHANGES if total == 0 else LogStatusEnum.OK
            )

            log.info(
                f"Знайдено {total} доменів, додано {new_count}, видалено {removed_count}"
            )
            await domain_log_service.create(domain_log)

        except Exception as e:
            session.rollback()
            domain_log.log_status = LogStatusEnum.FAILED
            await domain_log_service.create(domain_log)
            raise e

    return None


if __name__ == "__main__":
    from backend.config import settings

    asyncio.run(loader_parse_domains(settings.advertising_api))
