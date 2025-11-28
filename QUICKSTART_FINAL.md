# 🚀 VISA DISPUTE AGENT - QUICK START

## ⚡ Get Started in 3 Minutes

### Prerequisites
- Docker & Docker Compose installed
- Ollama installed (`brew install ollama` on Mac)

---

## Step 1: Start Ollama (1 minute)

```bash
# Start Ollama server
ollama serve

# In another terminal, pull the model
ollama pull llama3.2
```

---

## Step 2: Start the System (1 minute)

```bash
# Start all services
docker-compose up -d

# Wait for services to be ready (~30 seconds)
sleep 30

# Check health
curl http://localhost:8000/health
```

Expected output:
```json
{
    "status": "healthy",
    "database": "healthy",
    "vector_store": "healthy (2278 documents)",
    "version": "0.1.0"
}
```

---

## Step 3: Test It! (1 minute)

```bash
# Run the test suite
./test_system.sh
```

You should see:
```
✓ System is operational
✓ API endpoints responding
✓ Dispute submission working
✓ Multiple dispute types tested
```

---

## 🎯 Try Your First Dispute

```bash
curl -X POST http://localhost:8000/webhooks/dispute \
  -H "Content-Type: application/json" \
  -d '{
    "dispute_id": "MY-FIRST-DISPUTE",
    "customer_id": "CUST-001",
    "transaction_id": "TXN-001",
    "amount": 99.99,
    "currency": "USD",
    "reason_code": "10.4",
    "description": "Unauthorized online purchase",
    "timestamp": "2024-11-28T10:00:00Z"
  }'
```

Response:
```json
{
    "status": "accepted",
    "dispute_id": "MY-FIRST-DISPUTE",
    "message": "Dispute received and processing initiated"
}
```

---

## 📊 What Happens Next?

The system will:
1. ✅ Search through 2,278 Visa rules
2. ✅ Analyze fraud patterns
3. ✅ Make an AI-powered decision
4. ✅ Route based on confidence:
   - High confidence (≥85%) → Automated action
   - Low confidence (<85%) → Human review

---

## 🔍 Check Results

### View Review Queue
```bash
curl http://localhost:8000/review-queue | python3 -m json.tool
```

### View Logs
```bash
docker-compose logs -f app
```

---

## 🛑 Stop the System

```bash
docker-compose down
```

---

## 📚 Next Steps

- Read `PROJECT_COMPLETE.md` for full documentation
- Check `API_DOCUMENTATION.md` for API details
- See `ARCHITECTURE.md` for system design
- Run `./test_system.sh` for comprehensive tests

---

## 💡 Tips

- **Slow responses?** The first LLM call takes longer (model loading)
- **Need more rules?** Add them to `scripts/extracted_visa_rules.json`
- **Want to customize?** Edit `app/config/settings.py`
- **Debugging?** Check logs with `docker-compose logs -f`

---

## ✅ You're Ready!

Your Visa Dispute Agent is now running with:
- 2,278 real Visa rules
- Free local AI (Ollama)
- Complete audit trail
- Production-ready architecture

**Happy disputing! 🎉**
