import pandas as pd
import joblib
import time
import logging
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, accuracy_score
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s — %(message)s'
)

#  DB connection
def load_data():
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    df = pd.read_sql("SELECT * FROM crypto_prices ORDER BY timestamp ASC", engine)
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

    df['direction'] = (df['price'] > df['price'].shift(1)).astype(int)

    df = df.dropna()
    return df

# Train and save model 
def retrain():
    logging.info("Starting retraining...")

    df = load_data()
    df = build_features(df)

    logging.info(f"Rows available: {len(df)}")

    X = df[['lag_1', 'lag_2', 'lag_3',
            'momentum_1', 'momentum_3',
            'rolling_mean_5', 'rolling_std_5']]
    y = df['direction']

    params = {
        "n_estimators": 100,
        "max_depth": 4,
        "min_samples_leaf": 5,
        "class_weight": "balanced"
    }

    model = RandomForestClassifier(**params, random_state=42)
    model.fit(X, y)

    y_pred = model.predict(X)
    acc = accuracy_score(y, y_pred)
    f1  = f1_score(y, y_pred, average='macro')

    # MLflow logging 
    mlflow.set_experiment("crypto_direction_prediction")

    with mlflow.start_run():
        mlflow.log_params(params)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_macro", f1)
        mlflow.log_metric("rows_trained_on", len(df))
        mlflow.sklearn.log_model(model, "random_forest_model")

        logging.info(f"MLflow run logged — Accuracy: {acc:.4f} | F1: {f1:.4f}")

    joblib.dump(model, 'direction_model.pkl')
    logging.info("Model retrained and saved.")

# Loop for training  
if __name__ == "__main__":
    RETRAIN_EVERY_SECONDS = 3600

    while True:
        retrain()
        logging.info(f"Next retraining in {RETRAIN_EVERY_SECONDS // 60} minutes.")
        time.sleep(RETRAIN_EVERY_SECONDS)