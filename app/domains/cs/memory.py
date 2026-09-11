"""세션별 대화 메모리 (lesson01의 ConversationBufferWindowMemory 실습 적용).

프로토타입이므로 프로세스 메모리에만 저장한다 — 서버 재시작 시 사라진다.
실제 서비스에서는 DB나 Redis 등 영속 저장소로 교체해야 한다.
"""

from langchain_classic.memory import ConversationBufferWindowMemory

_MEMORY_STORE: dict[str, ConversationBufferWindowMemory] = {}
_WINDOW_SIZE = 4


def get_memory(session_id: str) -> ConversationBufferWindowMemory:
    if session_id not in _MEMORY_STORE:
        _MEMORY_STORE[session_id] = ConversationBufferWindowMemory(
            k=_WINDOW_SIZE, return_messages=True
        )
    return _MEMORY_STORE[session_id]


def turn_count(session_id: str) -> int:
    memory = _MEMORY_STORE.get(session_id)
    if memory is None:
        return 0
    return len(memory.chat_memory.messages) // 2
