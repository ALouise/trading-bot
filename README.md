# Intraday Systematic Trading Strategy

This project implements and deploys a systematic intraday trading strategy on a personal portfolio composed of European equities and various ETFs.

## Project Overview

### Backtesting

- Collect intraday price data for all assets in the portfolio
- Backtest several intraday trading strategies on this historical data
- Evaluate each strategy using performance metrics (e.g. return, Sharpe ratio, drawdown)
- Select the best-performing strategy for each ticker

### Live Strategy

- Deploy the selected strategy on live data using real-time price feeds
- Send BUY and SELL signals via Discord
- Plot real-time price evolution with trading signals
- Track the portfolio's cumulative return during the trading day

## Portfolio Composition

- European stocks
- Various thematic and regional ETFs

## To Do

- Build a historical intraday dataset
- Implement and compare multiple trading strategies
- Add evaluation tools to rank and monitor strategies
- Improve signal generation to include suggested order sizes


