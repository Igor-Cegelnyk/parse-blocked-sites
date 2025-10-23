from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(
    tags=["Main"],
)


@router.get(
    "/",
    summary="Рендерить головну сторінку",
    response_class=HTMLResponse,
    name="domain",
)
async def read_root(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("domain.html", {"request": request})
