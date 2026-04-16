import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# ===== TELEGRAM DETAILS =====
BOT_TOKEN = "8693861675:AAH20sGC3PU_ehueIVTLT73UwwVHTCl4uxQ"
CHAT_ID = "5926424014"

# ===== STOCK LIST =====
stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

# ===== TELEGRAM FUNCTION =====
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.get(url, params={
        "chat_id": CHAT_ID,
        "text": msg
    })
    print("Telegram:", response.text)

print("🚀 BOT RUNNING...")

for symbol in stocks:
    try:
        df = yf.download(symbol, period="1d", interval="5m", progress=False)

        if df is None or df.empty:
            print(f"No data for {symbol}")
            continue

        df = df.reset_index()

        # ===== STOCHASTIC (4,3,3) CORRECT =====
        low_min = df["Low"].rolling(window=4).min()
        high_max = df["High"].rolling(window=4).max()

        raw_k = (df["Close"] - low_min) / (high_max - low_min) * 100

        smooth_k = raw_k.rolling(window=3).mean()   # smooth %K
        smooth_d = smooth_k.rolling(window=3).mean()  # %D

        df["%k"] = smooth_k
        df["%d"] = smooth_d

        # ===== LAST VALUES =====
        last_k = float(df["%k"].iloc[-1])
        last_d = float(df["%d"].iloc[-1])

        print(symbol, round(last_k, 2), round(last_d, 2))

        # ===== TEST CONDITION =====
        if last_k < 70 and last_d < 70:
            msg = f"""🚨 TEST ALERT

Stock: {symbol}
K: {round(last_k,2)}
D: {round(last_d,2)}
Time: {datetime.now().strftime('%H:%M:%S')}
"""
            send(msg)

    except Exception as e:
        print("ERROR:", symbol, e)
