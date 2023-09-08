from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request

router = APIRouter(prefix="/app")


cur_path = Path(__file__).parent.parent
templates = Jinja2Templates(directory=cur_path / "templates")


@router.get("/uni")
async def uni_app(request: Request):
    return templates.TemplateResponse("uni.html", {"request": request})

