#!/bin/bash

# CloudMind Setup Script
# This script sets up the complete CloudMind environment

set -e

echo "🚀 CloudMind Setup Script"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    print_status "Checking Docker..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ and try again."
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.11+ and try again."
        exit 1
    fi
    
    print_success "All requirements are met"
}

# Setup environment file
setup_env() {
    print_status "Setting up environment file..."
    
    if [ ! -f .env ]; then
        cp env.example .env
        print_success "Created .env file from template"
    else
        print_warning ".env file already exists"
    fi
}

# Install frontend dependencies
install_frontend() {
    print_status "Installing frontend dependencies..."
    cd frontend
    
    if [ ! -d node_modules ]; then
        npm install
        print_success "Frontend dependencies installed"
    else
        print_warning "Frontend dependencies already installed"
    fi
    
    cd ..
}

# Install backend dependencies
install_backend() {
    print_status "Installing backend dependencies..."
    cd backend
    
    if [ ! -d venv ]; then
        python3 -m venv venv
        print_success "Created Python virtual environment"
    fi
    
    source venv/bin/activate
    pip install -r requirements.txt
    print_success "Backend dependencies installed"
    
    cd ..
}

# Start database services
start_database() {
    print_status "Starting database services..."
    
    # Start PostgreSQL and Redis
    docker-compose up -d postgres redis
    
    # Wait for PostgreSQL to be ready
    print_status "Waiting for PostgreSQL to be ready..."
    timeout=60
    counter=0
    while ! docker-compose exec -T postgres pg_isready -U cloudmind > /dev/null 2>&1; do
        sleep 1
        counter=$((counter + 1))
        if [ $counter -ge $timeout ]; then
            print_error "PostgreSQL failed to start within $timeout seconds"
            exit 1
        fi
    done
    print_success "PostgreSQL is ready"
}

# Run database migrations
run_migrations() {
    print_status "Running database migrations..."
    cd backend
    
    source venv/bin/activate
    
    # Initialize Alembic if not already done
    if [ ! -f alembic.ini ]; then
        alembic init alembic
        print_success "Initialized Alembic"
    fi
    
    # Run migrations
    alembic upgrade head
    print_success "Database migrations completed"
    
    cd ..
}

# Seed database with initial data
seed_database() {
    print_status "Seeding database with initial data..."
    cd backend
    
    source venv/bin/activate
    python -m app.scripts.seed_data
    
    print_success "Database seeded with initial data"
    cd ..
}

# Start all services
start_services() {
    print_status "Starting all services..."
    docker-compose up -d
    
    print_success "All services started"
}

# Check service health
check_health() {
    print_status "Checking service health..."
    
    # Wait a moment for services to start
    sleep 10
    
    # Check backend health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Backend is healthy"
    else
        print_warning "Backend health check failed"
    fi
    
    # Check frontend
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        print_success "Frontend is accessible"
    else
        print_warning "Frontend health check failed"
    fi
}

# Display final information
show_info() {
    echo ""
    echo "🎉 CloudMind Setup Complete!"
    echo "============================"
    echo ""
    echo "Services:"
    echo "  • Frontend: http://localhost:3000"
    echo "  • Backend API: http://localhost:8000"
    echo "  • API Documentation: http://localhost:8000/docs"
    echo "  • Grafana: http://localhost:3001"
    echo ""
    echo "Demo Credentials:"
    echo "  • Email: demo@cloudmind.local"
    echo "  • Password: password123"
    echo ""
    echo "Useful Commands:"
    echo "  • View logs: docker-compose logs -f"
    echo "  • Stop services: docker-compose down"
    echo "  • Restart services: docker-compose restart"
    echo "  • Update data: docker-compose exec backend python -m app.scripts.seed_data"
    echo ""
}

# Main setup function
main() {
    echo "Starting CloudMind setup..."
    echo ""
    
    check_docker
    check_requirements
    setup_env
    install_frontend
    install_backend
    start_database
    run_migrations
    seed_database
    start_services
    check_health
    show_info
}

# Run main function
main "$@" 