from datetime import date
import yfinance as yf


def draw_stock_price_since_2020(ticker):
    data = yf.download(ticker, start="2020-01-01", end=date.today())
    df = data['Close']
    return df
