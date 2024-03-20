# filename: plot_tesla_stock.py
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

# Calculate the date one week ago from today
one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)

# Fetch Tesla's stock data for the last week
data = yf.download("TSLA", start=one_week_ago.strftime('%Y-%m-%d'), end=datetime.datetime.now().strftime('%Y-%m-%d'))

# Plotting the closing prices
plt.figure(figsize=(10, 6))
plt.plot(data.index, data['Close'], marker='o', linestyle='-', color='b')
plt.title('Tesla Stock Price Movement for the Last Week')
plt.xlabel('Date')
plt.ylabel('Closing Price ($)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to not cut off labels
plt.show()
