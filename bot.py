import os

print("TOKEN:", os.getenv("8693861675:AAH20sGC3PU_ehueIVTLT73UwwVHTCl4uxQ"))
print("CHAT:", os.getenv("5067510130"))

# TEMP TEST
BOT_TOKEN = "PASTE_YOUR_TOKEN_HERE"
CHAT_ID = "PASTE_YOUR_CHAT_ID_HERE"

import requests

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

send("🚀 DIRECT TEST MESSAGE")
