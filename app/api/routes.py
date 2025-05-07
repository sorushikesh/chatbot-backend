from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.models.message import MessageRequest
from app.services.llama_service import stream_llama_response

router = APIRouter()

@router.post("/ask", response_class=StreamingResponse)
def ask_bot_stream(message: MessageRequest):
    stream = stream_llama_response(message.message)
    return StreamingResponse(stream, media_type="text/plain")
