# Crypto Direction Predictor 

A real-time ML system that predicts whether Bitcoin price will go **UP or DOWN** in the next 30 seconds.

## System Architecture
```
CoinGecko API (live price)
        ↓
store_data.py (every 30 sec)
        ↓
PostgreSQL Database
        ↓
retrain.py (every 1 hour)
        ↓
direction_model.pkl
        ↓
FastAPI /predict endpoint
        ↓
Streamlit Dashboard
```

## Tech Stack

- **Data Pipeline** — Python, CoinGecko API, psycopg2
- **Database** — PostgreSQL
- **ML Model** — RandomForestClassifier (scikit-learn)
- **Experiment Tracking** — MLflow
- **API** — FastAPI
- **Frontend** — Streamlit, Plotly
- **Environment** — Python venv

## Features

- Live data collection every 30 seconds
- Auto-retraining every hour on fresh data
- MLflow experiment tracking across runs
- REST API for predictions
- Interactive Streamlit dashboard

## Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | 81% |
| Macro F1 | 0.77 |
| UP Recall | 85% |
| Naive Baseline | 74.7% |

## Project Structure
```
crypto_project/
    store_data.py      — live data collection pipeline
    main.py            — FastAPI prediction endpoint
    retrain.py         — automated model retraining with MLflow
    app.py             — Streamlit frontend dashboard
    analysis.ipynb     — EDA and model development
    requirements.txt   — dependencies
    .env               — credentials (not pushed)
```

## Setup

1. Clone the repo
2. Create virtual environment and install dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
3. Create `.env` file with your PostgreSQL credentials
4. Create the database table
```sql
CREATE TABLE crypto_prices (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
5. Run the system
```bash
# Terminal 1 — collect data
python store_data.py

# Terminal 2 — serve predictions
uvicorn main:app --reload

# Terminal 3 — auto retrain
python retrain.py

# Terminal 4 — dashboard
streamlit run app.py
```

## API Usage
```bash
GET http://localhost:8000/predict
```

Response:
```json
{
  "prediction": "UP",
  "confidence": 54.58,
  "current_price": 70816.0
}
```

## Author

Aditya Kumar — [GitHub](https://github.com/adsharma14) | [LinkedIn](https://linkedin.com/in/your-linkedin)