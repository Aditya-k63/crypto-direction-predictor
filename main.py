from fastapi import FastAPI
import pandas as pd
import joblib
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# ── DB connection ───────────────────────────────────────────
def get_data():
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    df = pd.read_sql("SELECT * FROM crypto_prices ORDER BY timestamp DESC LIMIT 20", engine)
    return df

# Feature engineering 
def build_features(df):
    df = df.sort_values(by='timestamp').reset_index(drop=True)

    df['lag_1'] = df['price'].shift(1)
    df['lag_2'] = df['price'].shift(2)
    df['lag_3'] = df['price'].shift(3)
    df['momentum_1'] = df['price'].shift(1) - df['price'].shift(2)
    df['momentum_3'] = df['price'].shift(1) - df['price'].shift(4)
    df['rolling_mean_5'] = df['price'].shift(1).rolling(5).mean()
    df['rolling_std_5']  = df['price'].shift(1).rolling(5).std()

    df = df.dropna()
    return df

#  Load model once at starting only 
model = joblib.load("direction_model.pkl")

#  Prediction endpoint 
@app.get("/predict")
def predict():
    df = get_data()
    df = build_features(df)

    features = ['lag_1', 'lag_2', 'lag_3',
                'momentum_1', 'momentum_3',
                'rolling_mean_5', 'rolling_std_5']

    latest = df[features].iloc[[-1]]

    prediction = model.predict(latest)[0]
    probability = model.predict_proba(latest)[0]

    return {
        "prediction": "UP" if prediction == 1 else "DOWN",
        "confidence": round(float(max(probability)) * 100, 2),
        "current_price": float(df['price'].iloc[-1])
    }

# Health check 
@app.get("/")
def root():
    return {"status": "running"}