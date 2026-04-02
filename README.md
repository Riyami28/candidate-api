# Candidate Management API

A simple backend API to manage candidates for a recruitment system, built with Python and FastAPI.

## Features

- **Create Candidate** — `POST /candidates`
- **List Candidates** — `GET /candidates` (with optional `?status=` filter)
- **Update Status** — `PUT /candidates/{id}/status`

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API docs.

## Run Tests

```bash
pytest test_main.py -v
```
