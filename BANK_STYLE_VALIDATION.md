# 🏦 Bank-Style Authentication & Rejection System

## Overview

Your dispute system now has **7-layer bank-style validation** that automatically rejects invalid disputes before they reach the AI - just like how banks validate transactions!

---

## 🛡️ 7 Layers of Validation

### Layer 1: Customer Authentication
- Customer ID must be exactly 8 characters
- Format: 4 UPPERCASE letters + 4 numbers (e.g., CUST1234, BANK5678)
- Customer name must be at least 3 characters
- Only letters, spaces, and periods allowed in name

**Rejection Codes:**
- `AUTH001`: Customer authentication failed
- `AUTH002`: Invalid customer credentials

### Layer 2: Transaction Validation
- Transaction ID must be at least 5 characters
- Card number must be exactly 4 digits
- Merchant name must be at least 2 characters

**Rejection Codes:**
- `CARD001`: Card number invalid
- `MERCH001`: Invalid merchant name
- `MERCH002`: Transaction not found

### Layer 3: Amount Validation
- Minimum: ₹1
- Maximum: ₹1,00,00,000 (1 crore)
- Detects suspicious patterns (123456, 999999, etc.)

**Rejection Codes:**
- `AMOUNT001`: Amount exceeds limit
- `AMOUNT002`: Amount below minimum
- `AMOUNT003`: Suspicious amount pattern

### Layer 4: Time-Based Validation
- Transaction date cannot be in future
- Must file within 120 days of transaction (Visa rule)
- Date format must be valid

**Rejection Codes:**
- `TIME001`: Future date not allowed
- `TIME002`: Filed too late (>120 days)
- `TIME003`: Invalid date format

### Layer 5: Fraud Detection
- Detects test/spam submissions
- Checks for repeated characters
- Validates description quality
- Minimum 5 words required

**Rejection Codes:**
- `FRAUD001`: Multiple disputes detected
- `FRAUD002`: Suspicious activity pattern
- `FRAUD003`: Customer flagged

### Layer 6: Documentation Validation
- Description: 20-1000 characters
- Reason code must be valid
- Description must match reason code
- Validates keywords match dispute type

**Rejection Codes:**
- `DOC001`: Insufficient documentation
- `DOC002`: Description doesn't match type
- `REASON001`: Invalid reason code
- `REASON002`: Reason doesn't match description

### Layer 7: Contact Information
- Email must be valid format
- No temporary/disposable emails
- Phone must be 10-15 digits
- Comprehensive format validation

**Rejection Codes:**
- `CONTACT001`: Invalid email
- `CONTACT002`: Invalid phone
- `CONTACT003`: Contact info mismatch

---

## 📋 Reason Code Validation

The system validates that your description matches the reason code:

| Code | Type | Required Keywords |
|------|------|-------------------|
| 10.1 | Counterfeit | counterfeit, fake, cloned |
| 10.4 | Fraud | fraud, unauthorized, didn't make |
| 11.1 | Authorization | authorization, declined, not approved |
| 12.1 | Processing Error | processing, error, duplicate |
| 13.1 | Not Received | not received, never received, didn't receive |
| 13.2 | Cancelled Recurring | cancelled, recurring, subscription |
| 13.3 | Not as Described | not as described, defective, damaged, wrong item |

---

## ✅ Example: Valid Submission

```json
{
  "customer_id": "CUST1234",
  "customer_name": "John Smith",
  "email": "john@example.com",
  "phone": "+919876543210",
  "transaction_id": "TXN123456",
  "amount": 5000,
  "reason_code": "10.4",
  "description": "This is an unauthorized transaction. I did not make this purchase and suspect fraud on my account.",
  "transaction_date": "2024-11-15"
}
```

**Result**: ✅ Accepted - Proceeds to AI analysis

---

## ❌ Example: Rejected Submissions

### Rejection 1: Invalid Customer ID
```json
{
  "customer_id": "cust123",  // ❌ Wrong format
  ...
}
```
**Result**: 
```
REJECTED [AUTH002]
Customer ID must be 4 UPPERCASE letters followed by 4 numbers.
Example: BANK5678
```

### Rejection 2: Description Doesn't Match Reason
```json
{
  "reason_code": "10.4",  // Fraud
  "description": "Product was damaged"  // ❌ Doesn't mention fraud
}
```
**Result**:
```
REJECTED [REASON002]
Description does not match reason code 10.4.
Expected keywords: fraud, unauthorized, didn't make
```

### Rejection 3: Amount Too High
```json
{
  "amount": 15000000  // ❌ Over 1 crore
}
```
**Result**:
```
REJECTED [AMOUNT001]
Amount exceeds maximum limit.
Disputes over ₹1,00,00,000 require branch visit.
```

### Rejection 4: Filed Too Late
```json
{
  "transaction_date": "2024-01-01"  // ❌ Over 120 days ago
}
```
**Result**:
```
REJECTED [TIME002]
Dispute filed too late. Must be filed within 120 days of transaction.
Transaction was 150 days ago.
```

---

## 🎯 How It Works

```
User submits form
    ↓
Layer 1: Customer Auth ✓
    ↓
Layer 2: Transaction ✓
    ↓
Layer 3: Amount ✓
    ↓
Layer 4: Timing ✓
    ↓
Layer 5: Fraud Check ✓
    ↓
Layer 6: Documentation ✓
    ↓
Layer 7: Contact Info ✓
    ↓
All Pass? → AI Analysis
Any Fail? → REJECTED with code
```

---

## 🔍 Testing Rejections

### Test 1: Invalid Customer ID
- Customer ID: `test123` (lowercase)
- Expected: `AUTH002` rejection

### Test 2: Spam Detection
- Description: "test test test test test"
- Expected: `FRAUD002` rejection

### Test 3: Wrong Reason Code
- Reason: 10.4 (Fraud)
- Description: "Product not received"
- Expected: `REASON002` rejection

### Test 4: Invalid Email
- Email: "notanemail"
- Expected: `CONTACT001` rejection

---

## 📊 Rejection Statistics

The system logs all rejections with:
- Rejection code
- Rejection message
- Timestamp
- Customer details
- Reason for rejection

View rejections in audit logs:
```bash
docker-compose logs app | grep "REJECTED"
```

---

## 💡 Benefits

1. **Instant Feedback**: Users know immediately what's wrong
2. **Reduced AI Load**: Invalid disputes never reach AI
3. **Better Data Quality**: Only valid disputes processed
4. **Fraud Prevention**: Detects suspicious patterns
5. **Compliance**: Enforces Visa 120-day rule
6. **User Guidance**: Clear error messages help users fix issues

---

## 🎓 Bank-Style Features

Just like real banks:
- ✅ Multi-layer validation
- ✅ Rejection codes (like bank error codes)
- ✅ Time-based rules (120-day limit)
- ✅ Fraud detection
- ✅ Amount limits
- ✅ Documentation requirements
- ✅ Contact verification

---

**Your system now validates disputes like a professional bank!** 🏦
