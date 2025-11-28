# 🌐 WEB INTERFACE - USER GUIDE

## ✨ Beautiful Web UI for Dispute Submission

Your Visa Dispute Agent now has a **beautiful web interface**! No more terminal commands - just fill out a form and get instant results!

---

## 🚀 Access the Web Interface

### Open in Your Browser
```
http://localhost:8000/
```

That's it! The web interface will load automatically.

---

## 📝 How to Use

### Step 1: Fill Out the Form

The form asks for:

1. **Customer Name** - Full name (e.g., "John Doe")
2. **Customer ID** - Unique customer identifier (e.g., "CUST-12345")
3. **Card Number** - Last 4 digits only (e.g., "1234")
4. **Transaction ID** - Transaction reference (e.g., "TXN-98765")
5. **Dispute Amount** - Amount in dollars (e.g., "299.99")
6. **Reason Code** - Select from dropdown:
   - 10.4 - Fraud (Card Absent)
   - 10.1 - Counterfeit Fraud
   - 11.1 - Card Recovery Bulletin
   - 12.1 - Late Presentment
   - 13.1 - Services Not Provided
   - 13.2 - Cancelled Recurring
   - 13.3 - Not as Described
7. **Description** - Detailed explanation of the issue

### Step 2: Submit

Click the **"Submit Dispute"** button.

### Step 3: Get Instant Results

The system will:
1. Show a processing animation
2. Analyze against 2,278 Visa rules
3. Make an AI-powered decision
4. Display the result in 3-5 seconds

---

## 🎯 What You'll See

### ✅ Automated Decision (High Confidence)
```
✅ Dispute Processed Successfully

Dispute ID: DSP-1234567890
Status: ACCEPTED
Customer: John Doe
Amount: $299.99
Reason: 10.4

Your dispute has been automatically processed by our AI system.
You will receive an email with the decision shortly.
```

### 👤 Human Review (Low Confidence)
```
👤 Escalated to Human Review

Dispute ID: DSP-1234567890
Status: Pending Review
Confidence: 72.5%
Decision: ESCALATE
Reasoning: Complex case requiring specialist review

This case requires human review due to complexity or low confidence.
A specialist will review it within 24 hours.
```

### ❌ Error
```
❌ Error

Submission failed: [error message]

Please try again or contact support.
```

---

## 🎨 Features

### Beautiful Design
- Modern gradient background
- Clean, professional interface
- Smooth animations
- Mobile-responsive

### Real-Time Processing
- Live status updates
- Processing animation
- Instant results
- No page refresh needed

### Smart Validation
- Required field checking
- Format validation
- Helpful error messages
- Auto-generated dispute IDs

---

## 📱 Screenshots

### Main Form
```
┌─────────────────────────────────────────┐
│  💳 Visa Dispute Agent                  │
│  AI-Powered Dispute Resolution System   │
├─────────────────────────────────────────┤
│                                         │
│  🤖 Powered by AI: 2,278 Visa rules    │
│                                         │
│  Customer Name *                        │
│  [John Doe                    ]         │
│                                         │
│  Customer ID *                          │
│  [CUST-12345                  ]         │
│                                         │
│  Card Number (Last 4 digits) *         │
│  [1234]                                 │
│                                         │
│  Transaction ID *                       │
│  [TXN-98765                   ]         │
│                                         │
│  Dispute Amount ($) *                   │
│  [299.99                      ]         │
│                                         │
│  Reason Code *                          │
│  [10.4 - Fraud (Card Absent) ▼]        │
│                                         │
│  Description *                          │
│  [Unauthorized transaction...  ]        │
│  [                             ]        │
│                                         │
│  [    Submit Dispute    ]               │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔧 Technical Details

### How It Works

1. **Form Submission** → JavaScript captures form data
2. **API Call** → Sends POST request to `/webhooks/dispute`
3. **Processing** → Backend analyzes with AI
4. **Status Check** → Checks review queue
5. **Display Result** → Shows outcome to user

### Behind the Scenes

```javascript
// Form data is converted to API payload
{
    "dispute_id": "DSP-1701234567",
    "customer_id": "CUST-12345",
    "transaction_id": "TXN-98765",
    "amount": 299.99,
    "currency": "USD",
    "reason_code": "10.4",
    "description": "Unauthorized transaction...",
    "timestamp": "2024-11-28T10:00:00Z"
}
```

---

## 💡 Tips

### For Best Results
- Provide detailed descriptions
- Use correct reason codes
- Double-check amounts
- Include all relevant information

### Common Reason Codes
- **10.4** - Most common for online fraud
- **13.1** - For non-delivery issues
- **13.3** - For quality/description issues

### Processing Time
- **High confidence**: 3-5 seconds
- **Low confidence**: 3-5 seconds + human review
- **Average**: Under 10 seconds

---

## 🎉 Advantages Over Terminal

| Feature | Terminal | Web Interface |
|---------|----------|---------------|
| **Ease of Use** | Complex commands | Simple form |
| **Visual Feedback** | Text only | Beautiful UI |
| **Error Handling** | JSON errors | User-friendly messages |
| **Mobile Friendly** | No | Yes |
| **User Experience** | Technical | Intuitive |

---

## 🚀 Quick Start

### 1. Start the System
```bash
docker-compose up -d
```

### 2. Open Browser
```
http://localhost:8000/
```

### 3. Submit a Dispute
Fill out the form and click submit!

---

## 📊 Example Scenarios

### Scenario 1: Fraud Dispute
```
Customer Name: Jane Smith
Customer ID: CUST-99999
Card Number: 5678
Transaction ID: TXN-FRAUD-001
Amount: $599.99
Reason Code: 10.4 - Fraud (Card Absent)
Description: Unauthorized online purchase. Customer denies making this transaction.

Result: ✅ Automatically approved (High confidence: 92%)
```

### Scenario 2: Service Dispute
```
Customer Name: Bob Johnson
Customer ID: CUST-88888
Card Number: 9012
Transaction ID: TXN-SERVICE-001
Amount: $149.99
Reason Code: 13.1 - Services Not Provided
Description: Ordered product never arrived despite tracking showing delivered.

Result: 👤 Escalated to human review (Confidence: 68%)
```

---

## 🎊 You're Ready!

Your Visa Dispute Agent now has a **professional web interface** that anyone can use - no technical knowledge required!

**Access it now**: http://localhost:8000/

---

*Beautiful, Fast, and Intelligent Dispute Resolution* ✨
