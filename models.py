from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./results.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserResult(Base):
    __tablename__ = "user_results"
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=False)
    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=True)
    severity = Column(Float, nullable=True)
    report_path = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Create the table
Base.metadata.create_all(bind=engine)