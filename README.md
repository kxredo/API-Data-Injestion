# Crypto API Data Ingestion

## Overview
This project automatically fetches cryptocurrency market data from the **CoinGecko API** and stores it in a **PostgreSQL database**. It is designed to run periodically, allowing you to track cryptocurrency prices historically, analyze trends, and visualize data.

---

## Features
- Fetches top cryptocurrency market data (name, symbol, price, market cap, last updated) from CoinGecko API.
- Stores data in a PostgreSQL table `crypto_prices`.
- Automatically creates the table if it doesn't exist.
- Logs every run with timestamps, inserted coins, and errors.
- Can be scheduled to run periodically using Python's `schedule` library or Windows Task Scheduler.

---

## Configuration (`conf.ini`)
Store your database credentials here:

```ini
[postgresql]
host = localhost
port = 5432
database = crypto_db
user = your_username
password = your_password
```

## Diagram 
```
             ┌─────────────────────────┐
             │   CoinGecko API (JSON)  │
             └─────────────┬──────────┘
                           │
                           ▼
             ┌─────────────────────────┐
             │     Python Script       │
             │  (main.py + db.py)     │
             ├─────────────────────────┤
             │ 1. Fetch data from API │
             │ 2. Parse JSON          │
             │ 3. Convert timestamps  │
             │ 4. Insert into DB      │
             └─────────────┬──────────┘
                           │
          ┌────────────────┴───────────────┐
          │                                │
          ▼                                ▼
 ┌─────────────────────┐          ┌───────────────────┐
 │ PostgreSQL Database │          │ Logging (app.log) │
 │   crypto_prices     │          │  - Records start  │
 │ - Stores coin data  │          │    and end of run │
 │ - Tracks price,     │          │  - Logs inserted  │
 │   market cap, etc.  │          │    coins          │
 └─────────────────────┘          │  - Logs errors    │
                                  └───────────────────┘

```
---
## Installation and Running the Project
1. **Clone the repository:**

```bash
git clone <your-repo-url>
cd API-Data-Ingestion
```
2. **Create a Python virtual environment (optional but recommended):**
# macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

# Windows
```bash
python -m venv venv
venv\Scripts\activate
```

3.  **Install Dependencies:**
```bash
pip install requests psycopg2 schedule
```

## Database Preview

Here’s a view of the `crypto_prices` table in DBeaver:
<img width="1026" height="423" alt="dbeaver_table" src="https://github.com/user-attachments/assets/e4dfc711-cbf7-457e-a9f2-703b581b023f" />




