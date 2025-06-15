import time
import yfinance as yf
import requests
import pytz
from datetime import datetime, time as dt_time

def simple_signal(prices):
    if len(prices) < 4:
        return None
    if prices[-1] < min(prices[-4:-1]):
        return "SELL"
    if prices[-1] > max(prices[-4:-1]):
        return "BUY"
    return None

def send_discord_message(webhook_url, message):
    try:
        requests.post(webhook_url, json={"content": message})
    except Exception as e:
        print(f"[ERROR] Failed to send Discord message: {e}")

def run_signal_send_discord(ticker, interval, signal_func, webhook_url):
    prices = []
    timestamps = []
    last_signal = None

    paris_tz = pytz.timezone("Europe/Paris")
    #market_close = dt_time(17, 30)  # 17h30

    while True:
        now = datetime.now(paris_tz)
        #if now.time() >= market_close:
        #    print(">>> Market closed — stopping signal engine.")
        #    break

        try:
            p = yf.Ticker(ticker).fast_info['lastPrice']
        except:
            time.sleep(interval)
            continue

        prices.append(p)
        timestamps.append(now)

        if signal_func is not None:
            signal = signal_func(prices)
            if signal in ["BUY", "SELL"] and signal != last_signal:
                message = f"Signal: {signal} | {ticker} at {p:.2f} EUR"
                send_discord_message(webhook_url, message)
                last_signal = signal

        time.sleep(interval)