from flask import Flask, render_template
import requests, time

app = Flask(__name__)

# Simple in-memory cache
last_data = None
last_fetch = 0
CACHE_SECONDS = 60  # refresh every minute

def fetch_data_from_api():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10,  # keep it small for free tier
            "page": 1,
            "sparkline": "false"
        }
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        # Check for rate-limit or error message
        if isinstance(data, dict) and "status" in data:
            return None, data["status"]["error_message"]

        return data, None
    except Exception as e:
        return None, str(e)

@app.route("/")
def index():
    global last_data, last_fetch

    # Use cache unless stale
    if time.time() - last_fetch > CACHE_SECONDS or last_data is None:
        last_data, error_message = fetch_data_from_api()
        last_fetch = time.time()
    else:
        error_message = None

    return render_template("index.html", coins=last_data or [], error=error_message)

if __name__ == "__main__":
    app.run(debug=True)
