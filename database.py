from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from geoalchemy2 import Geometry
from datetime import datetime

DATABASE_URL = "sqlite:///omniscanner.db"  # swap with PostGIS in production

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class ScanRecord(Base):
    __tablename__ = "scan_records"

    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)

    density_index = Column(Float)
    anomaly_score = Column(Float)

    classification = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)
