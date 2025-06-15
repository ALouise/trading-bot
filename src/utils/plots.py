import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import yfinance as yf
from IPython.display import clear_output
import time
from datetime import datetime


def run_live_plot(ticker='MC.PA', interval=10, duration_minutes=5, signal_func=None):
    prices = []
    timestamps = []
    signals = []

    start_time = time.time()

    while True:
        now = datetime.now()
        try:
            p = yf.Ticker(ticker).fast_info['lastPrice']
        except:
            continue

        prices.append(p)
        timestamps.append(now)

        if signal_func is not None:
            signal = signal_func(prices)
            if signal in ["BUY", "SELL"]:
                signals.append((now, p, signal))

        clear_output(wait=True)
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, prices, label="Price")

        for t, price, s in signals:
            color = 'green' if s == "BUY" else 'red'
            plt.scatter(t, price, color=color, s=50, label=s)

        plt.title(f"{ticker} - Live Price")
        plt.xlabel("Time")
        plt.ylabel("Price (€)")
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.show()

        if time.time() - start_time > duration_minutes * 60:
            break

        time.sleep(interval)

def plot_signals_alternatives_buy_sell(df, ticker=""):
    fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    axs[0].plot(df["timestamp"], df["price"], label="Price", linewidth=1.5)
    buys = df[df["signal"] == "BUY"]
    sells = df[df["signal"] == "SELL"]
    axs[0].scatter(buys["timestamp"], buys["price"], color="green", label="BUY", s=40)
    axs[0].scatter(sells["timestamp"], sells["price"], color="red", label="SELL", s=40)
    axs[0].set_title(f"{ticker} - Price with Signals")
    axs[0].set_ylabel("Price (€)")
    axs[0].legend()
    axs[0].grid(True)

    position = None
    entry_price = None
    returns = []

    for i, row in df.iterrows():
        signal = row["signal"]
        price = row["price"]

        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = price
        elif signal == "SELL" and position == "LONG":
            ret = price - entry_price
            returns.append(ret)
            position = None
            entry_price = None
        elif signal == "SELL" and position is None:
            position = "SHORT"
            entry_price = price
        elif signal == "BUY" and position == "SHORT":
            ret = entry_price - price
            returns.append(ret)
            position = None
            entry_price = None
        else:
            returns.append(0)

    while len(returns) < len(df):
        returns.append(0)

    df["cum_return"] = np.cumsum(returns)
    axs[1].plot(df["timestamp"], df["cum_return"], label="Cumulative Return", color="purple")
    axs[1].set_ylabel("PnL (€)")
    axs[1].set_title("Cumulative Return")
    axs[1].grid(True)

    spread_starts = []
    spread_durations = []
    spreads = []
    colors = []

    entry_price = None
    entry_time = None
    last_signal = None

    for i, row in df.iterrows():
        signal = row["signal"]
        price = row["price"]
        time = row["timestamp"]

        if signal in ["BUY", "SELL"]:
            if last_signal and last_signal != signal:
                if signal == "SELL" and last_signal == "BUY":
                    spread = price - entry_price
                elif signal == "BUY" and last_signal == "SELL":
                    spread = entry_price - price
                else:
                    spread = 0

                spread_starts.append(entry_time)
                spread_durations.append(time - entry_time)
                spreads.append(spread)
                colors.append("green" if spread > 0 else "red")

                entry_price = None
                entry_time = None
                last_signal = None
            else:
                entry_price = price
                entry_time = time
                last_signal = signal

    start_nums = mdates.date2num(spread_starts)
    widths = [d.total_seconds() / 86400 for d in spread_durations]  # matplotlib uses days

    axs[2].barh(
        y=range(len(spreads)),
        width=widths,
        left=start_nums,
        height=[abs(s) for s in spreads],
        color=colors,
        edgecolor="black"
    )

    axs[2].xaxis_date()
    axs[2].set_title("Trade Spreads (width = duration)")
    axs[2].set_xlabel("Time")
    axs[2].set_ylabel("Spread (€)")
    axs[2].grid(True)

def plot_signals(df, ticker=""):
    fig, axs = plt.subplots(2, 1, figsize=(12,5), sharex=True)

    axs[0].plot(df["timestamp"], df["price"], label="Price", linewidth=1.5)
    buys = df[df["signal"] == "BUY"]
    sells = df[df["signal"] == "SELL"]
    axs[0].scatter(buys["timestamp"], buys["price"], color="green", label="BUY", s=40)
    axs[0].scatter(sells["timestamp"], sells["price"], color="red", label="SELL", s=40)
    axs[0].set_title(f"{ticker} - Price with Signals")
    axs[0].set_ylabel("Price (€)")
    axs[0].legend()
    axs[0].grid(True)

    position = None
    entry_price = None
    returns = []

    for i, row in df.iterrows():
        signal = row["signal"]
        price = row["price"]

        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = price
        elif signal == "SELL" and position == "LONG":
            ret = price - entry_price
            returns.append(ret)
            position = None
            entry_price = None
        elif signal == "SELL" and position is None:
            position = "SHORT"
            entry_price = price
        elif signal == "BUY" and position == "SHORT":
            ret = entry_price - price
            returns.append(ret)
            position = None
            entry_price = None
        else:
            returns.append(0)

    while len(returns) < len(df):
        returns.append(0)

    df["cum_return"] = np.cumsum(returns)
    axs[1].plot(df["timestamp"], df["cum_return"], label="Cumulative Return", color="purple")
    axs[1].set_ylabel("PnL (€)")
    axs[1].set_title("Cumulative Return")
    axs[1].grid(True)


    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()