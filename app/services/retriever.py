import logging
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from app.services.vector_store import get_vector_store
from app.core.config import settings

logger = logging.getLogger(__name__)

QA_TEMPLATE = """
You are a helpful, polite assistant with financial domain knowledge.
Use the following context to answer the user's question naturally and clearly.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}

Answer:
"""

PROMPT = PromptTemplate(
    template=QA_TEMPLATE,
    input_variables=["context", "question"]
)

def build_qa_chain():
    retriever = get_vector_store().as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5}
    )

    llm = AzureChatOpenAI(
        azure_deployment=settings.AZURE_DEPLOYMENT,
        azure_endpoint=settings.AZURE_ENDPOINT,
        api_key=settings.AZURE_API_KEY,
        api_version=settings.AZURE_API_VERSION
    )

    logger.info("QA chain initialized with NLP-enhanced prompt")

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )
