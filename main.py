import requests
import time
from flask import Flask, render_template, request

app = Flask(__name__)

# Cache variables
cache_data = []
cache_timestamp = 0
CACHE_DURATION = 300  # 5 minutes

@app.route("/", methods=["GET", "HEAD"])
def index():
    global cache_data, cache_timestamp

    # Ignore HEAD requests (Render health checks)
    if request.method == "HEAD":
        return "", 200

    now = time.time()

    # Refresh cache if expired
    if not cache_data or (now - cache_timestamp) > CACHE_DURATION:
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

            if isinstance(data, list) and all(isinstance(c, dict) for c in data):
                cache_data = data
                cache_timestamp = now
            else:
                print("CoinGecko returned error:", data)

        except Exception as e:
            print("Error fetching CoinGecko data:", e)

    return render_template(
        "index.html",
        coins=cache_data,
        error_msg=None if cache_data else "⚠ API limit reached — showing no data."
    )

if __name__ == "__main__":
    app.run(debug=True)
