"""Seed ChromaDB with extracted Visa rules from PDF"""
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.vector_store import get_vector_store


def seed_database() -> None:
    """Seed ChromaDB with extracted Visa rules"""
    print("=" * 60)
    print("SEEDING CHROMADB WITH VISA RULES")
    print("=" * 60)
    
    # Load extracted rules
    rules_file = "scripts/extracted_visa_rules.json"
    if not os.path.exists(rules_file):
        print(f"Error: {rules_file} not found. Run extract_visa_rules.py first.")
        return
    
    print(f"\nLoading rules from {rules_file}...")
    with open(rules_file, 'r') as f:
        rules = json.load(f)
    
    print(f"Loaded {len(rules)} rules")
    
    print("\nInitializing ChromaDB connection...")
    vector_store = get_vector_store()
    vector_store.initialize()
    
    current_count = vector_store.get_collection_count()
    print(f"Current collection count: {current_count}")
    
    if current_count > 0:
        print("\n⚠️  Collection already contains documents. Adding new rules...")
    
    print(f"\nSeeding {len(rules)} Visa rules...")
    print("This may take a few minutes...")
    
    # Process in batches to avoid memory issues
    batch_size = 100
    total_batches = (len(rules) + batch_size - 1) // batch_size
    
    for i in range(0, len(rules), batch_size):
        batch = rules[i:i + batch_size]
        batch_num = i // batch_size + 1
        
        documents = [rule["content"] for rule in batch]
        metadatas = [rule["metadata"] for rule in batch]
        ids = [rule["id"] for rule in batch]
        
        vector_store.add_documents(documents, metadatas, ids)
        
        print(f"  Batch {batch_num}/{total_batches} complete ({len(batch)} rules)")
    
    final_count = vector_store.get_collection_count()
    print(f"\n✓ Successfully seeded {len(rules)} documents.")
    print(f"✓ Final collection count: {final_count}")
    print("=" * 60)


if __name__ == "__main__":
    seed_database()
