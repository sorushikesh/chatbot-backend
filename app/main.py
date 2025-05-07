from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="LLaMA Chat API",
    version="1.0.0",
    description="FastAPI backend powered by LLaMA via Ollama"
)

app.include_router(router, prefix="/api")
