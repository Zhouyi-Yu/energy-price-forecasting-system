from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from .database import Base

class RawMarketData(Base):
    __tablename__ = "raw_market_data"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, unique=True)
    wti_usd_per_barrel = Column(Float, nullable=True)
    brent_usd_per_barrel = Column(Float, nullable=True)
    us_gasoline_usd_per_gallon = Column(Float, nullable=True)
    ab_gasoline_cad_per_litre = Column(Float, nullable=True)
    refinery_utilization_pct = Column(Float, nullable=True)
    gasoline_inventory_barrels = Column(Float, nullable=True)
    crude_inventory_barrels = Column(Float, nullable=True)
    
class RawEventData(Base):
    __tablename__ = "raw_event_data"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, unique=True)
    event_count_energy_related = Column(Integer, default=0)
    event_count_middle_east_conflict = Column(Integer, default=0)
    energy_infrastructure_attack_flag = Column(Boolean, default=False)
    hormuz_disruption_flag = Column(Boolean, default=False)
    sanctions_flag = Column(Boolean, default=False)
    headline_volume_energy_conflict = Column(Float, default=0.0)
    headline_tone_score = Column(Float, default=0.0)

class ProcessedFeatures(Base):
    __tablename__ = "processed_features"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, unique=True)
    wti_usd_per_barrel = Column(Float)
    brent_usd_per_barrel = Column(Float)
    us_gasoline_usd_per_gallon = Column(Float)
    wti_lag_1 = Column(Float, nullable=True)
    wti_lag_7 = Column(Float, nullable=True)
    wti_ma_7 = Column(Float, nullable=True)
    wti_ma_30 = Column(Float, nullable=True)
    event_intensity_score = Column(Float, nullable=True)
