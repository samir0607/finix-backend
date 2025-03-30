import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def fetch_market_recommendation(symbol):
    """
    Fetch market analyst recommendations for a given stock symbol using Finnhub.
    
    Parameters:
        symbol (str): Stock symbol (e.g., "AAPL").
    
    Returns:
        dict or list: JSON response containing recommendation trends.
    """
    url = "https://finnhub.io/api/v1/stock/recommendation"
    params = {
        "symbol": symbol,
        "token": FINNHUB_API_KEY
    }
    
    response = requests.get(url, params=params)
    
    # Check for successful response
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching recommendation: {response.status_code} - {response.text}")
        return None

def get_latest_recommendation(recommendations):
    """
    Extract the most recent recommendation trend from the list.
    
    Parameters:
        recommendations (list): List of recommendation data, each containing a 'period' key.
    
    Returns:
        dict: The latest recommendation data.
    """
    if not recommendations:
        return None
    try:
        # Convert 'period' string to datetime for sorting.
        latest = max(recommendations, key=lambda rec: datetime.strptime(rec['period'], '%Y-%m-%d'))
        return latest
    except Exception as e:
        print(f"Error processing recommendations: {e}")
        return None

# if __name__ == "__main__":
#     symbol = "AAPL"  # Replace with your desired stock symbol
#     recommendations = fetch_market_recommendation(symbol)
    
#     if recommendations:
#         latest_recommendation = get_latest_recommendation(recommendations)
#         if latest_recommendation:
#             print(f"Latest market analyst recommendation for {symbol}: {latest_recommendation}")
#         else:
#             print("Could not determine the latest recommendation.")
#     else:
#         print("No recommendation data retrieved.")

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_rsi(symbol, interval='daily', time_period=14, series_type='close'):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "RSI",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def get_latest_rsi(rsi_data):
    """
    Process the RSI data to extract the most recent RSI value.
    
    Returns:
        tuple: (latest_date, latest_rsi_value) or None if data is missing.
    """
    try:
        rsi_series = rsi_data.get("Technical Analysis: RSI", {})
        if not rsi_series:
            print("No RSI data found.")
            return None
        
        # Parse the dates and find the latest one
        latest_date = max(rsi_series.keys(), key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
        latest_rsi_value = rsi_series[latest_date]["RSI"]
        return latest_date, latest_rsi_value
    except Exception as e:
        print("Error processing RSI data:", e)
        return None

# if __name__ == "__main__":
#     symbol = "AAPL"  # Replace with your desired symbol
#     rsi_data = get_rsi(symbol)
#     latest = get_latest_rsi(rsi_data)
    
#     if latest:
#         date, rsi_value = latest
#         print(f"Latest RSI for {symbol} on {date} is {rsi_value}")
#     else:
#         print("Failed to retrieve the latest RSI data.")


def generate_stock_data(symbol):

    res = ""

    rsi_data = get_rsi(symbol)
    latest = get_latest_rsi(rsi_data)
    date, rsi_value = latest
    res += f"Latest RSI for {symbol} on {date} is {rsi_value}\n"

    recommendations = fetch_market_recommendation(symbol)
    latest_recommendation = get_latest_recommendation(recommendations)

    res += f"Latest market analyst recommendation for {symbol}: {latest_recommendation}\n"

    return res