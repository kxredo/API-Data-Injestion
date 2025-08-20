from datetime import datetime
import psycopg2
from contextlib import closing
import configparser
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def load_db_config(path='conf.ini'):
    config = configparser.ConfigParser()
    config.read(path)
    if 'postgresql' not in config:
        logging.error("No [postgresql] section found in conf.ini")
        raise KeyError("No [postgresql] section found in conf.ini")
    return config['postgresql']

db_config = load_db_config()

def get_connection():
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        logging.info("Database connection established")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

def create_table():
    try:
        with closing(get_connection()) as conn, conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id SERIAL PRIMARY KEY,
                coin_name VARCHAR(50),
                symbol VARCHAR(10),
                price_usd NUMERIC,
                market_cap NUMERIC,
                last_updated TIMESTAMP
            )
            """)
            conn.commit()
            logging.info("Table 'crypto_prices' is ready")
    except Exception as e:
        logging.error(f"Error creating table: {e}")
        raise

def insert_coin_data(coin_data):
    try:
        with closing(get_connection()) as conn, conn.cursor() as cur:
            cur.execute("""
            INSERT INTO crypto_prices (coin_name, symbol, price_usd, market_cap, last_updated)
            VALUES (%s, %s, %s, %s, %s)
            """, (
                coin_data['name'],
                coin_data['symbol'],
                coin_data['current_price'],
                coin_data['market_cap'],
                coin_data['last_updated']
            ))
            conn.commit()

            logging.info(f"[Run {datetime.now().strftime('%Y%m%d-%H%M%S')}] Inserted {coin_data['name']} ({coin_data['symbol']}) into database")
    except Exception as e:
        logging.error(f"Failed to insert {coin_data['name']}: {e}")
