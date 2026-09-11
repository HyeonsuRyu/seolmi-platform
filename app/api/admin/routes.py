"""관리자 면 스켈레톤. 화면 스케치 1장만 제공 (README 8장 '인원 제약' 참고).

실제 재고·정산·CS 티켓 라우팅 대시보드 등은 각 도메인 구현 후 연결한다.
"""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request, "admin/home.html", {"title": "관리자 (준비 중)"}
    )
