# SendGrid Email Setup (Alternative to Gmail)

SendGrid is more reliable than Gmail SMTP for sending transactional emails. It has a free tier with 100 emails/day.

## Why SendGrid?

- ✅ More reliable delivery
- ✅ Better for transactional emails
- ✅ No 2FA/App Password hassles
- ✅ Better deliverability (less likely to go to spam)
- ✅ Free tier: 100 emails/day

## Setup Steps

### 1. Create SendGrid Account

1. Go to https://signup.sendgrid.com/
2. Sign up for a free account
3. Verify your email address

### 2. Create API Key

1. Log in to SendGrid dashboard
2. Go to **Settings** → **API Keys**
3. Click **Create API Key**
4. Name it: "Dispute System"
5. Select **Full Access** (or at least Mail Send access)
6. Click **Create & View**
7. **COPY THE API KEY** (you won't see it again!)

### 3. Verify Sender Identity

1. Go to **Settings** → **Sender Authentication**
2. Click **Verify a Single Sender**
3. Fill in your details:
   - From Name: Dispute Resolution System
   - From Email: your-email@gmail.com (or any email you own)
   - Reply To: same email
4. Check your email and click the verification link

### 4. Update .env File

Add to your `.env` file:

```bash
# SendGrid Configuration (Primary - more reliable)
SENDGRID_API_KEY=SG.your-api-key-here

# Gmail SMTP (Fallback)
SMTP_EMAIL=sk.mohammadshafi3044@gmail.com
SMTP_PASSWORD=tmicsjfjtkenuszq
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 5. Install SendGrid Package

```bash
# In your project directory
pip install sendgrid

# Or add to requirements.txt
echo "sendgrid==6.11.0" >> requirements.txt
pip install -r requirements.txt
```

### 6. Restart Docker

```bash
docker-compose down
docker-compose up -d
```

## Testing

```bash
# Test email sending
docker exec ragproject-app-1 python -c "
from app.tools.unified_email_service import unified_email_service

result = unified_email_service.send_dispute_decision(
    to_email='sk.mohammadshafi1@gmail.com',
    dispute_id='SENDGRID-TEST-001',
    customer_name='Shaik Shafi',
    decision='accept',
    reasoning='Testing SendGrid email delivery',
    amount=1000.00,
    currency='INR'
)

print(result)
"
```

## How It Works

The system now uses a **unified email service** that:

1. **Tries SendGrid first** (if configured)
2. **Falls back to Gmail SMTP** (if SendGrid fails)
3. **Logs which provider was used**

This ensures maximum reliability!

## Troubleshooting

### SendGrid emails not sending?

1. Check API key is correct in `.env`
2. Verify sender identity in SendGrid dashboard
3. Check SendGrid activity log: https://app.sendgrid.com/email_activity

### Still using Gmail?

- If SendGrid isn't configured, system automatically uses Gmail SMTP
- Check logs to see which provider is being used

## Free Tier Limits

- **SendGrid Free**: 100 emails/day
- **Gmail SMTP**: ~500 emails/day (but less reliable)

For production, consider upgrading SendGrid or using AWS SES.

---

**Recommendation**: Use SendGrid for production deployments. It's more reliable and professional.
