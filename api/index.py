"""Vercel serverless function entry point"""
from app.api.main import app

# Vercel expects the app to be named 'app' or exported as handler
handler = app
