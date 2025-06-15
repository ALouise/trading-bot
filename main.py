from src.data.collect_intraday_price_per_tickers import collect_for_day, get_tickers_from_positions
from src.signal.signals_live import run_signal_send_discord, simple_signal
from config.discord import DISCORD_WEBHOOK


# every day: load positions file on boursobank web => EXECUTE this file, initialise TICKERS list, 
# and collect intraday price per tickers => objective: load data to backtest the intraday strat

STRATEGY = simple_signal  # choose here the buy/sell strat
unique_ticker = 'BTC-USD' #first step: strat on only one ticker

if __name__ == "__main__":
    print(">>> Collecting tickers and intraday data...")
    #get_tickers_from_positions()
    #collect_for_day()

    print(">>> Running live strategy and sending signals to Discord...")
    run_signal_send_discord(
        ticker=unique_ticker,
        interval=10,  # in seconds
        signal_func= STRATEGY,
        webhook_url= DISCORD_WEBHOOK
    )