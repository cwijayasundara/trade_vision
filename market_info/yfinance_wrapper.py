import yfinance as yf


def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    return stock.info


def get_income_statement(ticker):
    stock = yf.Ticker(ticker)
    return stock.income_stmt


def show_news(ticker):
    stock = yf.Ticker(ticker)
    return stock.news


def show_recommendations(ticker):
    stock = yf.Ticker(ticker)
    return stock.recommendations


# recommendations = show_recommendations("TSLA")
# print(recommendations)