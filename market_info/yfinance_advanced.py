import yfinance as yf
import pandas as pd


def print_professional_recommendations(ticker_symbol, recent_n=180):
    # Fetch the recommendations
    ticker = yf.Ticker(ticker_symbol)
    recommendations = ticker.recommendations

    if recommendations is not None and not recommendations.empty:
        # Sort the recommendations by date in descending order to get the most recent ones
        recommendations = recommendations.sort_index(ascending=False)

        # Optionally, filter to show only the most recent N recommendations
        if recent_n > 0:
            recommendations = recommendations.head(recent_n)

        # Ensure we only try to display columns that exist. Adjust as necessary.
        expected_columns = ['Firm', 'To Grade', 'Action']
        actual_columns = [col for col in expected_columns if col in recommendations.columns]

        # Print the recommendations in a professional manner
        print(f"Latest {recent_n} Analyst Recommendations for {ticker_symbol}:\n")
        print(recommendations[actual_columns].to_string(index=True))  # Index is the date
    else:
        print(f"No recommendations data available for {ticker_symbol}.")


# Example usage
ticker_symbol = "AAPL"  # Example: Apple Inc.
print_professional_recommendations(ticker_symbol)
