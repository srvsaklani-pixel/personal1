import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# ===== TELEGRAM DETAILS =====
BOT_TOKEN = "8693861675:AAH20sGC3PU_ehueIVTLT73UwwVHTCl4uxQ"
CHAT_ID = "5926424014"

# ===== STOCK LIST =====
stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

# ===== SEND TELEGRAM MESSAGE =====
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

print("🚀 BOT RUNNING...")

for symbol in stocks:
    try:
        # ===== FETCH DATA =====
        df = yf.download(symbol, period="1d", interval="5m", progress=False)

        if df is None or df.empty:
            print(f"No data for {symbol}")
            continue

        df = df.reset_index()

        # ===== STOCHASTIC (4,3,3) =====
        low_min = df["Low"].rolling(4).min()
        high_max = df["High"].rolling(4).max()

        df["%k"] = (df["Close"] - low_min) / (high_max - low_min) * 100
        df["%d"] = df["%k"].rolling(3).mean()
        df["%k"] = df["%k"].rolling(3).mean()

        # ===== GET LAST VALUES (FIXED) =====
        last_k = float(df["%k"].iloc[-1])
        last_d = float(df["%d"].iloc[-1])

        print(symbol, round(last_k, 2), round(last_d, 2))

        # ===== ALERT CONDITION =====
        if last_k < 20 and last_d < 20:
            msg = f"""🚨 STOCHASTIC ALERT

Stock: {symbol}
K: {round(last_k,2)}
D: {round(last_d,2)}
Time: {datetime.now().strftime('%H:%M:%S')}
"""
            send(msg)

    except Exception as e:
        print("ERROR:", symbol, e)
