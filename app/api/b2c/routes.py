"""B2C 면 스켈레톤. 화면 스케치 1장만 제공 (README 8장 '인원 제약' 참고).

실제 소분 상품 구매·후기 등은 app/domains/catalog, orders 구현 후 연결한다.
"""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/b2c", tags=["b2c"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request, "b2c/home.html", {"title": "B2C — 일반 소비자용 (준비 중)"}
    )
