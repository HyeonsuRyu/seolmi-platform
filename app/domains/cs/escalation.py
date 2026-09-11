"""README 5.3 즉시 에스컬레이션 규칙의 1차 필터.

LLM에게 판단을 맡기지 않고 규칙 기반으로 먼저 걸러낸다 (자동응답 금지 대상은
LLM 응답 자체를 생성하지 않는 것이 안전하기 때문). 키워드 목록은 시작점이며
실제 서비스 전에 운영팀 검수가 필요하다 [확인 필요].
"""

SAFETY_KEYWORDS = ["이물질", "복통", "식중독", "배탈", "알레르기"]
LEGAL_RISK_KEYWORDS = ["등급", "원산지", "1++", "투플러스", "허위표시"]
AUTHORITY_KEYWORDS = ["언론", "기자", "변호사", "소비자원", "고발"]

REPEAT_INQUIRY_THRESHOLD = 3


def check_escalation(message: str, turn_count: int) -> str | None:
    """규칙에 해당하면 에스컬레이션 사유 문자열을, 아니면 None을 반환한다."""

    for kw in SAFETY_KEYWORDS:
        if kw in message:
            return f"안전·위생 이슈 의심 키워드 감지: '{kw}' — 즉시 담당자 확인 필요"

    for kw in LEGAL_RISK_KEYWORDS:
        if kw in message:
            return f"등급·원산지 표기 관련 이의 가능성: '{kw}' — 정해진 스크립트 외 자동응답 금지"

    for kw in AUTHORITY_KEYWORDS:
        if kw in message:
            return f"언론·기관·법률 관련 언급 감지: '{kw}' — 자동응답 금지"

    if turn_count >= REPEAT_INQUIRY_THRESHOLD:
        return f"동일 세션 {turn_count}회 이상 재문의 — 상담원 확인 필요 (근사치 판정)"

    return None
