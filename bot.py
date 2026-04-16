import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz

# ===== TELEGRAM DETAILS =====
BOT_TOKEN = "8693861675:AAH20sGC3PU_ehueIVTLT73UwwVHTCl4uxQ"
CHAT_ID = "5067510130"

# ===== STOCK LIST =====
stocks = [
    "ICICIBANK.NS", "ICICIPRULI.NS", "INFY.NS", "ITC.NS",
    "KOTAKBANK.NS", "LT.NS", "MARICO.NS", "NESTLEIND.NS",
    "NAM-INDIA.NS", "PAGEIND.NS", "PFIZER.NS", "PIDILITIND.NS",
    "PGHH.NS", "RELIANCE.NS", "SANOFI.NS", "TCS.NS", "TITAN.NS"
]

# ===== TELEGRAM FUNCTION =====
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.get(url, params={
        "chat_id": CHAT_ID,
        "text": msg
    })
    print("Telegram:", response.text)

# ===== INDIA TIME =====
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

print("🚀 BOT RUNNING AT:", now.strftime("%H:%M IST"))

# ===== 30-MIN HEARTBEAT =====
if now.minute % 30 == 0:
    send(f"✅ Bot running fine at {now.strftime('%H:%M IST')}")

# ===== STOCK SCANNING =====
for symbol in stocks:
    try:
        df = yf.download(symbol, period="6mo", interval="1d", progress=False)

        if df is None or df.empty:
            print(f"No data for {symbol}")
            continue

        df = df.reset_index()

        # ===== STOCHASTIC (4,3,3) =====
        low_min = df['Low'].rolling(4).min()
        high_max = df['High'].rolling(4).max()

        df['raw_k'] = ((df['Close'] - low_min) / (high_max - low_min)) * 100
        df['k'] = df['raw_k'].rolling(3).mean()
        df['d'] = df['k'].rolling(3).mean()

        df = df.dropna()

        # ===== LAST VALUES =====
        last_k = float(df['k'].iloc[-1])
        last_d = float(df['d'].iloc[-1])

        print(symbol, round(last_k, 2), round(last_d, 2))

        # ===== ALERT CONDITION =====
        if last_k < 20 and last_d < 20:
            msg = f"""🚨 STOCHASTIC ALERT

Stock: {symbol}
K: {round(last_k,2)}
D: {round(last_d,2)}
Time: {now.strftime('%Y-%m-%d %H:%M IST')}
"""
            send(msg)

    except Exception as e:
        print("ERROR:", symbol, e)
