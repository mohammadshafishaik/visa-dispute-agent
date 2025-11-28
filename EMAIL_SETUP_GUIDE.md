# 📧 Email Setup Guide - Free Gmail SMTP

## How to Enable Real Email Notifications

Your system can send real emails to users using Gmail's free SMTP service!

---

## Step 1: Create/Use Gmail Account

You need a Gmail account to send emails. You can use:
- Your existing Gmail account
- Create a new free Gmail account at https://gmail.com

---

## Step 2: Enable 2-Factor Authentication

1. Go to https://myaccount.google.com/security
2. Click on "2-Step Verification"
3. Follow the steps to enable it
4. This is required to create App Passwords

---

## Step 3: Generate App Password

1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" as the app
3. Select "Other" as the device and name it "Dispute System"
4. Click "Generate"
5. **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)

---

## Step 4: Update .env File

Open your `.env` file and update these lines:

```bash
# Replace with your Gmail address
SMTP_EMAIL=your-email@gmail.com

# Replace with the App Password from Step 3 (remove spaces)
SMTP_PASSWORD=abcdefghijklmnop
```

Example:
```bash
SMTP_EMAIL=disputesystem@gmail.com
SMTP_PASSWORD=xyzw1234abcd5678
```

---

## Step 5: Restart the System

```bash
docker-compose restart app
```

---

## Step 6: Test It!

1. Open http://localhost:8000/
2. Fill out the dispute form
3. **Use a real email address** in the Email field
4. Submit the form
5. Check your email inbox!

---

## ✅ What You'll Receive

When a dispute is processed, the user will receive a professional HTML email with:

- Dispute ID
- Decision (Accept/Reject/Review)
- Reasoning
- Amount
- Professional formatting

---

## 🔒 Security Notes

- **App Password is NOT your Gmail password**
- App Password is specific to this application
- You can revoke it anytime from Google Account settings
- Never share your App Password
- The password is stored in `.env` file (not committed to git)

---

## 🆓 Free Tier Limits

Gmail SMTP is completely free with these limits:
- **500 emails per day** (more than enough!)
- No cost
- Reliable delivery
- Professional appearance

---

## 🐛 Troubleshooting

### Email not sending?

1. **Check .env file**
   ```bash
   cat .env | grep SMTP
   ```
   Make sure SMTP_EMAIL and SMTP_PASSWORD are set

2. **Verify App Password**
   - Make sure you used App Password, not regular password
   - Remove any spaces from the password
   - Password should be 16 characters

3. **Check 2FA is enabled**
   - App Passwords only work with 2-Factor Authentication enabled

4. **Restart Docker**
   ```bash
   docker-compose restart app
   ```

5. **Check logs**
   ```bash
   docker-compose logs app | grep -i email
   ```

### Still not working?

The system will show an error message if email fails. Common issues:
- Wrong email/password
- 2FA not enabled
- App Password not generated
- Network/firewall blocking SMTP port 587

---

## 📝 Alternative: Use Your Own SMTP

You can use any SMTP service:

### SendGrid (Free: 100 emails/day)
```bash
SMTP_EMAIL=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

### Mailgun (Free: 100 emails/day)
```bash
SMTP_EMAIL=postmaster@your-domain.mailgun.org
SMTP_PASSWORD=your-mailgun-password
```

### AWS SES (Free: 62,000 emails/month)
Requires AWS account setup

---

## ✨ Benefits of Real Email

- ✅ Users receive instant notifications
- ✅ Professional appearance
- ✅ HTML formatted emails
- ✅ Reliable delivery
- ✅ Free (Gmail SMTP)
- ✅ Easy setup (5 minutes)

---

## 🎉 You're Done!

Once configured, every dispute will automatically send a real email to the user's provided email address!

**Test it now**: http://localhost:8000/
