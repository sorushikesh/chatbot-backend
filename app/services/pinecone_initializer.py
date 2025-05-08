import logging
from pinecone import Pinecone, PodSpec
from sentence_transformers import SentenceTransformer
from app.core.config import settings

logger = logging.getLogger(__name__)

def initialize_pinecone_index(model_name: str) -> tuple:
    collection_name = settings.PINECONE_INDEX_NAME
    pinecone_env = settings.PINECONE_ENV
    pinecone_api_key = settings.PINECONE_API_KEY

    logger.info("Loading SentenceTransformer model: %s", model_name)
    model = SentenceTransformer(model_name)
    vector_dimension = len(model.encode("sample text"))
    logger.info("Vector dimension detected: %d", vector_dimension)

    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(collection_name)

    logger.info("Pinecone index '%s' is ready", collection_name)
    return pc, index, vector_dimension
