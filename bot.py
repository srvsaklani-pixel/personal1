import yfinance as yf
import pandas as pd
import requests
import os

BOT_TOKEN = os.getenv("8693861675:AAH20sGC3PU_ehueIVTLT73UwwVHTCl4uxQ")
CHAT_ID = os.getenv("5067510130")

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# ✅ SIMPLE TEST (no loops, no indentation issues)
msg = "🚀 TEST MESSAGE FROM BOT"
send(msg)

print("Message sent")
