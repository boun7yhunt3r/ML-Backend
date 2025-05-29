# AI Firewall API

A lightweight, secure REST API built with FastAPI and SQLite for logging and retrieving security events, designed for cloud-native deployment with Docker.

# Prerequisites

- **Docker**: Installed and running for containerized deployment.
- **Python 3.9+**: Optional, for local testing without Docker.
- **curl or Postman**: For testing API endpoints.

# Setup Instructions

## Local Setup (Without Docker)

1. Create a project directory and add the required files: `main.py`, `database.py`, `models.py`, and `requirements.txt`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```
4. Access the API at `http://localhost:8000`.

## Docker Setup

1. Save all project files in a project directory.
2. Build the Docker image:
   ```bash
   docker build -t ai-firewall-api .
   ```
3. Run the Docker container with a volume for SQLite persistence:
   ```bash
   docker run -d -p 8000:8000 -v $(pwd)/events.db:/app/events.db ai-firewall-api
   ```
4. Access the API at `http://localhost:8000`.

# Testing the API

## Log an Event (POST /log-event)

```bash
curl -X POST "http://localhost:8000/log-event" \
-H "Content-Type: application/json" \
-H "X-API-Key: secure-api-key-12345" \
-d '{"event_id": "evt_123", "timestamp": "2025-05-29T09:26:00Z", "severity": "high", "description": "Unauthorized access attempt"}'
```

**Expected Response**:
```json
{"message": "Event logged successfully", "event_id": "evt_123"}
```

## Retrieve All Events (GET /events)

```bash
curl -X GET "http://localhost:8000/events" \
-H "X-API-Key: secure-api-key-12345"
```

**Expected Response**:
```json
{
  "events": [
    {"event_id": "evt_123", "timestamp": "2025-05-29T09:26:00Z", "severity": "high", "description": "Unauthorized access attempt"}
  ]
}
```

## Retrieve Events by Severity (GET /events?severity=high)

```bash
curl -X GET "http://localhost:8000/events?severity=high" \
-H "X-API-Key: secure-api-key-12345"
```

# Error Handling

- **Invalid Timestamp**: Returns 400 with `"Invalid timestamp format"`.
- **Duplicate Event ID**: Returns 400 with `"Event ID already exists"`.
- **Invalid API Key**: Returns 401 with `"Invalid API key"`.
- **Validation**: Non-empty description and valid severity enforced via Pydantic.

# Implementation Details

- **FastAPI**: Provides async capabilities and automatic OpenAPI documentation.
- **SQLite**: Lightweight relational database with a single `events` table.
- **Input Validation**: Pydantic enforces non-empty `event_id`, ISO timestamp, valid severity enum, and non-empty description.
- **Security**: API key authentication via `X-API-Key` header secures all endpoints.
- **Docker**: Ensures cloud-native deployment with persistent SQLite storage via a volume.

# Potential Optimizations

- Add indexes on `severity` and `timestamp` for faster `GET /events` queries.
- Implement caching with Redis for frequent `GET /events` calls.
- Use `aiosqlite` for non-blocking database operations.
- Scale with Kubernetes for high-traffic scenarios.

# Troubleshooting

- **Database Errors**: Ensure `events.db` is writable in the Docker volume.
- **Port Conflicts**: Verify port `8000` is free or modify it in the Docker run command.
- **API Key Issues**: Use the correct key (`secure-api-key-12345`) in the `X-API-Key` header.