import ipaddress
from typing import List, TYPE_CHECKING

from fastapi import APIRouter, Query, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.params import Depends
from starlette import status

from backend.config import settings
from backend.routers.dependencies import get_domain_service
from backend.schemas.domain import DomainRead

if TYPE_CHECKING:
    from backend.services.domain_service import DomainService

router = APIRouter(
    prefix=settings.api_prefix.domain_search,
    tags=["Domain Search"],
)


@router.get(
    "",
    summary="Рендерить вкладку Пошук",
    response_class=HTMLResponse,
    name="domain-search",
)
async def domain_search(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("domain_search.html", {"request": request})


@router.get(
    "/search",
    summary="Пошук заблокованого домену в БД по його назві чи IP",
    status_code=status.HTTP_200_OK,
    response_model=List[DomainRead],
    responses={
        404: {"description": "Дані відсутні"},
    },
)
async def get_domains(
    domain: str = Query(
        ...,
        description="Назва домену чи IP адреса",
        example="rtbet-5772.com",
    ),
    domain_service: "DomainService" = Depends(get_domain_service),
):
    try:
        ipaddress.ip_address(domain)
        domains = await domain_service.get_all(
            filters={"ip_address": domain},
        )
    except ValueError:
        domains = await domain_service.get_all(
            filters={"domain_name": domain},
        )
    if not domains:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Дані відсутні",
        )
    return domains
