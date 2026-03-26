import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Page config 
st.set_page_config(
    page_title="Crypto Price Predictor",
    layout="wide"
)

# DB connection 
def load_data():
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    df = pd.read_sql("SELECT * FROM crypto_prices ORDER BY timestamp ASC", engine)
    return df

# Fetch prediction from FastAPI
def get_prediction():
    try:
        response = requests.get("http://127.0.0.1:8000/predict")
        return response.json()
    except:
        return None

# UI 
st.title(" Bitcoin Direction Predictor")
st.caption("Live ML system — data collected every 30 seconds")

st.divider()

# Top metrics 
pred = get_prediction()

col1, col2, col3 = st.columns(3)

if pred:
    col1.metric(
        label="Current Price",
        value=f"${pred['current_price']:,.2f}"
    )

    direction = pred['prediction']
    confidence = pred['confidence']

    col2.metric(
        label="Prediction",
        value=f"{'⬆UP' if direction == 'UP' else '⬇DOWN'}"
    )

    col3.metric(
        label="Confidence",
        value=f"{confidence}%"
    )
else:
    st.error("Could not connect to prediction API. Is your uvicorn is running?")

st.divider()

# Price chart 
st.subheader("Live Price History")

df = load_data()

fig = px.line(
    df,
    x='timestamp',
    y='price',
    title='Bitcoin Price Over Time',
    labels={'price': 'Price (USD)', 'timestamp': 'Time'}
)

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig, width="stretch")

#  Raw data toggleeee
with st.expander("View raw data"):
    st.dataframe(df.tail(20))

st.divider()

# Auto refresh 
st.caption("Page refreshes every 60 seconds")
time.sleep(60)
st.rerun()