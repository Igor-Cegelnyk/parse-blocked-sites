import ipaddress
from typing import List, TYPE_CHECKING

from fastapi import APIRouter, Query, Request, HTTPException, File, UploadFile, Response
from fastapi.responses import HTMLResponse
from fastapi.params import Depends
from starlette import status

from backend.config import settings
from backend.routers.dependencies import get_domain_service
from backend.schemas.domain import DomainRead, DomainExcel
from backend.services.excel_service import ExcelExportService

if TYPE_CHECKING:
    from backend.services.domain_service import DomainService

router = APIRouter(
    prefix=settings.api_prefix.domain,
    tags=["Domain"],
)


@router.get(
    "",
    summary="Рендерить головну сторінку та вкладку Заблоковані Домени",
    response_class=HTMLResponse,
    name="domains",
)
async def domain_page(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("domain.html", {"request": request})


@router.get(
    "/list",
    summary="Повертає дані по всім доменам, що зберігаються в БД",
    status_code=status.HTTP_200_OK,
    response_model=List[DomainRead],
    responses={
        404: {"description": "Дані відсутні"},
    },
)
async def get_all_domains(
    offset: int = Query(
        1,
        ge=0,
        description="Початковий індекс для пагінації, починається з 0",
    ),
    limit: int = Query(
        25,
        ge=0,
        description="Максимальна кількість доменів для повернення",
    ),
    domain_service: "DomainService" = Depends(get_domain_service),
):
    domains = await domain_service.get_all(offset=offset, limit=limit)
    if not domains:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Дані відсутні",
        )
    return domains


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


@router.get(
    "/excel-export",
    summary="Генерує та зберігає файл формату xlsx з усіма доменами в БД",
    response_class=HTMLResponse,
    response_model=List[DomainRead],
)
async def domains_excel_export(
    domain_service: "DomainService" = Depends(get_domain_service),
):
    domains = await domain_service.get_all()
    return await ExcelExportService().export_excel(
        data=domains, schema=DomainExcel, filename="blocked domains.xlsx"
    )


@router.post(
    "/upload",
    summary="Повертає відфільтровані дані по доменам відповідно до вмісту файла",
    status_code=status.HTTP_200_OK,
    response_model=List[DomainRead],
    responses={
        404: {"description": "Дані відсутні"},
    },
)
async def upload_file(file: UploadFile = File(...)):
    # domains = []
    # if not domains:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Дані відсутні",
    #     )
    return Response(status_code=status.HTTP_200_OK)
