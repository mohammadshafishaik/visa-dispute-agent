#!/bin/bash

echo "=========================================="
echo "📧 Email Setup for Dispute System"
echo "=========================================="
echo ""

echo "To enable real email notifications, you need:"
echo "1. A Gmail account"
echo "2. Gmail App Password (not your regular password)"
echo ""

echo "Quick Steps:"
echo "1. Go to: https://myaccount.google.com/apppasswords"
echo "2. Enable 2-Factor Authentication if not already enabled"
echo "3. Create an App Password for 'Mail'"
echo "4. Copy the 16-character password"
echo ""

read -p "Do you have your Gmail App Password ready? (y/n): " ready

if [ "$ready" != "y" ]; then
    echo ""
    echo "Please get your App Password first, then run this script again."
    echo "Guide: EMAIL_SETUP_GUIDE.md"
    exit 0
fi

echo ""
read -p "Enter your Gmail address: " email
read -p "Enter your App Password (16 characters, no spaces): " password

echo ""
echo "Updating .env file..."

# Update .env file
sed -i.bak "s/SMTP_EMAIL=.*/SMTP_EMAIL=$email/" .env
sed -i.bak "s/SMTP_PASSWORD=.*/SMTP_PASSWORD=$password/" .env

echo "✅ .env file updated!"
echo ""
echo "Restarting Docker container..."
docker-compose restart app

echo ""
echo "=========================================="
echo "✅ Email Setup Complete!"
echo "=========================================="
echo ""
echo "Test it now:"
echo "1. Open http://localhost:8000/"
echo "2. Fill the form with a real email"
echo "3. Submit and check your inbox!"
echo ""
echo "Note: First email might go to spam folder"
echo "=========================================="
