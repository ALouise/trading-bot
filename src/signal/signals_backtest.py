import pandas as pd

def load_data(filepath):
    df = pd.read_csv(filepath, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

def signals_sma_x(df, x):
    signals = []
    for i in range(len(df)):
        if i < x:
            signals.append(None)
        else:
            avg = df.loc[i-x:i-1, "price"].mean()
            if df.loc[i, "price"] < avg:
                signals.append("SELL")
            elif df.loc[i, "price"] > avg:
                signals.append("BUY")
            else:
                signals.append(None)
    df["signal"] = signals
    return df

def signals_sma_x_filtered(df, x):
    signals = []
    last_signal = None
    for i in range(len(df)):
        if i < x:
            signals.append(None)
            continue
        avg = df.loc[i-x:i-1, "price"].mean()
        price = df.loc[i, "price"]

        if avg < price and last_signal != "BUY":
            signals.append("BUY")
            last_signal = "BUY"
        elif avg > price and last_signal != "SELL":
            signals.append("SELL")
            last_signal = "SELL"
        else:
            signals.append(None)
    df["signal"] = signals
    return df

def signals_sma_x_profit_filtered(df, x):
    signals = []
    last_signal = None
    last_entry_price = None

    for i in range(len(df)):
        if i < x:
            signals.append(None)
            continue

        avg = df.loc[i - x:i - 1, "price"].mean()
        price = df.loc[i, "price"]

        if avg < price:
            if last_signal == "SELL" and last_entry_price and price < last_entry_price:
                signals.append("BUY")
                last_signal = "BUY"
                last_entry_price = price
            elif last_signal != "BUY" and last_signal is None:
                signals.append("BUY")
                last_signal = "BUY"
                last_entry_price = price
            else:
                signals.append(None)

        elif avg > price:
            if last_signal == "BUY" and last_entry_price and price > last_entry_price:
                signals.append("SELL")
                last_signal = "SELL"
                last_entry_price = price
            elif last_signal != "SELL" and last_signal is None:
                signals.append("SELL")
                last_signal = "SELL"
                last_entry_price = price
            else:
                signals.append(None)

        else:
            signals.append(None)

    df["signal"] = signals
    return df