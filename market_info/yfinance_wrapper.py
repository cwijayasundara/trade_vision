import yfinance as yf
import pandas as pd
import datetime
import streamlit as st


@st.cache_data
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    # Select relevant information
    name = info.get('longName', 'N/A')
    symbol = info.get('symbol', 'N/A')
    sector = info.get('sector', 'N/A')
    industry = info.get('industry', 'N/A')
    market_cap = info.get('marketCap', 'N/A')
    current_price = info.get('currentPrice', 'N/A')
    fifty_two_week_high = info.get('fiftyTwoWeekHigh', 'N/A')
    fifty_two_week_low = info.get('fiftyTwoWeekLow', 'N/A')
    dividend_yield = info.get('dividendYield', 'N/A') * 100 if info.get('dividendYield') else 'N/A'
    pe_ratio = info.get('trailingPE', 'N/A')
    eps = info.get('trailingEps', 'N/A')
    beta = info.get('beta', 'N/A')
    volume = info.get('volume', 'N/A')

    # Format the information into a summary string
    summary = (f"Summary for {name} ({symbol}):\n"
               f"- Sector: {sector}\n- Industry: {industry}\n- Market Cap: {market_cap}\n"
               f"- Current Price: ${current_price}\n- 52 Week High: ${fifty_two_week_high}\n"
               f"- 52 Week Low: ${fifty_two_week_low}\n- Dividend Yield: {dividend_yield}%\n"
               f"- P/E Ratio: {pe_ratio}\n- EPS: {eps}\n- Beta: {beta}\n- Volume: {volume}")
    return summary


@st.cache_data
def get_income_statement(ticker):
    stock = yf.Ticker(ticker)
    income_stmt = stock.income_stmt
    income_stmt_transposed = income_stmt.transpose()
    formatted_income_stmt = income_stmt_transposed.applymap(lambda x: f"{x / 1e6:.2f}M" if pd.notnull(x) else "N/A")
    pd.set_option('display.max_columns', None)
    return formatted_income_stmt


@st.cache_data
def show_news(ticker):
    stock = yf.Ticker(ticker)
    news_items = stock.news
    formatted_news = []
    for item in news_items:
        title = item.get('title')
        summary = item.get('summary')
        link = item.get('link')
        publisher = item.get('publisher')
        date = item.get('providerPublishTime')
        date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
        formatted_news.append(
            f"Title: {title}\nSummary: {summary}\nPublisher: {publisher}\nDate: {date}\nLink: {link}\n")
    return "\n".join(formatted_news)


@st.cache_data
def show_recommendations(ticker):
    stock = yf.Ticker(ticker)
    return stock.recommendations


@st.cache_data
def extract_future_outlook(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    future_outlook = {
        'Earnings Growth': info.get('earningsGrowth', 'N/A'),
        'Forward P/E': info.get('forwardPE', 'N/A'),
        'PEG Ratio': info.get('pegRatio', 'N/A'),
        'Analyst Recommendations': ticker.recommendations.tail() if ticker.recommendations is not None else 'N/A',
        'Target Mean Price': info.get('targetMeanPrice', 'N/A'),
    }

    """ Format the information into a summary string """
    summary = (f"Future Outlook for {info.get('longName', 'N/A')} ({info.get('symbol', 'N/A')}):\n"
               f"- Earnings Growth: {future_outlook['Earnings Growth']}\n"
               f"- Forward P/E: {future_outlook['Forward P/E']}\n"
               f"- PEG Ratio: {future_outlook['PEG Ratio']}\n"
               f"- Target Mean Price: {future_outlook['Target Mean Price']}")
    return summary
