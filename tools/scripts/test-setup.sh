#!/bin/bash
set -e

# CloudMind Setup Tester
# Tests all components before starting development

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

echo "🧪 CloudMind Setup Testing"
echo "=========================="

ERRORS=0

# Test 1: Python Environment
print_info "Testing Python environment..."
cd backend
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found"
    ((ERRORS++))
else
    source venv/bin/activate
    if python -c "import app.main" 2>/dev/null; then
        print_status "Backend imports successful"
    else
        print_error "Backend import failed"
        ((ERRORS++))
    fi
fi
cd ..

# Test 2: Frontend Environment  
print_info "Testing frontend environment..."
cd frontend
if [ -f "package.json" ] && [ -d "node_modules" ]; then
    if npm run build >/dev/null 2>&1; then
        print_status "Frontend build successful"
    else
        print_error "Frontend build failed"
        ((ERRORS++))
    fi
else
    print_error "Frontend dependencies not installed"
    ((ERRORS++))
fi
cd ..

# Test 3: Database Connection
print_info "Testing database connection..."
if pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
    print_status "PostgreSQL connection successful"
else
    print_error "PostgreSQL connection failed"
    ((ERRORS++))
fi

# Test 4: Redis Connection
print_info "Testing Redis connection..."
if redis-cli ping >/dev/null 2>&1; then
    print_status "Redis connection successful"
else
    print_error "Redis connection failed"
    ((ERRORS++))
fi

# Test 5: Environment Configuration
print_info "Testing environment configuration..."
if [ -f ".env" ]; then
    print_status "Environment file exists"
else
    print_error "Environment file missing"
    ((ERRORS++))
fi

# Summary
echo ""
if [ $ERRORS -eq 0 ]; then
    print_status "All tests passed! CloudMind is ready to start."
    echo ""
    echo "🚀 Start development with: ./tools/scripts/start-dev.sh"
    exit 0
else
    print_error "$ERRORS test(s) failed. Please fix the issues above."
    echo ""
    echo "🔧 Run setup with: ./tools/scripts/setup-dev.sh"
    exit 1
fi


