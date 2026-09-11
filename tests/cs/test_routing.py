"""README 5.5 회귀 테스트: 실제 OpenAI API를 호출하므로 비용이 발생한다.

OPENAI_API_KEY가 없으면 스킵한다. 프롬프트(prompts/cs_router.md)를 고친 뒤
`pytest tests/cs/test_routing.py` 로 정확도가 떨어지지 않았는지 확인한다.
"""

import os
from pathlib import Path

import pytest
import yaml

from app.domains.cs.classify import classify_department
from app.domains.cs.schemas import Department

CASES_FILE = Path(__file__).parent / "routing_cases.yaml"

pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY가 없어 실제 LLM 호출 테스트를 건너뜁니다.",
)


def _load_cases():
    with open(CASES_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.mark.parametrize("case", _load_cases() if os.getenv("OPENAI_API_KEY") else [])
def test_routing_case(case):
    expected = Department(case["department"])
    actual = classify_department(case["inquiry"])
    assert actual == expected, f"'{case['inquiry']}' → 기대: {expected}, 실제: {actual}"
