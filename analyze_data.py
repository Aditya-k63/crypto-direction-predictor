import pandas as pd
import psycopg2

# Connect to DB
conn = psycopg2.connect(
    dbname="crypto",
    user="postgres",
    password="1234509876",
    host="localhost",
    port="5432"
)

# Load data into pandas
query = "SELECT * FROM crypto_prices"
df = pd.read_sql(query, conn)

conn.close()

# Basic checks
print(df.head())
print(df.info())
print(df.describe())


import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

plt.plot(df['timestamp'], df['price'])
plt.xlabel("Time")
plt.ylabel("Price")
plt.title("Bitcoin Price Over Time")
plt.xticks(rotation=45)

plt.tight_layout()

plt.show()  # 👈 THIS is required




# Sort data first (VERY IMPORTANT)
df = df.sort_values(by='timestamp')

# Create lag feature
df['prev_price'] = df['price'].shift(1)

# Remove NaN row
df = df.dropna()

print(df.columns)


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Features and target
X = df[['prev_price']]
y = df['price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

print("Sample Predictions:")
print(y_pred[:5])