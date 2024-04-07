import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go
import datetime


def predict_stock_price(ticker):
    today = datetime.date.today()

    # Download historical stock data from Yahoo Finance
    stock_data = yf.download(ticker, start='2020-01-01', end=today)

    if not stock_data.empty:
        # Reset the index to get the Date as a column and create a standalone DataFrame
        stock_data.reset_index(inplace=True)

        # Use only Date and Close price for prediction, ensuring it's a copy
        data = stock_data[['Date', 'Close']].copy()

        # Convert dates to ordinal numbers to use as features for the model
        data['Date_ordinal'] = pd.to_datetime(data['Date']).map(pd.Timestamp.toordinal)

        # Splitting the data into features and target, using the ordinal dates for modeling
        X = data['Date_ordinal'].values.reshape(-1, 1)
        y = data['Close'].values

        # Splitting the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Create a model and train it
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Making predictions
        predictions = model.predict(X_test)

        # Prepare X_test dates for plotting
        X_test_dates = [pd.Timestamp.fromordinal(int(ordinal)) for ordinal in X_test.flatten()]

        # Plotting using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=X_test_dates, y=y_test, mode='markers', name='Actual Price'))
        fig.add_trace(go.Scatter(x=X_test_dates, y=predictions, mode='lines', name='Predicted Price'))
        fig.update_layout(title=f'Stock Price Prediction for {ticker} using Linear Regression Model',
                          xaxis_title='Date', yaxis_title='Stock Price')

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Failed to load data. Please check the stock ticker.")
