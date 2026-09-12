from fastapi import APIRouter
from pydantic import BaseModel

from app.services.vector_store import search_documents
from app.services.ai_analysis import ask_rag

router = APIRouter(prefix="/rag", tags=["RAG"])


class RAGRequest(BaseModel):
    question: str


@router.post("/query")
def rag_query(request: RAGRequest):

    chunks = search_documents(request.question)

    answer = ask_rag(
        question=request.question,
        context=chunks
    )

    return {
        "question": request.question,
        "answer": answer
    }