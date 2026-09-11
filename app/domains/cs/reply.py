"""부서별 답변 생성 체인.

환불·교환/마케팅은 lesson01 스타일(system+history+question)의 단순 LCEL 체인이고,
일반문의는 lesson02 스타일의 RAG 체인(FAQ 검색 결과를 context로 주입)이다.
두 경우 모두 세션 메모리(app.domains.cs.memory)를 history로 넘겨 멀티턴 맥락을 유지한다.
"""

from functools import lru_cache
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from app.domains.cs import rag
from app.domains.cs.schemas import Department

PROMPTS_DIR = Path(__file__).resolve().parents[3] / "prompts"

_PROMPT_FILE = {
    Department.REFUND: "cs_reply_refund.md",
    Department.MARKETING: "cs_reply_marketing.md",
    Department.GENERAL: "cs_reply_general.md",
}


def _load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


@lru_cache
def _llm():
    return ChatOpenAI(model="gpt-5-nano", temperature=0.3)


@lru_cache
def _simple_reply_chain(department: Department):
    system = _load_prompt(_PROMPT_FILE[department])
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{inquiry}"),
    ])
    return prompt | _llm() | StrOutputParser()


@lru_cache
def _general_reply_chain():
    system = _load_prompt(_PROMPT_FILE[Department.GENERAL])
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{inquiry}"),
    ])
    return prompt | _llm() | StrOutputParser()


def generate_reply(department: Department, inquiry: str, history: list) -> str:
    if department == Department.GENERAL:
        context = rag.search_faq(inquiry)
        chain = _general_reply_chain()
        return chain.invoke({"context": context, "history": history, "inquiry": inquiry})

    chain = _simple_reply_chain(department)
    return chain.invoke({"history": history, "inquiry": inquiry})
