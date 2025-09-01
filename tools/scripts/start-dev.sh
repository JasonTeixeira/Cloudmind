#!/bin/bash
set -e

# CloudMind Development Server Starter
# This script starts both backend and frontend in development mode

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to cleanup background processes
cleanup() {
    print_info "Shutting down services..."
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}

# Trap to cleanup on script exit
trap cleanup EXIT INT TERM

echo "🚀 Starting CloudMind Development Environment"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the CloudMind root directory"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    print_warning "No .env file found. Creating from development template..."
    if [ -f ".env.development" ]; then
        cp .env.development .env
        print_status "Created .env from development template"
    else
        print_error ".env.development template not found!"
        exit 1
    fi
fi

# Check services
print_info "Checking required services..."

# Check PostgreSQL
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    print_status "PostgreSQL is running"
else
    print_error "PostgreSQL is not running. Please start it first:"
    echo "  macOS: brew services start postgresql"
    echo "  Ubuntu: sudo systemctl start postgresql"
    exit 1
fi

# Check Redis
if redis-cli ping > /dev/null 2>&1; then
    print_status "Redis is running"
else
    print_error "Redis is not running. Please start it first:"
    echo "  macOS: brew services start redis"
    echo "  Ubuntu: sudo systemctl start redis"
    exit 1
fi

# Start Backend
print_info "Starting backend server..."
cd backend

if [ ! -d "venv" ]; then
    print_error "Virtual environment not found. Please run setup-dev.sh first"
    exit 1
fi

source venv/bin/activate

# Install any missing dependencies
pip install -q -r requirements.txt

# Start backend in background
print_status "Backend starting on http://localhost:8000"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!

cd ..

# Start Frontend
print_info "Starting frontend server..."
cd frontend

# Install any missing dependencies
npm install --silent

# Start frontend in background
print_status "Frontend starting on http://localhost:3000"
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!

cd ..

# Wait for services to start
print_info "Waiting for services to initialize..."
sleep 10

# Check if services are running
BACKEND_RUNNING=false
FRONTEND_RUNNING=false

if curl -s http://localhost:8000/docs > /dev/null 2>&1 || curl -s http://localhost:8000/ > /dev/null 2>&1; then
    BACKEND_RUNNING=true
    print_status "Backend is ready: http://localhost:8000"
else
    print_warning "Backend is still starting up..."
fi

if curl -s http://localhost:3000 > /dev/null 2>&1; then
    FRONTEND_RUNNING=true
    print_status "Frontend is ready: http://localhost:3000"
else
    print_warning "Frontend is still starting up..."
fi

echo ""
echo "🎉 CloudMind Development Environment"
echo "===================================="
echo "🌐 Frontend:    http://localhost:3000"
echo "🔌 Backend:     http://localhost:8000"
echo "📚 API Docs:    http://localhost:8000/docs"
echo ""
echo "📋 Logs:"
echo "   Backend:  tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep the script running and show live status
while true do
    sleep 30
    
    # Check service health
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        print_error "Backend process died!"
        break
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        print_error "Frontend process died!"
        break
    fi
    
    print_info "Services running normally..."
done


