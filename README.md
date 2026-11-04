# OurAPI2026

A Flask REST API for managing students and reports.

## Tech stack

- Python
- Flask
- MySQL
- PyMySQL
- Docker
- uv
- Postman

## Setup

1. Create a virtual environment:

   ```powershell
   uv venv .venv
   ```

2. Install the dependencies:

   ```powershell
   uv pip install -r requirements.txt
   ```

3. Run the app:

   ```powershell
   .venv\Scripts\python.exe app.py
   ```

## Database (MySQL)

1. Start MySQL in Docker:

   ```powershell
   docker run --name part2-mysql -e MYSQL_ROOT_PASSWORD=root123 -e MYSQL_DATABASE=university -p 3307:3306 -v mysql_data:/var/lib/mysql -d mysql:8.4
   ```

2. Create the tables:

   ```powershell
   Get-Content schema.sql | docker exec -i part2-mysql mysql -uroot -proot123 university
   ```

3. Load the demo data and the login user (admin / admin123):

   ```powershell
   Get-Content seed.sql | docker exec -i part2-mysql mysql -uroot -proot123 university
   ```

The API connects to MySQL on 127.0.0.1 port 3307 (see db.py).

## Run with Docker

1. Open Docker Desktop and wait for "Engine running".
2. Build the image:

   ```powershell
   docker build -t ourapi2026 .
   ```

3. Run the image, then open http://127.0.0.1:5000:

   ```powershell
   docker run --rm --name ourapi2026 -p 5000:5000 ourapi2026
   ```

## Endpoints

| Method | Endpoint | Purpose | Token needed |
|---|---|---|---|
| GET | `/` | Health check | No |
| POST | `/reports` | Create a report | No |
| GET | `/reports` | Get all reports | No |
| GET | `/reports/<id>` | Get one report | No |
| PUT | `/reports/<id>` | Update a report | No |
| DELETE | `/reports/<id>` | Delete a report | No |
| POST | `/students` | Create a student | No |
| GET | `/students` | Get all students | Yes |
| GET | `/students/<id>` | Get one student | Yes |
| PUT | `/students/<id>` | Update a student | Yes |
| DELETE | `/students/<id>` | Delete a student | Yes |
| POST | `/login` | Get a token | No |
| POST | `/refresh` | Get a new token using the current token | Current token |
