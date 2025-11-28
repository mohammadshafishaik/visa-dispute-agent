"""Extract Visa rules from PDF and prepare for ChromaDB seeding"""
import sys
import os
import re
import json
from typing import List, Dict
import pdfplumber

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from PDF"""
    print(f"Opening PDF: {pdf_path}")
    text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        for i, page in enumerate(pdf.pages, 1):
            if i % 10 == 0:
                print(f"Processing page {i}...")
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    
    return text


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at sentence boundary
        if end < text_length:
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)
            
            if break_point > chunk_size * 0.5:  # Only break if we're past halfway
                chunk = chunk[:break_point + 1]
                end = start + break_point + 1
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return chunks


def extract_reason_codes(text: str) -> List[Dict]:
    """Extract reason codes and their descriptions"""
    rules = []
    
    # Pattern to match reason codes like "10.4", "13.1", etc.
    pattern = r'(\d+\.\d+)\s*[-–—]\s*([^\n]+)'
    matches = re.finditer(pattern, text)
    
    for match in matches:
        code = match.group(1)
        description = match.group(2).strip()
        
        # Find context around this code (next 500 chars)
        start_pos = match.start()
        context = text[start_pos:start_pos + 800]
        
        rules.append({
            "reason_code": code,
            "description": description,
            "context": context
        })
    
    return rules


def create_structured_rules(text: str) -> List[Dict]:
    """Create structured rules from PDF text"""
    print("\nExtracting structured rules...")
    
    # Extract reason codes
    reason_codes = extract_reason_codes(text)
    print(f"Found {len(reason_codes)} reason codes")
    
    # Create chunks for general content
    chunks = chunk_text(text, chunk_size=1000, overlap=200)
    print(f"Created {len(chunks)} text chunks")
    
    rules = []
    
    # Add reason code rules with unique IDs
    for i, rc in enumerate(reason_codes):
        rules.append({
            "id": f"visa_reason_code_{rc['reason_code'].replace('.', '_')}_{i:04d}",
            "content": f"Visa Reason Code {rc['reason_code']} - {rc['description']}\n\n{rc['context']}",
            "metadata": {
                "type": "reason_code",
                "reason_code": rc['reason_code'],
                "category": "dispute_reason"
            }
        })
    
    # Add general content chunks
    for i, chunk in enumerate(chunks):
        if len(chunk) > 100:  # Only add substantial chunks
            # Try to identify category from content
            category = "general"
            if any(word in chunk.lower() for word in ["fraud", "unauthorized", "counterfeit"]):
                category = "fraud"
            elif any(word in chunk.lower() for word in ["service", "merchandise", "delivery"]):
                category = "service_dispute"
            elif any(word in chunk.lower() for word in ["time limit", "deadline", "days"]):
                category = "time_limits"
            elif any(word in chunk.lower() for word in ["evidence", "documentation", "proof"]):
                category = "evidence"
            
            rules.append({
                "id": f"visa_rule_chunk_{i:04d}",
                "content": chunk,
                "metadata": {
                    "type": "content_chunk",
                    "category": category,
                    "chunk_index": i
                }
            })
    
    return rules


def main():
    pdf_path = "visa-rules-public copy.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return
    
    print("=" * 60)
    print("VISA RULES EXTRACTION")
    print("=" * 60)
    
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    print(f"\nExtracted {len(text)} characters from PDF")
    
    # Create structured rules
    rules = create_structured_rules(text)
    print(f"\nTotal rules created: {len(rules)}")
    
    # Save to JSON for review
    output_file = "scripts/extracted_visa_rules.json"
    with open(output_file, 'w') as f:
        json.dump(rules, f, indent=2)
    
    print(f"\nRules saved to: {output_file}")
    print("\nSample rules:")
    for rule in rules[:3]:
        print(f"\n- ID: {rule['id']}")
        print(f"  Category: {rule['metadata'].get('category', 'N/A')}")
        print(f"  Content preview: {rule['content'][:150]}...")
    
    print("\n" + "=" * 60)
    print(f"✓ Successfully extracted {len(rules)} rules")
    print("=" * 60)
    
    return rules


if __name__ == "__main__":
    main()
