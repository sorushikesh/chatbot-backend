import logging
from pymongo import MongoClient
from langchain.schema import Document
from app.core.config import settings

logger = logging.getLogger(__name__)

def convert_transaction_doc(doc: dict) -> list[Document]:
    documents = []

    for txn in doc.get("transactions", []):
        parts = [
            f"Transaction ID: {txn.get('txn_id')}",
            f"Type: {txn.get('type')}",
            f"Amount: {txn.get('amount')}",
            f"Description: {txn.get('description')}",
            f"Timestamp: {txn.get('timestamp')}",
            f"Account Number: {doc.get('accountNumber')}",
            f"Transaction Date: {doc.get('date')}"
        ]

        if txn.get("type") == "credit" and "creditor" in txn:
            parts.append(f"Creditor: {txn['creditor'].get('name')} (IBAN: {txn['creditor'].get('iban')}, BIC: {txn['creditor'].get('bic')})")
        elif txn.get("type") == "debit" and "debtor" in txn:
            parts.append(f"Debtor: {txn['debtor'].get('name')} (IBAN: {txn['debtor'].get('iban')}, BIC: {txn['debtor'].get('bic')})")

        text = "\n".join(parts)

        metadata = {
            "_id": str(doc.get("_id")),
            "accountNumber": doc.get("accountNumber"),
            "txn_id": txn.get("txn_id"),
            "date": doc.get("date"),
            "type": txn.get("type")
        }

        documents.append(Document(page_content=text, metadata=metadata))

    return documents

def load_documents() -> list[Document]:
    logger.info("Connecting to MongoDB")
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]

    all_documents = []
    collection = db["TRANSACTIONS"]

    logger.info("Fetching documents from 'TRANSACTIONS' collection")
    for doc in collection.find():
        tx_docs = convert_transaction_doc(doc)
        all_documents.extend(tx_docs)

    logger.info("Prepared %d document chunks from MongoDB", len(all_documents))
    return all_documents
