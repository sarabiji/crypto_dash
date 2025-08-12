import requests
import time
from flask import Flask, render_template, request

app = Flask(__name__)

# Cache variables
cache_data = None
cache_timestamp = 0
CACHE_DURATION = 300  # 5 minutes in seconds

@app.route("/", methods=["GET", "HEAD"])
def index():
    global cache_data, cache_timestamp

    # Ignore HEAD requests from Render health checks
    if request.method == "HEAD":
        return "", 200

    now = time.time()

    # If cache is empty or expired, fetch new data
    if cache_data is None or (now - cache_timestamp) > CACHE_DURATION:
        try:
            response = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets",
                params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": 10,
                    "page": 1,
                    "sparkline": False
                },
                timeout=10
            )
            data = response.json()

            # If API returned an error, keep old cache
            if isinstance(data, list):
                cache_data = data
                cache_timestamp = now
            else:
                print("API error, keeping old cache:", data)

        except Exception as e:
            print("Error fetching CoinGecko data:", e)

    # Render page with cached data (or empty if nothing cached yet)
    return render_template(
        "index.html",
        coins=cache_data if cache_data else [],
        error=None if cache_data else "No data available (API rate limit reached)"
    )

if __name__ == "__main__":
    app.run(debug=True)
