import logging
import threading
import time

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from app.services.db_loader import load_documents
from app.services.pinecone_initializer import initialize_pinecone_index

logger = logging.getLogger(__name__)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_, index, vector_dimension = initialize_pinecone_index(MODEL_NAME)
embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)


def get_vector_store():
    logger.info("Creating Pinecone vector store")
    return PineconeVectorStore(index=index, embedding=embeddings, namespace="default")


def auto_ingest_documents(interval_minutes=5):
    def ingest():
        while True:
            try:
                logger.info("Ingesting documents into Pinecone vector store")
                docs = load_documents()
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500, chunk_overlap=50
                )
                chunks = splitter.split_documents(docs)
                vector_store = get_vector_store()
                vector_store.add_documents(chunks)
                logger.info("Successfully indexed %d document chunks", len(chunks))
            except Exception as e:
                logger.exception("Failed to auto-ingest documents")

            time.sleep(interval_minutes * 60)

    thread = threading.Thread(target=ingest, daemon=True)
    thread.start()


auto_ingest_documents()
