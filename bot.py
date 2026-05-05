import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz

BOT_TOKEN = "8693861675:AAH20sGC3PU_ehueIVTLT73UwwVHTCl4uxQ"
CHAT_ID = "-1003904590545"

stocks = [
    # Original
    "ICICIBANK.NS", "ICICIPRULI.NS", "INFY.NS", "ITC.NS",
    "KOTAKBANK.NS", "LT.NS", "MARICO.NS", "NESTLEIND.NS",
    "NAM-INDIA.NS", "PAGEIND.NS", "PFIZER.NS", "PIDILITIND.NS",
    "PGHH.NS", "RELIANCE.NS", "SANOFI.NS", "TCS.NS", "TITAN.NS",

    # V40
    "SBIN.NS", "HDFCBANK.NS", "AXISBANK.NS",
    "HCLTECH.NS",
    "HDFCAMC.NS", "HDFCLIFE.NS", "ICICIGI.NS",
    "BAJAJFINSV.NS", "BAJAJHLDNG.NS", "BAJFINANCE.NS",
    "HINDUNILVR.NS", "COLPAL.NS", "DABUR.NS", "GILLETTE.NS",
    "BATAINDIA.NS", "HAVELLS.NS", "VOLTAS.NS",
    "GLAXO.NS", "ABBOTINDIA.NS",
    "ASIANPAINT.NS", "BERGEPAINT.NS",
    "MARUTI.NS", "BAJAJ-AUTO.NS",

    # V40 NEXT
    "CDSL.NS", "BSE.NS",
    "ANGELONE.NS", "IIFL.NS", "MCX.NS",
    "ULTRACEMCO.NS", "ACC.NS",
    "TEAMLEASE.NS", "QUESS.NS",
    "ASTRAZEN.NS", "CIPLA.NS", "ERIS.NS", "LALPATHLAB.NS",
    "APOLLOHOSP.NS", "FORTIS.NS",
    "ADANIPORTS.NS", "JSWINFRA.NS",
    "GODREJCP.NS", "DIXON.NS", "CERA.NS",
    "HONAUT.NS", "RELAXO.NS", "SYMPHONY.NS", "VIPIND.NS",
    "BOSCHLTD.NS", "EICHERMOT.NS",
    "UNITDSPR.NS", "RADICO.NS"
]

# ===== GROUP MAPPING =====
stock_groups = {
    # V40
    "ICICIBANK.NS": "V40", "ICICIPRULI.NS": "V40", "INFY.NS": "V40", "ITC.NS": "V40",
    "KOTAKBANK.NS": "V40", "LT.NS": "V40", "MARICO.NS": "V40", "NESTLEIND.NS": "V40",
    "NAM-INDIA.NS": "V40", "PAGEIND.NS": "V40", "PFIZER.NS": "V40", "PIDILITIND.NS": "V40",
    "PGHH.NS": "V40", "RELIANCE.NS": "V40", "SANOFI.NS": "V40", "TCS.NS": "V40", "TITAN.NS": "V40",
    "SBIN.NS": "V40", "HDFCBANK.NS": "V40", "AXISBANK.NS": "V40",
    "HCLTECH.NS": "V40",
    "HDFCAMC.NS": "V40", "HDFCLIFE.NS": "V40", "ICICIGI.NS": "V40",
    "BAJAJFINSV.NS": "V40", "BAJAJHLDNG.NS": "V40", "BAJFINANCE.NS": "V40",
    "HINDUNILVR.NS": "V40", "COLPAL.NS": "V40", "DABUR.NS": "V40", "GILLETTE.NS": "V40",
    "BATAINDIA.NS": "V40", "HAVELLS.NS": "V40", "VOLTAS.NS": "V40",
    "GLAXO.NS": "V40", "ABBOTINDIA.NS": "V40",
    "ASIANPAINT.NS": "V40", "BERGEPAINT.NS": "V40",
    "MARUTI.NS": "V40", "BAJAJ-AUTO.NS": "V40",

    # V40 NEXT
    "CDSL.NS": "V40 NEXT", "BSE.NS": "V40 NEXT",
    "ANGELONE.NS": "V40 NEXT", "IIFL.NS": "V40 NEXT", "MCX.NS": "V40 NEXT",
    "ULTRACEMCO.NS": "V40 NEXT", "ACC.NS": "V40 NEXT",
    "TEAMLEASE.NS": "V40 NEXT", "QUESS.NS": "V40 NEXT",
    "ASTRAZEN.NS": "V40 NEXT", "CIPLA.NS": "V40 NEXT",
    "ERIS.NS": "V40 NEXT", "LALPATHLAB.NS": "V40 NEXT",
    "APOLLOHOSP.NS": "V40 NEXT", "FORTIS.NS": "V40 NEXT",
    "ADANIPORTS.NS": "V40 NEXT", "JSWINFRA.NS": "V40 NEXT",
    "GODREJCP.NS": "V40 NEXT", "DIXON.NS": "V40 NEXT",
    "CERA.NS": "V40 NEXT", "HONAUT.NS": "V40 NEXT",
    "RELAXO.NS": "V40 NEXT", "SYMPHONY.NS": "V40 NEXT",
    "VIPIND.NS": "V40 NEXT",
    "BOSCHLTD.NS": "V40 NEXT", "EICHERMOT.NS": "V40 NEXT",
    "UNITDSPR.NS": "V40 NEXT", "RADICO.NS": "V40 NEXT"
}

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": msg})

# ===== TIME =====
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

print("🚀 BOT RUNNING AT:", now.strftime("%H:%M IST"))

# ===== ALWAYS SEND HEARTBEAT =====
send(f"✅ Bot checked at {now.strftime('%H:%M IST')}")

# ===== STOCK SCAN =====
for symbol in stocks:
    try:
        group = stock_groups.get(symbol, "UNKNOWN")

        df = yf.download(symbol, period="6mo", interval="1d", progress=False)

        if df is None or df.empty:
            continue

        df = df.reset_index()

        low_min = df['Low'].rolling(4).min()
        high_max = df['High'].rolling(4).max()

        df['raw_k'] = ((df['Close'] - low_min) / (high_max - low_min)) * 100
        df['k'] = df['raw_k'].rolling(3).mean()
        df['d'] = df['k'].rolling(3).mean()

        df = df.dropna()

        last_k = float(df['k'].iloc[-1])
        last_d = float(df['d'].iloc[-1])

        print(symbol, round(last_k, 2), round(last_d, 2))

        if last_k < 20 and last_d < 20:
            msg = f"""🚨 STOCHASTIC ALERT

Stock: {symbol}
Group: {group}
K: {round(last_k,2)}
D: {round(last_d,2)}
Time: {now.strftime('%Y-%m-%d %H:%M IST')}
"""
            send(msg)

    except Exception as e:
        print("ERROR:", symbol, e)
