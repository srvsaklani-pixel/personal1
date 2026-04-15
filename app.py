import yfinance as yf
import pandas as pd
import time
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

alerted = set()

print("🚀 BOT STARTED")

while True:
    for symbol in stocks:
        try:
            df = yf.download(symbol, period="1d", interval="5m")

            if df.empty:
                continue

            df = df.reset_index()

            low_min = df["Low"].rolling(4).min()
            high_max = df["High"].rolling(4).max()

            df["%k"] = (df["Close"] - low_min) / (high_max - low_min) * 100
            df["%d"] = df["%k"].rolling(3).mean()
            df["%k"] = df["%k"].rolling(3).mean()

            last_k = df.iloc[-1]["%k"]
            last_d = df.iloc[-1]["%d"]

            print(symbol, last_k, last_d)

            if last_k < 20 and last_d < 20:
                if symbol not in alerted:
                    msg = f"🚨 {symbol}\nK={round(last_k,2)} D={round(last_d,2)}"
                    send_telegram(msg)
                    alerted.add(symbol)
            else:
                if symbol in alerted:
                    alerted.remove(symbol)

        except Exception as e:
            print(e)

    time.sleep(300)
