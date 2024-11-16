import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
import pandas as pd
import numpy as np
import ta

# Function to analyze stock with Bollinger Bands and RSI for buy/sell signals
def analyze_stock(ticker, risk_multiplier):  
    # Download historical data
    df = yf.download(ticker, start='2019-01-01')
    
    # Calculate Bollinger Bands and RSI
    df['ma_20'] = df['Close'].rolling(20).mean()
    df['vol'] = df['Close'].rolling(20).std()
    df['upper_bb'] = df['ma_20'] + (2 * df['vol'])
    df['lower_bb'] = df['ma_20'] - (2 * df['vol'])
    df['rsi'] = ta.momentum.rsi(df['Close'], window=6)
    df.dropna(inplace=True)

    # Define buy/sell conditions based on RSI and Bollinger Bands
    conditions = [
        (df['rsi'] < 30) & (df['Close'] < df['lower_bb']),
        (df['rsi'] > 70) & (df['Close'] > df['upper_bb'])
    ]
    choices = ['Buy', 'Sell']
    df['signal'] = np.select(conditions, choices)
    df['signal'] = df['signal'].shift(1)

    # Initialize lists for transaction data
    position = False
    buy_dates, sell_dates = [], []
    buy_prices, sell_prices = [], []

    # Loop to find buy and sell dates and prices based on signals
    for index, row in df.iterrows():
        # Buy condition every 5 days if not already in a position
        if not position and row['signal'] == 'Buy':
            buy_dates.append(index)
            buy_prices.append(row['Open'])
            position = True
        # Check if 5 days have passed for selling
        elif position:
            previous_close = df['Close'].shift(1).loc[index]
            if (index - buy_dates[-1]).days >= 5:  # Buy every 5 days
                sell_dates.append(index)
                sell_prices.append(row['Open'])
                position = False
            elif row['signal'] == 'Sell' or (previous_close < risk_multiplier * buy_prices[-1]):
                sell_dates.append(index)
                sell_prices.append(row['Open'])
                position = False

    # Ensure buy and sell lists are of the same length
    if len(buy_dates) > len(sell_dates):
        sell_dates.append(None)
        sell_prices.append(None)
    elif len(sell_dates) > len(buy_dates):
        buy_dates.append(None)
        buy_prices.append(None)

    # Create DataFrame for transaction details
    transactions = pd.DataFrame({
        'Buy Date': buy_dates,
        'Buy Price': buy_prices,
        'Sell Date': sell_dates,
        'Sell Price': sell_prices
    })

    # Calculate returns
    transactions['Return (%)'] = ((transactions['Sell Price'] - transactions['Buy Price']) / transactions['Buy Price']) * 100

    # Calculate total profit and percent return
    total_profit = transactions['Sell Price'].sum() - transactions['Buy Price'].sum()
    total_return_percent = (total_profit / transactions['Buy Price'].sum()) * 100 if transactions['Buy Price'].sum() > 0 else 0

    # Print results
    print(f"\nResults for {ticker} with risk level ({risk_multiplier * 100}% of buy price):")
    print(transactions)
    print(f"Total Profit: ${total_profit:.2f}")
    print(f"Total Return: {total_return_percent:.2f}%")

    # Plotting with Matplotlib
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot closing prices
    ax.plot(df.index, df['Close'], label='Close Price', color='blue', linewidth=1)
    ax.plot(df['ma_20'], label='20-day MA', color='orange', linewidth=1)

    # Plot Bollinger Bands
    ax.fill_between(df.index, df['lower_bb'], df['upper_bb'], color='lightgray', alpha=0.5, label='Bollinger Bands')

    # Plot buy signals
    if buy_dates and buy_prices:
        ax.scatter(buy_dates, buy_prices, marker='^', color='green', s=100, label='Buy Signal', zorder=5)

    # Plot sell signals
    if sell_dates and sell_prices:
        ax.scatter(sell_dates, sell_prices, marker='v', color='red', s=100, label='Sell Signal', zorder=5)

    # Annotate total profit on the chart
    ax.annotate(f'Total Profit: ${total_profit:.2f}\nTotal Return: {total_return_percent:.2f}%',
                xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12, bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white'))

    ax.set_title(f"{ticker} Price and Buy/Sell Signals")
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{ticker}_chart.png")  # Save the plot to the current working directory
    plt.close(fig)  # Close the plot to avoid displaying it

# List of tickers to analyze
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NFLX", "PEP", "PG", "JPM", "BAC", "GS", "JNJ", "PFE", "MRK", "XOM", "CVX", "DUK", "NEE"]

# Define risk multipliers for different risk levels
risk_levels = {
    "Low Risk": 0.95,   # Sell if price falls below 95% of buy price
    "Medium Risk": 0.85,  # Sell if price falls below 85% of buy price
    "High Risk": 0.70   # Sell if price falls below 70% of buy price
}

# Loop through each ticker and risk level
for ticker in tickers:
    for risk_name, risk_multiplier in risk_levels.items():
        print(f"\nAnalyzing {ticker} with {risk_name} ({risk_multiplier * 100}% of buy price)...")
        analyze_stock(ticker, risk_multiplier)