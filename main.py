from flask import Flask, render_template
import requests
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def index():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    data = requests.get(url, params=params).json()

    # Log shape and type of each coin
    for i, coin in enumerate(data):
        logging.debug(f"Coin {i} type: {type(coin)}, keys: {list(coin.keys())}")

    return render_template("index.html", coins=data)

if __name__ == "__main__":
    app.run()
