#!/bin/bash
set -e

echo "🚀 CloudMind Development Setup"
echo "==============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the CloudMind root directory"
    exit 1
fi

print_status "Starting CloudMind development setup..."

# 1. Environment Setup
print_status "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.development .env
    print_status "Created .env from development template"
else
    print_warning ".env already exists, skipping..."
fi

# 2. Backend Setup
print_status "Setting up backend environment..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Created Python virtual environment"
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements/dev.txt
print_status "Installed Python dependencies"

cd ..

# 3. Frontend Setup
print_status "Setting up frontend environment..."
cd frontend

# Install Node.js dependencies
npm install
print_status "Installed Node.js dependencies"

cd ..

# 4. Database Setup
print_status "Checking database requirements..."
if command -v pg_isready > /dev/null 2>&1; then
    if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
        print_status "PostgreSQL is running"
    else
        print_warning "PostgreSQL is not running. Please start it manually:"
        echo "  macOS: brew services start postgresql"
        echo "  Ubuntu: sudo systemctl start postgresql"
    fi
else
    print_warning "PostgreSQL not found. Please install it:"
    echo "  macOS: brew install postgresql"
    echo "  Ubuntu: sudo apt install postgresql"
fi

# 5. Redis Setup
print_status "Checking Redis requirements..."
if command -v redis-cli > /dev/null 2>&1; then
    if redis-cli ping > /dev/null 2>&1; then
        print_status "Redis is running"
    else
        print_warning "Redis is not running. Please start it manually:"
        echo "  macOS: brew services start redis"
        echo "  Ubuntu: sudo systemctl start redis"
    fi
else
    print_warning "Redis not found. Please install it:"
    echo "  macOS: brew install redis"
    echo "  Ubuntu: sudo apt install redis-server"
fi

# 6. Create necessary directories
print_status "Creating project directories..."
mkdir -p logs data backups temp

# 7. Set up git hooks (if git repo)
if [ -d ".git" ]; then
    print_status "Setting up git hooks..."
    cd backend
    source venv/bin/activate
    pre-commit install 2>/dev/null || print_warning "Pre-commit hooks setup skipped"
    cd ..
fi

print_status "Development setup complete!"
echo ""
echo "🎉 CloudMind is ready for development!"
echo ""
echo "Next steps:"
echo "1. Start the backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "2. Start the frontend: cd frontend && npm run dev"
echo "3. Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "For more information, see the README.md file."


