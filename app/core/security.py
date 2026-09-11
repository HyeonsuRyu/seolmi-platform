"""JWT 인증 스켈레톤.

README 2장: 역할 3종(b2b/consumer/admin) JWT 인증 예정이지만 아직 미구현이다.
현재는 모든 요청을 인증 없이 통과시키는 자리표시자만 둔다.
실제 로그인·토큰 발급·검증이 들어오면 이 파일을 채운다.
"""

from typing import Optional


def get_current_role() -> Optional[str]:
    # TODO(류현수): JWT 검증 후 "b2b" | "consumer" | "admin" 반환하도록 구현
    return None
