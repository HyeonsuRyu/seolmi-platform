from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.admin.routes import router as admin_router
from app.api.b2b.routes import router as b2b_router
from app.api.b2c.routes import router as b2c_router
from app.domains.cs.api import router as cs_router

app = FastAPI(title="설미(Seolmi) 플랫폼 프로토타입")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(b2b_router)
app.include_router(b2c_router)
app.include_router(admin_router)
app.include_router(cs_router)


@app.get("/")
def index(request: Request):
    links = [
        ("/cs", "CS 챗봇 (구현됨 — LangChain LCEL/메모리/RAG)"),
        ("/b2b", "B2B (스케치 전용)"),
        ("/b2c", "B2C (스케치 전용)"),
        ("/admin", "관리자 (스케치 전용)"),
    ]
    return templates.TemplateResponse(request, "base.html", {"title": "설미 프로토타입", "links": links})
