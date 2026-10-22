# Genome Analysis Tool

## Backend (FastAPI)

```
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

API docs: http://127.0.0.1:8000/docs

### Run step 1 tests

```
cd backend
venv/bin/python run_tests.py
```

## Frontend (React + Vite)

```
cd frontend
npm run dev
```

Open the URL printed in the terminal (default http://localhost:5173).

Run both the backend and frontend at the same time, in separate terminals.
