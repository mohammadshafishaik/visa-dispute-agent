# 🏦 Visa Dispute Resolution System

An AI-powered, event-driven autonomous agent for automated Visa dispute resolution with bank-style validation and real-time email notifications.

## ✨ Features

- 🤖 **AI-Powered Decision Making** - Uses LLM with 2,278 Visa rules for intelligent dispute resolution
- 🏦 **Bank-Style 7-Layer Validation** - Professional validation with clear rejection codes
- 📧 **Real-Time Email Notifications** - Automated email updates via Gmail SMTP or SendGrid
- 🌐 **Professional Web Interface** - User-friendly form with instant validation feedback
- 🔄 **Event-Driven Architecture** - LangGraph state machine for reliable processing
- 📊 **Human Review Queue** - Low-confidence cases escalated to specialists
- 🔍 **RAG-Based Research** - ChromaDB vector store with Visa rule retrieval
- 🛡️ **Security Features** - Rate limiting, input validation, audit logging

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Ollama (for local LLM) or OpenAI API key

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/visa-dispute-agent.git
cd visa-dispute-agent
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

Required environment variables:
```bash
# Email Configuration
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Database
DATABASE_URL=postgresql://visa_user:visa_password@postgres:5432/visa_disputes

# LLM
LLM_MODEL=llama3.2
LLM_PROVIDER=ollama
```

### 3. Start Services

```bash
docker-compose up -d
```

### 4. Access Application

- **Web Interface**: http://localhost:8000/
- **API Health**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs

## 📖 Documentation

- [Installation Guide](INSTALLATION_GUIDE.md) - Detailed setup instructions
- [API Documentation](API_DOCUMENTATION.md) - API endpoints and usage
- [Architecture](ARCHITECTURE.md) - System design and components
- [Email Setup](SENDGRID_SETUP.md) - Configure email notifications
- [Deployment Guide](GITHUB_DEPLOYMENT.md) - Deploy to cloud platforms
- [Testing](TESTING.md) - Run tests and validation

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Web Form   │────▶│  Validation  │────▶│ LangGraph   │
│  /API       │     │  (7 Layers)  │     │ State       │
└─────────────┘     └──────────────┘     │ Machine     │
                                          └──────┬──────┘
                                                 │
                    ┌────────────────────────────┼────────────────┐
                    ▼                            ▼                ▼
            ┌───────────────┐          ┌─────────────┐   ┌──────────────┐
            │ RAG Retrieval │          │ Adjudication│   │ Email Service│
            │ (ChromaDB)    │          │ (LLM)       │   │ (SMTP/SendGrid)│
            └───────────────┘          └─────────────┘   └──────────────┘
```

## 🔧 Technology Stack

- **Backend**: FastAPI, Python 3.11
- **AI/LLM**: LangChain, LangGraph, Ollama/OpenAI
- **Vector Store**: ChromaDB
- **Database**: PostgreSQL
- **Email**: Gmail SMTP / SendGrid
- **Deployment**: Docker, Docker Compose

## 📊 Validation Layers

1. **Customer Authentication** - ID format, name validation
2. **Transaction Validation** - ID, card number, merchant
3. **Amount Validation** - Range checks, suspicious patterns
4. **Timing Validation** - 120-day Visa rule compliance
5. **Fraud Detection** - Pattern analysis
6. **Documentation** - Description requirements
7. **Contact Information** - Email, phone validation

## 🧪 Testing

```bash
# Run all tests
pytest

# Test specific component
pytest tests/test_validation.py

# Test email service
docker exec ragproject-app-1 python -c "from app.tools.unified_email_service import unified_email_service; print(unified_email_service.send_dispute_decision(...))"
```

## 📧 Email Configuration

### Option 1: Gmail SMTP (Quick Setup)

1. Enable 2-Step Verification in Gmail
2. Generate App Password
3. Add to `.env`:
   ```bash
   SMTP_EMAIL=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

### Option 2: SendGrid (Recommended for Production)

1. Create free SendGrid account
2. Generate API key
3. Add to `.env`:
   ```bash
   SENDGRID_API_KEY=SG.your-api-key
   ```

See [SENDGRID_SETUP.md](SENDGRID_SETUP.md) for detailed instructions.

## 🚀 Deployment

### Deploy to Render.com (Free Tier)

1. Push to GitHub
2. Connect repository to Render
3. Set environment variables
4. Deploy!

See [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) for detailed deployment instructions.

## 📝 API Usage

### Submit Dispute

```bash
curl -X POST http://localhost:8000/webhooks/dispute \
  -H "Content-Type: application/json" \
  -d '{
    "dispute_id": "DSP-001",
    "customer_id": "CUST1234",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "transaction_id": "TXN123456",
    "transaction_date": "2024-11-25",
    "merchant_name": "Amazon",
    "card_number": "1234",
    "amount": 1000.00,
    "currency": "INR",
    "reason_code": "10.4",
    "description": "Unauthorized transaction on my card",
    "timestamp": "2024-11-29T10:00:00Z"
  }'
```

### Check Status

```bash
curl http://localhost:8000/disputes/DSP-001
```

## 🔒 Security

- ✅ Input validation on all endpoints
- ✅ Rate limiting (100 requests/minute)
- ✅ SQL injection prevention
- ✅ Environment variable secrets
- ✅ Audit logging
- ✅ CORS configuration

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 👥 Authors

- Shaik Shafi - Initial work

## 🙏 Acknowledgments

- Visa for dispute resolution rules
- LangChain for AI orchestration
- FastAPI for the web framework

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Check documentation in `/docs`
- Review troubleshooting guide

---

**Built with ❤️  and modern Python**
