import logging

from fastapi import APIRouter, HTTPException

from app.models.chat import ChatRequest, ChatResponse
from app.services.retriever import build_qa_chain

logger = logging.getLogger(__name__)

router = APIRouter()
qa_chain = build_qa_chain()


@router.post("/ask", response_model=ChatResponse)
def ask(chat: ChatRequest):
    try:
        logger.info("Incoming message: %s", chat.message)
        response = qa_chain.invoke({"query": chat.message})
        result = response.get("result")
        logger.info("Response generated successfully")
        return ChatResponse(response=result)
    except Exception as e:
        logger.exception("QA chain processing failed")
        raise HTTPException(status_code=500, detail="Failed to generate response")
