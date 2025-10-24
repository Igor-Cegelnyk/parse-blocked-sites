from typing import List, TYPE_CHECKING

from fastapi import APIRouter, Request, Depends, Query, Response, HTTPException
from fastapi.responses import HTMLResponse
from starlette import status

from backend.auto_loader.parse_domain.loader_parse_domain import loader_parse_domains
from backend.config import settings
from backend.models import BlockListEnum, LogStatusEnum
from backend.routers.dependencies import get_domain_log_service

from backend.schemas.domain_log import DomainLogRead, DomainLogParam

if TYPE_CHECKING:
    from backend.services.domain_log_service import DomainLogService

router = APIRouter(
    prefix=settings.api_prefix.history,
    tags=["History"],
)


@router.get(
    "",
    summary="Рендерить вкладку Історія завантажень",
    response_class=HTMLResponse,
    name="history",
)
async def history(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "block_lists": [e.value for e in BlockListEnum],
            "log_statuses": [e.value for e in LogStatusEnum],
        },
    )


@router.get(
    "/log",
    summary="Повертає інформацію про результати прасингу доменів",
    response_model=List[DomainLogRead],
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Дані відсутні"}},
)
async def get_domain_logs(
    offset: int = Query(
        1,
        ge=0,
        description="Початковий індекс для пагінації, починається з 0",
    ),
    limit: int = Query(
        25,
        ge=0,
        description="Максимальна кількість записів для повернення",
    ),
    log_status: LogStatusEnum = Query(None, description="Статус завантаження"),
    block_list: BlockListEnum = Query(None, description="Список блокування"),
    domain_log_service: "DomainLogService" = Depends(get_domain_log_service),
):
    filters = {}
    if log_status is not None:
        filters["log_status"] = LogStatusEnum(log_status)
    if block_list is not None:
        filters["block_list"] = BlockListEnum(block_list)

    domain_logs = await domain_log_service.get_all(
        filters=filters,
        order_by="id",
        desc_order=True,
        offset=offset,
        limit=limit,
    )
    if not domain_logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Дані відсутні",
        )
    return domain_logs


@router.post(
    "/log",
    summary="Ручний запуск парсингу заблокованих доменів та їх запис в БД",
    status_code=status.HTTP_200_OK,
    responses={
        500: {"description": "Сталася помилка при парсингу даних"},
    },
)
async def parse_domain(params: DomainLogParam):
    if params.block_list == "honlapok":
        api_settings = settings.website_api
    else:
        api_settings = settings.advertising_api
    try:
        await loader_parse_domains(api_settings)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Сталася помилка при парсингу даних",
        )
