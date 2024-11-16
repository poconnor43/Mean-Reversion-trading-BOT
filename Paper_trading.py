import alpaca_trade_api as tradeapi
import pandas as pd
import ta
import time


class LiveTrader:
    def __init__(self, api_key, api_secret, base_url, initial_capital=100000):
        self.api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
        self.capital = initial_capital
        self.position = {}
        self.buy_price = {}
        self.trades = []
        self.history = {}  # To store historical data for each stock

    def get_historical_data(self, ticker):
        # Get historical data for the past 20 minutes (you can adjust this)
        try:
            bars = self.api.get_bars(ticker, '1Min', limit=20).df  # Changed 'minute' to '1Min'
            return bars
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

    def analyze_stock(self, ticker, risk_multiplier):
        # Update historical data
        new_data = self.get_historical_data(ticker)
        if new_data.empty:
            print(f"No data available for {ticker}. Skipping analysis.")
            return  # Skip analysis if no data

        if ticker not in self.history:
            self.history[ticker] = pd.DataFrame()  # Initialize history for new stock

        self.history[ticker] = pd.concat([self.history[ticker], new_data]).drop_duplicates()

        # Calculate Bollinger Bands and RSI using ta
        df = self.history[ticker]
        df['ma_20'] = df['close'].rolling(20).mean()
        df['vol'] = df['close'].rolling(20).std()
        df['upper_bb'] = df['ma_20'] + (2 * df['vol'])
        df['lower_bb'] = df['ma_20'] - (2 * df['vol'])
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()

        # Get the latest close price
        latest_close = df['close'].iloc[-1]

        # Define your buy/sell conditions based on the latest data
        if ticker not in self.position or self.position[ticker] is None:
            if self.should_buy(df, latest_close):
                self.position[ticker] = 'Buy'
                self.buy_price[ticker] = latest_close
                self.trades.append({'Ticker': ticker, 'Type': 'Buy', 'Price': self.buy_price[ticker]})
                self.api.submit_order(
                    symbol=ticker,
                    qty=1,  # Define your quantity
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )

        elif self.position[ticker] == 'Buy':
            if self.should_sell(df, latest_close, risk_multiplier):
                self.position[ticker] = None
                profit = latest_close - self.buy_price[ticker]
                self.capital += profit
                self.trades.append({'Ticker': ticker, 'Type': 'Sell', 'Price': latest_close, 'Profit': profit})
                self.api.submit_order(
                    symbol=ticker,
                    qty=1,  # Define your quantity
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )

    def should_buy(self, df, close_price):
        # Check the latest RSI and Bollinger Bands for buy signal
        latest_rsi = df['rsi'].iloc[-1]
        return latest_rsi < 30 and close_price < df['lower_bb'].iloc[-1]

    def should_sell(self, df, close_price, risk_multiplier):
        # Check the latest RSI and Bollinger Bands for sell signal
        latest_rsi = df['rsi'].iloc[-1]
        return (latest_rsi > 70 and close_price > df['upper_bb'].iloc[-1]) or (close_price < risk_multiplier * self.buy_price[ticker])

    def print_summary(self):
        total_profit = self.capital - 10000  # Assuming initial capital is 10000
        print(f"Total Capital after trades: ${self.capital:.2f}")
        print(f"Total Profit: ${total_profit:.2f}")
        for trade in self.trades:
            print(trade)

    def check_market_status(self):
        clock = self.api.get_clock()  # This method should now work correctly
        if clock.is_open:
            print("The market is open!")
        else:
            print("The market is closed.")


# Example usage
api_key = 'Enter based off alpaca account'
api_secret = 'Enter based off of alpaca account'
base_url = 'https://paper-api.alpaca.markets'  # Corrected base URL for Alpaca paper trading (no extra v2)

# Create an instance of LiveTrader
live_trader = LiveTrader(api_key, api_secret, base_url)

# Define risk multipliers for different stocks
risk_multipliers = {
    "AAPL": 0.95,  # Low risk for Apple
    "MSFT": 0.85,  # Medium risk for Microsoft
    "GOOGL": 0.70  # High risk for Google
}

# Main loop to run the strategy continuously
tickers = list(risk_multipliers.keys())  # Get the list of tickers from risk multipliers

while True:
    live_trader.check_market_status()

    if live_trader.api.get_clock().is_open:
        for ticker in tickers:
            print(f"\nAnalyzing {ticker}...")
            live_trader.analyze_stock(ticker, risk_multipliers[ticker])
    else:
        print("Market is closed, skipping analysis.")
    
    # Wait for a minute before checking again
    time.sleep(60)