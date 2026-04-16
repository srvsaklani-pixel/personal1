import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# 🔴 DIRECT VALUES (TEMPORARY FIX)
BOT_TOKEN = "8693861675:AAH20sGC3PU_ehueIVTLT73UwwVHTCl4uxQ"
CHAT_ID = "5926424014"

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

for symbol in stocks:
    try:
        df = yf.download(symbol, period="1d", interval="5m", progress=False)

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
            msg = f"""🚨 ALERT

Stock: {symbol}
K: {round(last_k,2)}
D: {round(last_d,2)}
Time: {datetime.now().strftime('%H:%M:%S')}
"""
            send(msg)

    except Exception as e:
        print("ERROR:", symbol, e)
