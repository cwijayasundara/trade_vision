# filename: tesla_stock_plot.py
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

# Define the stock symbol and time period
stock_symbol = 'TSLA'
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=4*365)  # 4 years

# Fetch the stock data
tesla_data = yf.download(stock_symbol, start=start_date, end=end_date)

# Plotting the stock price data
plt.figure(figsize=(14, 7))
plt.plot(tesla_data.index, tesla_data['Close'], label='Close Price')
plt.title(f'{stock_symbol} Stock Price Movement for the Past 4 Years')
plt.xlabel('Date')
plt.ylabel('Stock Price in USD')
plt.legend()
plt.grid(True)
plt.show()