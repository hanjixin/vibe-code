#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo "Stopping servers..."
    kill $(jobs -p) 2>/dev/null
}
trap cleanup EXIT

echo "Starting Backend..."
source backend/.venv/bin/activate
# Run uvicorn from root, pointing to backend.app.main:app
uvicorn backend.app.main:app --reload --port 8000 &

echo "Starting Frontend..."
cd frontend
npm run dev &
cd ..

echo "Servers started. Backend at http://localhost:8000, Frontend at http://localhost:5173 (usually)."
echo "Press Ctrl+C to stop."
wait
