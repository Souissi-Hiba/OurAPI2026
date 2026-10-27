# OurAPI2026

A Flask REST API for managing students and reports.

## Tech stack

- Python
- Flask
- Docker
- uv
- Postman

## Setup

1. Create a virtual environment:

   ```powershell
   uv venv .venv
   ```

2. Install Flask:

   ```powershell
   uv pip install Flask
   ```

3. Run the app:

   ```powershell
   .venv\Scripts\python.exe app.py
   ```

## Run with Docker

1. Open Docker Desktop and wait for "Engine running".
2. Build the image:

   ```powershell
   docker build -t ourapi2026 .
   ```

3. Run the image, then open http://127.0.0.1:5000:

   ```powershell
   docker run --rm -p 5000:5000 ourapi2026
   ```

## Endpoints

| Method | Endpoint | Purpose | Token needed |
|---|---|---|---|
| GET | `/` | Health check | No |
| POST | `/reports` | Create a report | No |
| GET | `/reports` | Get all reports | No |
| GET | `/reports/<id>` | Get one report | No |
| POST | `/students` | Create a student | No |
| GET | `/students` | Get all students | Yes |
| GET | `/students/<id>` | Get one student | Yes |
| POST | `/login` | Get a token | No |
| POST | `/refresh` | Get a new token using the current token | Current token |
