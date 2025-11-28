# 📧 Setup Email for sk.mohammadshafi3044@gmail.com

## Quick Setup (2 Minutes)

Your email is already configured in the system! You just need to get the App Password.

---

## Step 1: Get Gmail App Password

### Option A: Direct Link
1. Go to: https://myaccount.google.com/apppasswords
2. Sign in with: **sk.mohammadshafi3044@gmail.com**

### Option B: Manual Navigation
1. Go to: https://myaccount.google.com/
2. Click "Security" on the left
3. Scroll to "2-Step Verification" 
4. If not enabled, enable it first (takes 1 minute)
5. Go back to Security
6. Click "App passwords"

---

## Step 2: Create App Password

1. In App Passwords page:
   - Select app: **Mail**
   - Select device: **Other (Custom name)**
   - Name it: **Dispute System**
2. Click **Generate**
3. You'll see a 16-character password like: `abcd efgh ijkl mnop`
4. **Copy this password** (remove spaces)

---

## Step 3: Update .env File

Open the `.env` file and replace this line:

```bash
SMTP_PASSWORD=your-app-password-here
```

With your actual password (no spaces):

```bash
SMTP_PASSWORD=abcdefghijklmnop
```

**Example:**
```bash
SMTP_EMAIL=sk.mohammadshafi3044@gmail.com
SMTP_PASSWORD=xyzw1234abcd5678
```

---

## Step 4: Restart Docker

```bash
docker-compose restart app
```

Wait 10 seconds, then test!

---

## Step 5: Test Email

1. Open: http://localhost:8000/
2. Fill the form
3. Use **sk.mohammadshafi3044@gmail.com** in the email field
4. Submit
5. Check your Gmail inbox!

---

## 🔍 Troubleshooting

### Can't find App Passwords?
- Make sure 2-Step Verification is enabled first
- Go to: https://myaccount.google.com/security
- Enable "2-Step Verification"
- Then try App Passwords again

### Still not working?
1. Make sure password has NO spaces
2. Check .env file is saved
3. Restart: `docker-compose restart app`
4. Check logs: `docker-compose logs app | grep -i email`

---

## ✅ Once Done

Every dispute will send a real email to:
- **sk.mohammadshafi3044@gmail.com** (or any email users provide)
- Professional HTML format
- Instant delivery
- Free (Gmail SMTP)

---

**Your email is already configured! Just need the App Password!** 🎉
