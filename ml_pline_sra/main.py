from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from database import init_db, log_prediction
from datetime import datetime

app = FastAPI(title="Security Risk Analysis API")

# Load the trained model
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

class EventInput(BaseModel):
    request_size: float
    response_time: float

@app.post("/predict")
async def predict(event: EventInput):
    try:
        # Preprocess input
        data = pd.DataFrame([[event.request_size, event.response_time]], columns=["request_size", "response_time"])
        data_scaled = scaler.transform(data)
        
        # Make prediction
        prediction = model.predict(data_scaled)[0]
        
        # Generate event_id and timestamp
        event_id = f"evt_{int(datetime.now().timestamp())}"
        timestamp = datetime.now().isoformat() + "Z"
        
        # Log prediction to SQLite
        log_prediction(event_id, event.request_size, event.response_time, int(prediction), timestamp)
        
        return {"event_id": event_id, "is_risky": int(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")