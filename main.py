from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",   # Required parameter
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)
    return response.json()



@app.route("/")
def index():
    data = get_crypto_data()
    print(data)  
    return render_template("index.html", coins=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
