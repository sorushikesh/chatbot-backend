import logging
from pymongo import MongoClient
from langchain.schema import Document
from app.core.config import settings

logger = logging.getLogger(__name__)

from typing import List

def convert_transaction_doc(doc: dict) -> List[Document]:
    txn_type = doc.get("transactionType", "").lower()

    parts = [
        f"Transaction ID: {doc.get('transactionId')}",
        f"Type: {txn_type}",
        f"Amount: {doc.get('amount')} {doc.get('currency')}",
        f"Description: {doc.get('description')}",
        f"Category: {doc.get('category')}",
        f"Status: {doc.get('status')}",
        f"Reference Number: {doc.get('referenceNumber')}",
        f"Transaction Date: {doc.get('transactionDate')}",
        f"Account Key: {doc.get('accountKey')}"
    ]

    if txn_type == "credit" and "creditor" in doc:
        creditor = doc["creditor"]
        parts.append(
            f"Creditor: {creditor.get('name')} (IBAN: {creditor.get('iban')}, BIC: {creditor.get('bic')})"
        )
    elif txn_type == "debit" and "debtor" in doc:
        debtor = doc["debtor"]
        parts.append(
            f"Debtor: {debtor.get('name')} (IBAN: {debtor.get('iban')}, BIC: {debtor.get('bic')})"
        )

    text = "\n".join(parts)

    metadata = {
        "_id": str(doc.get("_id", "")),
        "transactionId": doc.get("transactionId"),
        "accountKey": doc.get("accountKey"),
        "type": txn_type,
        "status": doc.get("status"),
        "category": doc.get("category"),
        "date": doc.get("transactionDate")
    }

    return [Document(page_content=text, metadata=metadata)]

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
