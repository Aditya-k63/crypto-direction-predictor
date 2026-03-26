import requests

url = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": "bitcoin",
    "vs_currencies": "usd"
}

response = requests.get(url, params=params)

data = response.json()

price = data['bitcoin']['usd']

print(price)
