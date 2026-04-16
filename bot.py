import yfinance as yf
import pandas as pd
import requests
import os
from datetime import datetime

BOT_TOKEN = os.getenv("8684314803:AAHiUYBClepHX8gptTX4Vu52Y_1bJ0-Ctxs")
CHAT_ID = os.getenv("5926424014")

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

for symbol in stocks:
    try:
        df = yf.download(symbol, period="1d", interval="5m", progress=False)

        if df is None or df.empty:
            print(f"No data for {symbol}")
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

        # ✅ TEMP TEST (always send alert)
        if True:
            msg = f"TEST ALERT\n{symbol}\nK={round(last_k,2)} D={round(last_d,2)}"
            send(msg)

    except Exception as e:
        print("ERROR:", symbol, e)
