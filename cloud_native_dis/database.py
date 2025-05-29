from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import logging

# Database connection URL
DATABASE_URL = "postgresql://user:password@db:5432/logs"

Base = declarative_base()

class Log(Base):
    __tablename__ = "logs"
    
    log_id = Column(String, primary_key=True)
    source_ip = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)

# Create engine with retry mechanism
def create_engine_with_retry(max_retries=5, delay=5):
    for attempt in range(max_retries):
        try:
            engine = create_engine(DATABASE_URL)
            # Test connection
            with engine.connect() as connection:
                pass
            return engine
        except Exception as e:
            logging.warning(f"Database connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise Exception("Failed to connect to database after retries")

engine = create_engine_with_retry()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {str(e)}")
        raise