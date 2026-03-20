import os
import pickle
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sql.database import SessionLocal
from sql.models import ProcessedFeatures, RawMarketData, RawEventData

app = FastAPI(title="Gasoline Price Forecasting API")

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "lr_model.pkl")
lr_model = None

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "project": "Gasoline Price Forecasting System",
        "documentation": "/docs",
        "endpoints": {
            "forecast": "/forecast/wti",
            "history": "/history/wti",
            "events": "/events/recent"
        }
    }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    global lr_model
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            lr_model = pickle.load(f)

@app.get("/forecast/wti")
def get_wti_forecast(horizon: str = "1d", db: Session = Depends(get_db)):
    if horizon != "1d":
        raise HTTPException(status_code=400, detail="Only 1d horizon is exposed in MVP route.")
        
    latest = db.query(ProcessedFeatures).order_by(desc(ProcessedFeatures.date)).first()
    if not latest:
        raise HTTPException(status_code=404, detail="No feature data available to score.")
        
    if not lr_model:
        raise HTTPException(status_code=503, detail="Model artifact missing. Train models first.")
        
    import pandas as pd
    features = pd.DataFrame([{
        'wti_usd_per_barrel': latest.wti_usd_per_barrel,
        'wti_lag_1': latest.wti_lag_1 or latest.wti_usd_per_barrel,
        'wti_ma_7': latest.wti_ma_7 or latest.wti_usd_per_barrel,
        'event_intensity_score': latest.event_intensity_score or 0.0
    }])
    
    pred = lr_model.predict(features)[0]
    
    return {
        "target": "wti_next_day",
        "forecast_timestamp": (latest.date + timedelta(days=1)).isoformat(),
        "predicted_value": round(float(pred), 2),
        "recent_actual_value": round(float(latest.wti_usd_per_barrel), 2),
        "model_version": "lr_v1",
        "recent_event_intensity": round(float(latest.event_intensity_score or 0.0), 2)
    }

@app.get("/history/wti")
def get_wti_history(limit: int = 30, db: Session = Depends(get_db)):
    records = db.query(RawMarketData).order_by(desc(RawMarketData.date)).limit(limit).all()
    # Reverse so it returns chronological
    return [{"date": r.date.isoformat(), "wti_usd_per_barrel": round(r.wti_usd_per_barrel, 2)} for r in records[::-1]]

@app.get("/events/recent")
def get_recent_events(limit: int = 7, db: Session = Depends(get_db)):
    records = db.query(RawEventData).order_by(desc(RawEventData.date)).limit(limit).all()
    return [
        {
            "date": r.date.isoformat(), 
            "energy_attack": r.energy_infrastructure_attack_flag,
            "headline_volume": round(r.headline_volume_energy_conflict, 2),
            "tone_score": round(r.headline_tone_score, 2)
        } for r in records[::-1]
    ]
