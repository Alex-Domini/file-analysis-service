from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Web"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@router.get("/files-page", response_class=HTMLResponse)
async def files_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="files.html",
    )
