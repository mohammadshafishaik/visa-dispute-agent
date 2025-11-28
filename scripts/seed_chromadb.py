"""Seed ChromaDB with sample Visa rules and regulations"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.vector_store import get_vector_store


# Sample Visa rules for dispute resolution
VISA_RULES = [
    {
        "id": "visa_rule_001",
        "content": "Visa Reason Code 10.4 - Other Fraud, Card Absent Environment. "
                   "Cardholder claims they did not authorize or participate in a transaction "
                   "conducted in a card-absent environment (e.g., online, phone, mail order). "
                   "Time limit: 120 days from transaction processing date.",
        "metadata": {"category": "fraud", "reason_code": "10.4", "environment": "card_absent"}
    },
    {
        "id": "visa_rule_002",
        "content": "Visa Reason Code 13.1 - Services Not Provided or Merchandise Not Received. "
                   "Cardholder claims they did not receive goods or services as agreed. "
                   "Merchant must provide proof of delivery or service completion. "
                   "Time limit: 120 days from expected delivery date.",
        "metadata": {"category": "service_dispute", "reason_code": "13.1"}
    },
    {
        "id": "visa_rule_003",
        "content": "Visa Reason Code 13.3 - Not as Described or Defective Merchandise. "
                   "Cardholder claims merchandise or services were not as described or defective. "
                   "Cardholder must have attempted to return merchandise or resolve with merchant. "
                   "Time limit: 120 days from transaction date.",
        "metadata": {"category": "quality_dispute", "reason_code": "13.3"}
    },
    {
        "id": "visa_rule_004",
        "content": "Visa Chargeback Time Limits. Cardholders have 120 days from the transaction "
                   "processing date or expected delivery date to file a dispute. Merchants have "
                   "30 days to respond to a chargeback with supporting documentation. "
                   "Failure to respond within time limits results in automatic liability.",
        "metadata": {"category": "time_limits", "type": "procedural"}
    },
    {
        "id": "visa_rule_005",
        "content": "Friendly Fraud Detection. Patterns indicating friendly fraud include: "
                   "multiple chargebacks from same cardholder, disputes filed after merchandise "
                   "delivery confirmation, disputes for digital goods with confirmed access, "
                   "high-value disputes without merchant contact attempts. "
                   "Chargeback rate above 1% indicates potential friendly fraud patterns.",
        "metadata": {"category": "fraud_detection", "type": "friendly_fraud"}
    },
    {
        "id": "visa_rule_006",
        "content": "Visa Reason Code 11.1 - Card Recovery Bulletin or Exception File. "
                   "Transaction processed on a card listed in the Card Recovery Bulletin. "
                   "Merchant must check authorization and card validity at time of transaction. "
                   "Time limit: 120 days from transaction processing date.",
        "metadata": {"category": "authorization", "reason_code": "11.1"}
    },
    {
        "id": "visa_rule_007",
        "content": "Visa Reason Code 12.1 - Late Presentment. Transaction not presented within "
                   "required time frame. Visa requires transactions to be presented within "
                   "specified time limits based on transaction type and region. "
                   "Merchant liability if presentment is late.",
        "metadata": {"category": "processing_error", "reason_code": "12.1"}
    },
    {
        "id": "visa_rule_008",
        "content": "Compelling Evidence for Fraud Disputes. To counter fraud claims, merchants "
                   "must provide: IP address matching cardholder's location, device fingerprint "
                   "matching previous legitimate transactions, delivery address matching billing "
                   "address, cardholder communication history, previous undisputed transactions "
                   "from same account.",
        "metadata": {"category": "evidence_requirements", "type": "fraud_defense"}
    },
    {
        "id": "visa_rule_009",
        "content": "Visa Reason Code 13.2 - Cancelled Recurring Transaction. Cardholder claims "
                   "they cancelled a recurring transaction but were still charged. Merchant must "
                   "provide proof that cancellation was not properly requested or that service "
                   "was provided after cancellation request. Time limit: 120 days from transaction date.",
        "metadata": {"category": "recurring_billing", "reason_code": "13.2"}
    },
    {
        "id": "visa_rule_010",
        "content": "Visa Dispute Resolution Framework. All disputes must follow the standard "
                   "workflow: cardholder files dispute with issuer, issuer reviews and may file "
                   "chargeback, merchant responds with evidence, issuer makes final decision. "
                   "If merchant disagrees, they may escalate to pre-arbitration. "
                   "Arbitration is final and binding with fees for losing party.",
        "metadata": {"category": "procedural", "type": "dispute_workflow"}
    },
    {
        "id": "visa_rule_011",
        "content": "Visa Authorization Requirements. Merchants must obtain authorization for all "
                   "transactions. Authorization confirms card validity and available funds. "
                   "Failure to obtain authorization or processing after authorization decline "
                   "results in merchant liability for disputes. Authorization codes must be "
                   "retained for dispute defense.",
        "metadata": {"category": "authorization", "type": "requirements"}
    },
    {
        "id": "visa_rule_012",
        "content": "Visa Reason Code 10.1 - EMV Liability Shift Counterfeit Fraud. Counterfeit "
                   "card transaction at chip-enabled terminal. If merchant's terminal is not "
                   "chip-enabled, merchant is liable. If terminal is chip-enabled and chip was "
                   "read, issuer is liable. Time limit: 120 days from transaction processing date.",
        "metadata": {"category": "fraud", "reason_code": "10.1", "type": "counterfeit"}
    },
]


def seed_database() -> None:
    """Seed ChromaDB with Visa rules"""
    print("Initializing ChromaDB connection...")
    vector_store = get_vector_store()
    vector_store.initialize()
    
    print(f"Current collection count: {vector_store.get_collection_count()}")
    
    if vector_store.get_collection_count() > 0:
        print("Collection already contains documents. Skipping seed.")
        return
    
    print(f"Seeding {len(VISA_RULES)} Visa rules...")
    
    documents = [rule["content"] for rule in VISA_RULES]
    metadatas = [rule["metadata"] for rule in VISA_RULES]
    ids = [rule["id"] for rule in VISA_RULES]
    
    vector_store.add_documents(documents, metadatas, ids)
    
    print(f"Successfully seeded {len(VISA_RULES)} documents.")
    print(f"Final collection count: {vector_store.get_collection_count()}")


if __name__ == "__main__":
    seed_database()
