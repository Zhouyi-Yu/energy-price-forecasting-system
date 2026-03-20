import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sql.database import SessionLocal, engine
from sql.models import RawMarketData, RawEventData, ProcessedFeatures

def build_features():
    db = SessionLocal()
    
    if db.query(ProcessedFeatures).first():
        print("Features already processed.")
        db.close()
        return

    print("Extracting raw data...")
    market_df = pd.read_sql(db.query(RawMarketData).statement, db.bind)
    event_df = pd.read_sql(db.query(RawEventData).statement, db.bind)
    
    if market_df.empty or event_df.empty:
        print("No raw data found. Please run mock_data_generator.py first.")
        db.close()
        return
        
    print("Engineering features...")
    df = pd.merge(market_df, event_df, on='date', how='inner')
    df = df.sort_values('date').set_index('date')
    
    # Handle NaNs from different frequencies (ffill carries previous value forward)
    df = df.ffill()
    
    # Calculate features
    df['wti_lag_1'] = df['wti_usd_per_barrel'].shift(1)
    df['wti_lag_7'] = df['wti_usd_per_barrel'].shift(7)
    df['wti_ma_7'] = df['wti_usd_per_barrel'].rolling(window=7).mean()
    df['wti_ma_30'] = df['wti_usd_per_barrel'].rolling(window=30).mean()
    
    # Conflict/Event Intensity Score combination
    df['event_intensity_score'] = (
        df['event_count_energy_related'] * 2.0 +
        df['event_count_middle_east_conflict'] * 1.5 +
        df['energy_infrastructure_attack_flag'].astype(int) * 10.0 +
        df['hormuz_disruption_flag'].astype(int) * 20.0 +
        df['headline_volume_energy_conflict'] * 0.1
    )
    
    df = df.dropna(subset=['wti_lag_7', 'wti_ma_30'])
    
    processed_records = []
    for date, row in df.iterrows():
        feat = ProcessedFeatures(
            date=date,
            wti_usd_per_barrel=row['wti_usd_per_barrel'],
            brent_usd_per_barrel=row['brent_usd_per_barrel'],
            us_gasoline_usd_per_gallon=row['us_gasoline_usd_per_gallon'],
            wti_lag_1=row['wti_lag_1'],
            wti_lag_7=row['wti_lag_7'],
            wti_ma_7=row['wti_ma_7'],
            wti_ma_30=row['wti_ma_30'],
            event_intensity_score=row['event_intensity_score']
        )
        processed_records.append(feat)
        
    db.bulk_save_objects(processed_records)
    db.commit()
    db.close()
    
    print(f"Engineered features for {len(processed_records)} dates successfully.")

if __name__ == "__main__":
    build_features()
