# 📧 Quick Email Setup (2 Minutes)

## Why No Emails?

Your system is working, but emails need Gmail SMTP configuration!

---

## Option 1: Quick Setup Script (Easiest)

```bash
chmod +x setup_email.sh
./setup_email.sh
```

Follow the prompts!

---

## Option 2: Manual Setup

### Step 1: Get Gmail App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in to your Gmail
3. If you see "2-Step Verification is not turned on":
   - Click "2-Step Verification"
   - Follow steps to enable it
   - Come back to App Passwords
4. Select "Mail" and "Other (Custom name)"
5. Name it "Dispute System"
6. Click "Generate"
7. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

### Step 2: Update .env File

Open `.env` and replace these lines:

```bash
SMTP_EMAIL=your-actual-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
```

**Remove all spaces from the password!**

### Step 3: Restart

```bash
docker-compose restart app
```

### Step 4: Test

1. Open http://localhost:8000/
2. Fill form with YOUR real email
3. Submit
4. Check your inbox (and spam folder)!

---

## Current Status

Right now, emails are being **logged to console** instead of sent.

To see what emails would be sent:
```bash
docker-compose logs -f app | grep "EMAIL"
```

---

## Troubleshooting

### "App Passwords" option not showing?
- You need to enable 2-Factor Authentication first
- Go to: https://myaccount.google.com/security
- Enable "2-Step Verification"

### Still not working?
1. Make sure password has NO spaces
2. Use App Password, NOT your Gmail password
3. Check logs: `docker-compose logs app | grep -i email`
4. Restart: `docker-compose restart app`

---

## Alternative: Use Mailtrap (Testing)

For testing without real emails:

1. Sign up at https://mailtrap.io (free)
2. Get SMTP credentials
3. Update .env:
   ```bash
   SMTP_EMAIL=your-mailtrap-username
   SMTP_PASSWORD=your-mailtrap-password
   ```
4. Update `app/tools/email_service.py`:
   ```python
   self.smtp_server = "smtp.mailtrap.io"
   self.smtp_port = 2525
   ```

---

## ✅ Once Configured

Emails will be sent automatically to users with:
- Professional HTML formatting
- Dispute details
- Decision and reasoning
- Instant delivery

---

**Need help? Check EMAIL_SETUP_GUIDE.md for detailed instructions!**
