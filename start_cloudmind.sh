#!/bin/bash

echo "🚀 Starting CloudMind (Local Setup)..."

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "❌ PostgreSQL is not running. Starting it..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew services start postgresql
    else
        sudo systemctl start postgresql
    fi
fi

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis is not running. Starting it..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew services start redis
    else
        sudo systemctl start redis
    fi
fi

# Start the backend
echo "🚀 Starting CloudMind backend..."
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
