"""lesson02의 PDF+FAISS RAG 실습을, data/cs_faq/*.md FAQ 문서에 적용.

'일반문의' 부서 답변에 근거 문서를 붙이기 위한 검색기(retriever)를 구성한다.
FAQ 파일 수가 적어 서버 시작 시 1회만 인메모리로 색인하고 재사용한다.
"""

from functools import lru_cache
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

FAQ_DIR = Path(__file__).resolve().parents[3] / "data" / "cs_faq"


@lru_cache
def get_retriever(k: int = 3):
    loader = DirectoryLoader(str(FAQ_DIR), glob="*.md", loader_cls=TextLoader)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb = FAISS.from_documents(chunks, embeddings)
    return vectordb.as_retriever(search_kwargs={"k": k})


def search_faq(question: str) -> str:
    retriever = get_retriever()
    docs = retriever.invoke(question)
    return "\n\n".join(d.page_content for d in docs)
