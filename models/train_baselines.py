import os
import sys
import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql.database import SessionLocal
from sql.models import ProcessedFeatures

def train_baselines():
    print("Loading engineered features...")
    db = SessionLocal()
    df = pd.read_sql(db.query(ProcessedFeatures).statement, db.bind)
    db.close()
    
    if df.empty:
        print("No processed features found. Run etl/mock_data_generator.py and features/engineering.py first.")
        return
        
    df = df.sort_values('date').set_index('date')
    
    # Target: Predict next-day WTI
    df['target_wti_next_day'] = df['wti_usd_per_barrel'].shift(-1)
    df = df.dropna(subset=['target_wti_next_day'])
    
    # Chronological Split (80/20) for Backtesting
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    features = ['wti_usd_per_barrel', 'wti_lag_1', 'wti_ma_7', 'event_intensity_score']
    
    X_train = train_df[features]
    y_train = train_df['target_wti_next_day']
    X_test = test_df[features]
    y_test = test_df['target_wti_next_day']
    
    # 1. Naive Baseline (Last Value)
    naive_preds = X_test['wti_usd_per_barrel']
    naive_mae = mean_absolute_error(y_test, naive_preds)
    naive_rmse = mean_squared_error(y_test, naive_preds) ** 0.5
    
    print(f"Naive Baseline     - MAE: {naive_mae:.2f}, RMSE: {naive_rmse:.2f}")
    
    # 2. Linear Regression (Market + Geo Features)
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_preds = lr.predict(X_test)
    
    lr_mae = mean_absolute_error(y_test, lr_preds)
    lr_rmse = mean_squared_error(y_test, lr_preds) ** 0.5
    
    print(f"Linear Regression  - MAE: {lr_mae:.2f}, RMSE: {lr_rmse:.2f}")
    
    # Save Model Artifact
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    model_path = os.path.join(os.path.dirname(__file__), 'lr_model.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(lr, f)
        
    print(f"Baseline model trained and saved to {model_path}")

if __name__ == "__main__":
    train_baselines()
