from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.domains.cs import memory as cs_memory
from app.domains.cs.classify import classify_department
from app.domains.cs.escalation import check_escalation
from app.domains.cs.reply import generate_reply
from app.domains.cs.schemas import ChatRequest, ChatResponse, Department

router = APIRouter(prefix="/cs", tags=["cs"])
templates = Jinja2Templates(directory="app/templates")

ESCALATION_REPLY = "죄송합니다. 이 문의는 자동응답 대상이 아니어서, 상담원이 확인 후 별도로 안내드리겠습니다."


@router.get("/")
def chat_page(request: Request):
    return templates.TemplateResponse(request, "cs/chat.html", {})


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    turns = cs_memory.turn_count(payload.session_id)
    escalation_reason = check_escalation(payload.message, turns + 1)

    if escalation_reason:
        department = Department.ESCALATE
        reply = ESCALATION_REPLY
    else:
        mem = cs_memory.get_memory(payload.session_id)
        history = mem.load_memory_variables({})["history"]

        department = classify_department(payload.message)
        reply = generate_reply(department, payload.message, history)

        mem.save_context({"input": payload.message}, {"output": reply})

    return ChatResponse(department=department, reply=reply, escalation=escalation_reason)
