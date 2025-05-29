# Cloud-Native Data Ingestion Service

A cloud-native FastAPI service for ingesting and storing security logs from a mock external API (JSON file), using PostgreSQL for storage, Docker and docker-compose for containerization, and a GitHub Actions CI/CD pipeline for automated testing and building. This project simulates the "implementation of cloud-native solutions" for the Senior Software Engineer (Backend) role at MATVIS.

# Objective

Ingest security logs from a mock external API and store them in a PostgreSQL database, with input validation, error handling, and a CI/CD pipeline for automated testing and deployment.

# Project Structure

- `main.py`: FastAPI application with ingestion and mock data loading endpoints.
- `database.py`: PostgreSQL setup and operations using SQLAlchemy.
- `models.py`: Pydantic model for input validation.
- `data/mock_logs.json`: Mock security logs simulating an external API.
- `Dockerfile`: Docker configuration for the FastAPI app.
- `docker-compose.yml`: Configuration for the app and PostgreSQL database.
- `requirements.txt`: Python dependencies.
- `.github/workflows/ci.yml`: GitHub Actions CI/CD pipeline configuration.

# Prerequisites

- **Docker and docker-compose**: Installed and running for containerized deployment.
- **Python 3.9+**: Optional, for local testing without Docker.
- **curl or Postman**: For testing the API endpoint.
- **GitHub**: For CI/CD pipeline integration.

# Setup Instructions

## Local Setup (Without Docker)

1. Create a project directory and save the required files: `main.py`, `database.py`, `models.py`, `data/mock_logs.json`, `requirements.txt`.
2. Set up a local PostgreSQL database (e.g., using Docker):
   ```bash
   docker run -d -p 5432:5432 --name postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=logs postgres:latest
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set the environment variable for the database:
   ```bash
   export DATABASE_URL=postgresql://user:password@localhost:5432/logs
   ```
5. Run the FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```
6. Access the API at `http://localhost:8000`.

## Docker Setup

1. Save all files in a project directory, including a `data` directory with `mock_logs.json`.
2. Build and start the services:
   ```bash
   docker-compose up --build
   ```
3. Access the API at `http://localhost:8000`.
4. The PostgreSQL database is automatically set up with persistent storage via the `pgdata` volume.

# Testing the API

## Ingest Log (POST /ingest)

```bash
curl -X POST "http://localhost:8000/ingest" \
-H "Content-Type: application/json" \
-d '{"log_id": "log_004", "source_ip": "192.168.1.4", "event_type": "logout", "timestamp": "2025-05-29T10:00:00Z"}'
```

**Expected Response**:
```json
{"message": "Log ingested successfully", "log_id": "log_004"}
```

## Load Mock Data (GET /load-mock-data)

```bash
curl -X GET "http://localhost:8000/load-mock-data"
```

**Expected Response**:
```json
{"message": "Loaded 3 mock logs"}
```

## Verify Data in PostgreSQL

```bash
docker-compose exec db psql -U user -d logs -c "SELECT * FROM logs;"
```

**Expected Output**აშ
 log_id  |  source_ip   |  event_type   |      timestamp
---------+--------------+---------------+---------------------
 log_001 | 192.168.1.1  | login_attempt | 2025-05-29T09:26:00Z
 log_002 | 10.0.0.2     | file_access   | 2025-05-29T09:27:00Z
 log_003 | 172.16.0.3   | api_call      | 2025-05-29T09:28:00Z

# CI/CD Pipeline

The `.github/workflows/ci.yml` defines a GitHub Actions workflow that:

- Checks out the code.
- Sets up Python 3.9.
- Installs dependencies.
- Runs tests with pytest (requires a test file).
- Builds the Docker image.

**To Use the CI/CD Pipeline**:

1. Push the project to a GitHub repository.
2. Add a `tests` directory with test cases (e.g., `test_main.py`) for pytest.
3. The workflow runs automatically on push, performing linting, testing, and building the Docker image.

# Implementation Details

- **FastAPI**: Provides `/ingest` endpoint for log ingestion and `/load-mock-data` for loading mock JSON data.
- **PostgreSQL**: Stores logs in a `logs` table with columns `log_id` (primary key), `source_ip`, `event_type`, and `timestamp`.
- **SQLAlchemy**: Manages database interactions with automatic table creation and session handling.
- **Error Handling**: Validates IP addresses and ISO timestamps using Pydantic and `ipaddress`. Handles database connection errors.
- **Docker and docker-compose**: Containerizes the app and PostgreSQL, with environment variables for database connection and a `pgdata` volume for persistence.
- **CI/CD**: GitHub Actions ensures automated testing and building, aligning with DevOps practices.
- **Security**: Input validation prevents invalid data, and database credentials are managed via environment variables.

# Potential Optimizations

- **Performance**: Add indexes on `source_ip` and `timestamp` for faster queries.
- **Scalability**: Deploy with Kubernetes for auto-scaling under high traffic.
- **Security**: Add API key authentication to secure endpoints.
- **Data Source**: Replace the JSON file with a real external API for production use.

# Troubleshooting

- **Database Connection Errors**: Ensure the PostgreSQL container is running and accessible (`db:5432`). Check the `DATABASE_URL` environment variable.
- **Invalid Input**: Verify JSON input matches the Pydantic model (e.g., valid IP, ISO timestamp).
- **Port Conflicts**: Confirm port `8000` is free or modify `docker-compose.yml`.
- **CI/CD Failures**: Add a `tests` directory with pytest test cases to enable the GitHub Actions workflow.

# Why or whynot

- **Explain Design**: Discuss why PostgreSQL was chosen (scalable, robust) over SQLite and how the service simulates cloud-native ingestion.
- **Error Handling**: Highlight IP and timestamp validation and database error handling, aligning with MATVIS’s security focus.
- **CI/CD**: Explain the GitHub Actions workflow and its role in reliable deployments, tying to DevOps requirements.
- **Docker**: Describe the `docker-compose` setup, emphasizing persistent storage and service dependencies.
- **Mentoring**: Structure explanations clearly, as if guiding a junior developer, to meet mentoring expectations.
