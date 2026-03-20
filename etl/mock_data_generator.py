import os
import sys
import random
from datetime import datetime, timedelta

# Add parent dir to path so we can import sql module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sql.database import SessionLocal, engine, Base
from sql.models import RawMarketData, RawEventData, ProcessedFeatures

def generate_mock_data():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    # Check if data already exists
    if db.query(RawMarketData).first():
        print("Mock data already exists. Skipping generation.")
        return
        
    start_date = datetime(2020, 1, 1)
    end_date = datetime.today()
    delta = end_date - start_date
    
    wti_price = 60.0
    brent_price = 65.0
    gasoline_price = 2.50
    
    print(f"Generating {(delta.days + 1)} days of mocked historical data...")
    for i in range(delta.days + 1):
        current_date = start_date + timedelta(days=i)
        
        # Simulated price evolution (Random Walk with Drift/Mean Reversion proxy)
        wti_price += random.uniform(-1.5, 1.5)
        # Add bounds roughly mimicking 2020-2026
        wti_price = max(20.0, min(120.0, wti_price)) 
        
        brent_price = wti_price + random.uniform(2, 6)
        gasoline_price = (wti_price * 0.03) + random.uniform(0.5, 1.0)
        
        market_entry = RawMarketData(
            date=current_date.date(),
            wti_usd_per_barrel=wti_price,
            brent_usd_per_barrel=brent_price,
            us_gasoline_usd_per_gallon=gasoline_price if current_date.weekday() == 0 else None,
            ab_gasoline_cad_per_litre=(gasoline_price * 1.35) if current_date.day == 1 else None,
            refinery_utilization_pct=random.uniform(75, 95) if current_date.weekday() == 2 else None,
            gasoline_inventory_barrels=random.uniform(200e6, 260e6) if current_date.weekday() == 2 else None,
            crude_inventory_barrels=random.uniform(400e6, 500e6) if current_date.weekday() == 2 else None,
        )
        db.add(market_entry)
        
        # Event data (simulating a shock in 2026 as per SRS)
        is_shock_period = (current_date.year == 2026 and current_date.month >= 3)
        
        event_entry = RawEventData(
            date=current_date.date(),
            event_count_energy_related=random.randint(5, 20) if is_shock_period else random.randint(0, 5),
            event_count_middle_east_conflict=random.randint(10, 50) if is_shock_period else random.randint(0, 10),
            energy_infrastructure_attack_flag=random.random() > 0.8 if is_shock_period else False,
            hormuz_disruption_flag=random.random() > 0.9 if is_shock_period else False,
            sanctions_flag=random.random() > 0.95,
            headline_volume_energy_conflict=random.uniform(50, 200) if is_shock_period else random.uniform(5, 30),
            headline_tone_score=random.uniform(-5, -1) if is_shock_period else random.uniform(-1, 1),
        )
        db.add(event_entry)
        
    db.commit()
    db.close()
    print("Mock data generated successfully!")

if __name__ == "__main__":
    generate_mock_data()
