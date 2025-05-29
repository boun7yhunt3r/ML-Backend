from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import OperationalError
from database import SessionLocal, Log, init_db
from datetime import datetime
import json
import ipaddress

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    init_db()
    yield
    # Cleanup (if needed) on shutdown

app = FastAPI(title="Cloud-Native Data Ingestion Service", lifespan=lifespan)

class LogCreate(BaseModel):
    log_id: str
    source_ip: str
    event_type: str
    timestamp: str

@app.post("/ingest")
async def ingest_log(log: LogCreate):
    try:
        # Validate IP address
        ipaddress.ip_address(log.source_ip)
        
        # Validate ISO timestamp
        datetime.fromisoformat(log.timestamp.replace("Z", "+00:00"))
        
        # Store log in PostgreSQL
        db = SessionLocal()
        try:
            db_log = Log(
                log_id=log.log_id,
                source_ip=log.source_ip,
                event_type=log.event_type,
                timestamp=log.timestamp
            )
            db.add(db_log)
            db.commit()
            db.refresh(db_log)
            return {"message": "Log ingested successfully", "log_id": log.log_id}
        finally:
            db.close()
            
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
    except OperationalError as oe:
        raise HTTPException(status_code=503, detail="Database connection error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/load-mock-data")
async def load_mock_data():
    try:
        with open("data/mock_logs.json", "r") as f:
            logs = json.load(f)
        
        db = SessionLocal()
        try:
            for log in logs:
                db_log = Log(
                    log_id=log["log_id"],
                    source_ip=log["source_ip"],
                    event_type=log["event_type"],
                    timestamp=log["timestamp"]
                )
                db.add(db_log)
            db.commit()
            return {"message": f"Loaded {len(logs)} mock logs"}
        finally:
            db.close()
            
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Mock data file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading mock data: {str(e)}")