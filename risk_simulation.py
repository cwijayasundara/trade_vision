""" download NVDA historical data from Yahoo Finance """
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt


def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


def refresh_data(ticker):
    today = pd.Timestamp.today().date()
    start_date = '2010-01-01'
    df = download_data(ticker, start_date=start_date, end_date=today)
    df.to_csv('stock_data/' + ticker.lower() + '.csv')


def construct_simulation(ticker, initial_investment, num_simulations, forecast_days, desired_return):

    refresh_data(ticker)

    """ upload data from data/nvda.csv  to a pandas dataframe """

    df = pd.read_csv('stock_data/' + ticker.lower() + '.csv')

    daily_returns = df["Adj Close"].pct_change().dropna()

    # Simulation parameters
    num_simulations = num_simulations
    forecast_days = forecast_days

    # Initialise simulation array, all zeros
    simulations = np.zeros((num_simulations, forecast_days))

    # Simulate future paths
    last_price = df["Adj Close"].iloc[-1]
    for i in range(num_simulations):
        cumulative_returns = np.random.choice(daily_returns, size=forecast_days, replace=True).cumsum()
        simulations[i, :] = last_price * (1 + cumulative_returns)

    # part 2

    # Calculate daily returns
    daily_returns = df["Adj Close"].pct_change().dropna()

    # Simulation parameters
    initial_investment = initial_investment  # Initial investment amount
    num_simulations = num_simulations  # Number of simulations
    forecast_days = forecast_days  # Investment horizon in days
    desired_return = desired_return  # Desired return (10%)

    # Calculate the average daily return
    average_daily_return = daily_returns.mean()

    # Calculate volatility as the standard deviation of daily returns
    volatility = daily_returns.std()

    print(f"Average Daily Return: {average_daily_return}")
    print(f"Volatility: {volatility}")

    daily_returns = np.log(df["Adj Close"] / df["Adj Close"].shift(1)).dropna()

    # Simulating future returns
    simulated_end_returns = np.zeros(num_simulations)
    for i in range(num_simulations):
        random_returns = np.random.normal(average_daily_return, volatility, forecast_days)
        cumulative_return = np.prod(1 + random_returns)
        simulated_end_returns[i] = initial_investment * cumulative_return

    # Calculate the final investment values
    final_investment_values = simulated_end_returns

    print("final_investment_values", final_investment_values)

    confidence_level = 0.95
    sorted_returns = np.sort(final_investment_values)
    index_at_var = int((1 - confidence_level) * num_simulations)
    var = initial_investment - sorted_returns[index_at_var]
    conditional_var = initial_investment - sorted_returns[:index_at_var].mean()

    print(f"Value at Risk (95% confidence): £{var:,.2f}")
    print(f"Expected Tail Loss (Conditional VaR): £{conditional_var:,.2f}")

    num_success = np.sum(final_investment_values >= initial_investment * (1 + desired_return))
    probability_of_success = num_success / num_simulations

    # print(f"Probability of achieving at least a {desired_return * 100}% return: {probability_of_success * 100:.2f}%")

    plt.figure(figsize=(10, 6))
    plt.hist(final_investment_values, bins=100, alpha=0.75)
    plt.axvline(
        initial_investment * (1 + desired_return),
        color="r",
        linestyle="dashed",
        linewidth=2,
    )
    plt.axvline(initial_investment - var, color="g", linestyle="dashed", linewidth=2)
    plt.title("Distribution of Final Investment Values")
    plt.xlabel("Final Investment Value")
    plt.ylabel("Frequency")
    plt.show()
    plt.savefig('risk_simulation.png')
    return var, conditional_var, probability_of_success


# construct_simulation('NVDA')
