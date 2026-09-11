"""lesson01의 LCEL(prompt | llm | parser) 패턴으로 만든 CS 부서 분류 체인."""

from functools import lru_cache
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.domains.cs.schemas import Department

PROMPTS_DIR = Path(__file__).resolve().parents[3] / "prompts"


def _load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


@lru_cache
def _router_chain():
    system = _load_prompt("cs_router.md")
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "{inquiry}"),
    ])
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    return prompt | llm | StrOutputParser()


_LABEL_TO_DEPARTMENT = {
    "환불": Department.REFUND,
    "교환": Department.REFUND,
    "마케팅": Department.MARKETING,
    "일반문의": Department.GENERAL,
    "일반": Department.GENERAL,
}


def classify_department(inquiry: str) -> Department:
    raw = _router_chain().invoke({"inquiry": inquiry}).strip()
    for label, department in _LABEL_TO_DEPARTMENT.items():
        if label in raw:
            return department
    # 라벨을 못 찾으면 일반문의로 안전하게 폴백한다.
    return Department.GENERAL
