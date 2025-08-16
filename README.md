

# Crypto Dashboard

A simple Flask-based web application that displays the top cryptocurrencies using the [CoinGecko API](https://www.coingecko.com/en/api/documentation). It fetches live price, market cap, and daily change data, then shows them in a clean, responsive table. See a live version of the app [here](https://crypto-dash.onrender.com/).

---

## Installation & Local Setup

1.  **Clone this repository**
    ```bash
    git clone [https://github.com/sarabiji/crypto-dashboard.git](https://github.com/sarabiji/crypto-dashboard.git)
    cd crypto-dashboard
    ```
2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    # Mac/Linux
    source venv/bin/activate
    # Windows
    venv\Scripts\activate
    ```
3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the app locally**
    ```bash
    python main.py
    ```
    Your app will be running at: `http://127.0.0.1:5000`

---

## Deployment to Render

1.  Push your project to GitHub.
2.  Go to [Render](https://render.com/) and click **New Web Service**.
3.  Connect your GitHub repo.
4.  Render will automatically detect the **Build** and **Start** commands from the `requirements.txt` and `Procfile`.

💡 **Tip**: Add a `Procfile` to your project's root directory to let Render know how to start your app without manual configuration.
 ```bash
  web: gunicorn main:app
 ```

---

## API Details

We use the following endpoint to fetch data:

`GET https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false`

This returns JSON fields like:
-   `name`
-   `current_price`
-   `market_cap`
-   `price_change_percentage_24h`
-   `image`

---

## Project Structure
 ```bash
crypto-dashboard/
│
├── main.py              # Flask app entry point
├── requirements.txt     # Python dependencies
├── Procfile             # For Render deployment
├── templates/
│   └── index.html       # HTML template
├── static/
│   └── style.css        # Stylesheet
└── README.md            # This file
 ```

---

## Requirements

The project uses the following dependencies:
-   `Flask==3.0.3`
-   `requests==2.32.3`
-   `gunicorn==23.0.0`

---

## License

This project is licensed under the **MIT License**.

Data Source: Powered by [CoinGecko API](https://www.coingecko.com/en/api)
