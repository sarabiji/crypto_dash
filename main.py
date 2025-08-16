# main.py
import requests
import time
from flask import Flask, render_template

app = Flask(__name__)

# --- Caching Configuration ---
# Global variables to store the cached data and the last update time.
# This simple in-memory cache avoids repeated API calls.
cached_data = None
last_updated = 0
CACHE_INTERVAL_SECONDS = 300  # Refresh data every 5 minutes

# --- API Configuration ---
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
API_PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 20,
    "page": 1,
    "sparkline": "false"
}

def get_crypto_data():
    """
    Fetches the top cryptocurrencies from the CoinGecko API.
    Returns a tuple of (data, error_message).
    """
    try:
        response = requests.get(API_URL, params=API_PARAMS, timeout=10)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        # Handle various request-related errors gracefully
        return None, f"Error fetching data from API: {e}. Please check your internet connection or the API status."

@app.route("/")
def home():
    """
    The main route for the dashboard.
    This route implements a caching mechanism.
    """
    global cached_data, last_updated

    # Check if the cache is stale
    if time.time() - last_updated > CACHE_INTERVAL_SECONDS:
        print("Cache is stale. Fetching new data...")
        new_data, error = get_crypto_data()
        
        # Check if new data was successfully fetched
        if new_data:
            cached_data = new_data
            last_updated = time.time()
        # If new data fetch failed but old data exists, serve the old data with a warning
        elif cached_data:
            print(f"Failed to fetch new data. Serving stale data from cache. Error: {error}")
            # We don't need to return a template here, as the code will continue to the render step.
        else:
            # If there's no cached data and the fetch failed, then we must show the error.
            return render_template("index.html", coins=None, error=error)
    else:
        print("Serving data from cache.")

    # Render the HTML template with the cached data
    return render_template("index.html", coins=cached_data, error=None)

if __name__ == "__main__":
    app.run(debug=True)
