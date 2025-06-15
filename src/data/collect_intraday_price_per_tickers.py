import yfinance as yf
import pandas as pd
import time
import os
from datetime import datetime
import pandas as pd

def get_tickers_from_positions():
    p = pd.read_csv("data/positions_pea/positions.csv", sep=";", decimal=",")
    m = pd.read_csv("config/ticker_map_yf_to_name.csv")
    d = dict(zip(m["name"].str.strip(), m["ticker"].str.strip()))
    return [d[n.strip().replace('"', '')] for n in p["name"] if n.strip().replace('"', '') in d]

TICKERS = get_tickers_from_positions()
INTERVAL_SECONDS = 120 #every five minutes
RUN_UNTIL_HOUR = 18


def collect_for_day():
    while True:
        now = datetime.now()
        if now.hour >= RUN_UNTIL_HOUR:
            print("End today collect data")
            break

        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")

        for ticker in TICKERS:
            try:
                price = yf.Ticker(ticker).fast_info['lastPrice']
                df = pd.DataFrame([[timestamp, ticker, price]], columns=["timestamp", "ticker", "price"])
                ticker_dir = os.path.join("data", "intraday_history", ticker)
                os.makedirs(ticker_dir, exist_ok=True)
                filepath = os.path.join(ticker_dir, f"{date_str}.csv")
                df.to_csv(filepath, mode='a', index=False, header=not os.path.exists(filepath))
            except Exception as e:
                print(f"Fail for {ticker} : {e}")
        
        time.sleep(INTERVAL_SECONDS)