import requests

BOT_TOKEN = "8693861675:AAH20sGC3PU_ehueIVTLT73UwwVHTCl4uxQ"
CHAT_ID = "5926424014"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

send("🚀 TEST MESSAGE - BOT WORKING")
print("Message sent")
