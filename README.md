# OurAPI2026

A Flask REST API for managing students and reports.

## Tech stack

- Python
- Flask
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
