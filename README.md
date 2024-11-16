# Mean Reversion Trading Algorithm: 20-Day Span for Fortune 100 & Emerging Markets

## Overview

This project focuses on the development and implementation of a **mean reversion trading strategy** designed for the **short-term trading of stocks**, with an emphasis on **Fortune 100 companies**. The core strategy operates on a 20-day span, leveraging historical price data to identify opportunities where an asset's price deviates significantly from its moving average, signaling a potential reversion to the mean.

Additionally, the project integrates insights and research from the **University of Brazil**, which explores the successful adaptation of mean reversion strategies in **emerging and lower-market economies**.

### Key Components:

- **Mean Reversion Algorithm**: A robust, rule-based system that identifies when a stock has deviated too far from its historical average over a 20-day period. When the stock price is deemed overbought or oversold relative to its moving average, the bot executes trades to capitalize on the expected reversal.
  
- **Fortune 100 Portfolio**: The bot focuses on trading stocks within the **Fortune 100**, with the goal of capitalizing on short-term price fluctuations based on mean reversion principles. The strategy is designed for both **high liquidity** and **established market performance**.

- **Emerging Market Research Integration**: The strategy is informed by research from the **University of Brazil**, which has shown success in implementing similar mean reversion strategies in **emerging markets** and **lower-income nations**. The research provides valuable insights into adapting the strategy to different market conditions, adding a layer of versatility to the algorithm.

- **Algorithmic Trading Bot**: The trading bot is automated, continuously monitoring and executing trades based on real-time market data and pre-set criteria for mean reversion. It aims to execute high-frequency trades on a short-term basis to capture quick profits from market inefficiencies.

## Features

- **Data-Driven Insights**: The bot uses historical data (at least 20 days of price action) to calculate a moving average and standard deviation to identify **mean reversion signals**.
  
- **Real-Time Execution**: Executes trades automatically when a security's price is expected to revert to its mean, either buying oversold assets or shorting overbought ones.

- **Risk Management**: Built-in risk management protocols including stop-loss thresholds, position sizing, and portfolio diversification to mitigate risk in volatile or adverse market conditions.

- **Scalability**: While designed for Fortune 100 stocks, the strategy has been adapted to emerging markets, leveraging research insights to make the bot versatile across diverse global markets.

## Research Insights

- **University of Brazil Study**: The algorithm incorporates findings from the **University of Brazil**, which demonstrated that mean reversion strategies could be particularly effective in emerging or lower-income markets, where **market inefficiencies** and **price misalignments** are more common due to lower liquidity and differing market dynamics.
  
- **Market Adaptation**: The bot takes into account regional volatility, trading volume, and macroeconomic indicators, allowing it to adjust its strategy for different market conditions.

## Technical Overview

- **Data Source**: The bot pulls historical stock price data from various reliable financial data providers (e.g., Yahoo Finance, Alpha Vantage, etc.) and uses **technical analysis** to identify trading signals based on the **20-day mean reversion** strategy.

- **Platform**: The bot is built in Python and utilizes key libraries such as **pandas**, **numpy**, **matplotlib**, and **TA-Lib** for technical analysis and charting. The trading platform is integrated with APIs such as **Alpaca** or **Interactive Brokers** for real-time execution.

- **Backtesting**: Backtesting modules are included to test the strategy on historical data to validate its effectiveness before going live.

## How It Works

1. **Data Collection**: The bot collects price data for each stock in its focus list (e.g., Fortune 100) or emerging market securities.
   
2. **Signal Generation**: It calculates the **20-day moving average** of each stock, as well as its standard deviation to determine when a stock's price deviates significantly from its mean.

3. **Trade Execution**: If a price is identified as being significantly above or below the mean (e.g., more than two standard deviations), the bot initiates a buy or sell order to capitalize on the anticipated price correction.

4. **Monitoring**: The bot continuously monitors the market, adjusts positions as needed, and ensures risk management rules are followed.

5. **Performance Evaluation**: After each trade, performance metrics are tracked, and the bot’s strategy is tweaked based on ongoing results to optimize returns.
