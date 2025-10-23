from typing import List

from fastapi import APIRouter, Request, UploadFile, File, Response, HTTPException
from fastapi.responses import HTMLResponse
from starlette import status

from backend.config import settings
from backend.schemas.domain import DomainRead

router = APIRouter(
    prefix=settings.api_prefix.file_search,
    tags=["File Search"],
)


@router.get(
    "/",
    summary="Рендерить вкладку пошук по файлу",
    response_class=HTMLResponse,
    name="file-search",
)
async def file_search(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("file_search.html", {"request": request})


@router.post(
    "/",
    summary="Повертає відфільтровані дані по доменам відповідно до вмісту файла",
    status_code=status.HTTP_200_OK,
    response_model=List[DomainRead],
    responses={
        404: {"description": "Дані відсутні"},
    },
)
async def upload_file(file: UploadFile = File(...)):
    # contents = await file.read()
    # domains = []
    # if not domains:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Дані відсутні",
    #     )
    return Response(status_code=status.HTTP_200_OK)
