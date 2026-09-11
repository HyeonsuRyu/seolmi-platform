from enum import Enum

from pydantic import BaseModel


class Department(str, Enum):
    REFUND = "환불·교환"
    MARKETING = "마케팅"
    GENERAL = "일반문의"
    ESCALATE = "에스컬레이션"


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    department: Department
    reply: str
    escalation: str | None = None
