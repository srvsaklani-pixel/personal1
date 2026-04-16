import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# ===== TELEGRAM DETAILS =====
BOT_TOKEN = "8693861675:AAH20sGC3PU_ehueIVTLT73UwwVHTCl4uxQ"
CHAT_ID = "5067510130"

# ===== STOCK LIST =====
stocks = ["RELIANCE.NS"]

# ===== TELEGRAM FUNCTION =====
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.get(url, params={
        "chat_id": CHAT_ID,
        "text": msg
    })
    print("Telegram:", response.text)

print("🚀 BOT RUNNING (DAILY)...")

for symbol in stocks:
    try:
        # ===== DAILY DATA =====
        df = yf.download(symbol, period="6mo", interval="1d", progress=False)

        if df is None or df.empty:
            print(f"No data for {symbol}")
            continue

        df = df.reset_index()

        # ===== STOCHASTIC (4,3,3) =====
        low_min = df['Low'].rolling(window=4).min()
        high_max = df['High'].rolling(window=4).max()

        df['raw_k'] = ((df['Close'] - low_min) / (high_max - low_min)) * 100

        df['k'] = df['raw_k'].rolling(window=3).mean()
        df['d'] = df['k'].rolling(window=3).mean()

        # Remove NaN
        df = df.dropna()

        # ===== LAST VALUES =====
        last_k = float(df['k'].iloc[-1])
        last_d = float(df['d'].iloc[-1])

        print(symbol, round(last_k, 2), round(last_d, 2))

        # ===== ALERT CONDITION =====
        if last_k < 20 and last_d < 20:
            msg = f"""🚨 DAILY STOCHASTIC ALERT

Stock: {symbol}
K: {round(last_k,2)}
D: {round(last_d,2)}
Date: {df['Date'].iloc[-1].strftime('%Y-%m-%d')}
"""
            send(msg)

    except Exception as e:
        print("ERROR:", symbol, e)
