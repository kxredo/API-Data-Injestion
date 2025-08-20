import requests
import schedule
import time
from datetime import datetime
from db import create_table, insert_coin_data, logging

def fetch_coin_data():
    logging.info("===== Script run started =====")
    start_time = datetime.now()
    
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Fetched {len(data)} coins from CoinGecko API")

        for coin in data:
            coin['last_updated'] = datetime.strptime(coin['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ")
            insert_coin_data(coin)

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
    except Exception as e:
        logging.error(f"Error processing data: {e}")
    
    end_time = datetime.now()
    logging.info(f"===== Script run finished (Duration: {end_time - start_time}) =====\n")

# Create table once before scheduling
create_table()

# Schedule the job every hour
schedule.every(1).hours.do(fetch_coin_data)

logging.info("Scheduler started. Script will fetch data every hour.")

# Keep script running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check for pending jobs every 60 seconds
