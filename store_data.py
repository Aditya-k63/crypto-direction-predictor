import requests
import psycopg2
import time

def fetch_and_store():
    try:
        # STEP 1: Fetch data
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd"
        }

        response = requests.get(url, params=params)
        data = response.json()

        price = data['bitcoin']['usd']

        # STEP 2: DB connection
        conn = psycopg2.connect(
            dbname="crypto",
            user="postgres",
            password="1234509876",
            host="localhost",
            port="5432"
        )

        cur = conn.cursor()

        # STEP 3: Insert
        cur.execute(
            "INSERT INTO crypto_prices (name, price) VALUES (%s, %s)",
            ("bitcoin", price)
        )

        conn.commit()
        cur.close()
        conn.close()

        print("Inserted:", price)

    except Exception as e:
        print("Error:", e)


# 🔁 LOOP
while True:
    fetch_and_store()
    time.sleep(30)  # wait 30 seconds