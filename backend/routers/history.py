from typing import List, TYPE_CHECKING

from fastapi import APIRouter, Request, Depends, Query, Response, HTTPException
from fastapi.responses import HTMLResponse
from starlette import status

from backend.auto_loader.parse_domain.loader_parse_domain import loader_parse_domains
from backend.config import settings
from backend.routers.dependencies import get_domain_log_service

from backend.schemas.domain_log import DomainLogRead

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
    return templates.TemplateResponse("history.html", {"request": request})


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
    domain_log_service: "DomainLogService" = Depends(get_domain_log_service),
):
    domain_logs = await domain_log_service.get_all(
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
async def parse_domain():
    try:
        await loader_parse_domains()
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Сталася помилка при парсингу даних",
        )
