import ssl
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from news_sentiment_analyser import analyse_sentiment_list, analyse_sentiment

ssl._create_default_https_context = ssl._create_unverified_context

finviz_url = 'https://finviz.com/quote.ashx?t='

st.cache_data


def get_news_for_ticker(ticker):
    url = finviz_url + ticker

    request = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(request)

    html = BeautifulSoup(response, features='html.parser')
    news_table = html.find(id='news-table')

    parsed_data = []
    for row in news_table.findAll('tr'):
        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

    news = pd.DataFrame(parsed_data, columns=['symbol', 'date', 'time', 'title'])
    """ return the first 30 news items"""
    news = news.head(30)
    return news


st.cache_data


def analyse_sentiment_df(news_df):
    sentiment_list = []
    for news_item in news_df['title']:
        sentiment = analyse_sentiment(news_item)
        sentiment_list.append(sentiment)
    print("sentiment list is", sentiment_list)
    response = analyse_sentiment_list(sentiment_list)
    return response
