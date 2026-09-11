"""B2B 면 스켈레톤. 화면 스케치 1장만 제공 (README 8장 '인원 제약' 참고).

실제 단가표·대량발주·세금계산서 등은 app/domains/pricing, orders 구현 후 연결한다.
"""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/b2b", tags=["b2b"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request, "b2b/home.html", {"title": "B2B — 사업장용 (준비 중)"}
    )
