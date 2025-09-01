#!/bin/bash

# Comprehensive Test Suite for CloudMind
# This script provides various testing options for the project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    log "Checking requirements..."
    
    local missing_tools=()
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        missing_tools+=("python3")
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        missing_tools+=("node")
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        missing_tools+=("npm")
    fi
    
    # Check Docker (optional)
    if ! command -v docker &> /dev/null; then
        warning "Docker not found - Docker tests will be skipped"
    fi
    
    # Check k6 (optional)
    if ! command -v k6 &> /dev/null; then
        warning "k6 not found - Load tests will be skipped"
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi
    
    success "All required tools are available"
}

# Setup Python environment
setup_python_env() {
    log "Setting up Python environment..."
    
    cd "$PROJECT_ROOT/backend"
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        log "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install requirements
    log "Installing Python dependencies..."
    pip install -r requirements.txt
    
    success "Python environment ready"
}

# Setup Node.js environment
setup_node_env() {
    log "Setting up Node.js environment..."
    
    cd "$PROJECT_ROOT/frontend"
    
    # Install dependencies
    log "Installing Node.js dependencies..."
    npm install
    
    success "Node.js environment ready"
}

# Run quick tests
run_quick_tests() {
    log "Running quick tests..."
    
    cd "$PROJECT_ROOT"
    python3 scripts/run_quick_tests.py
}

# Run comprehensive tests
run_comprehensive_tests() {
    log "Running comprehensive tests..."
    
    cd "$PROJECT_ROOT"
    
    local args=""
    
    if [ "$1" = "--stress" ]; then
        args="--include-stress"
    elif [ "$1" = "--chaos" ]; then
        args="--include-chaos"
    elif [ "$1" = "--load" ]; then
        args="--include-load"
    elif [ "$1" = "--security" ]; then
        args="--include-security-scan"
    elif [ "$1" = "--performance" ]; then
        args="--include-performance"
    elif [ "$1" = "--all" ]; then
        args="--include-stress --include-chaos --include-load --include-security-scan --include-performance"
    fi
    
    python3 scripts/run_all_tests.py $args
}

# Run specific test type
run_specific_test() {
    local test_type="$1"
    
    log "Running $test_type tests..."
    
    cd "$PROJECT_ROOT"
    python3 scripts/run_all_tests.py --test-type "$test_type"
}

# Run backend tests only
run_backend_tests() {
    log "Running backend tests only..."
    
    cd "$PROJECT_ROOT/backend"
    source venv/bin/activate
    
    # Run pytest with coverage
    python -m pytest tests/ -v --cov=app --cov-report=html:coverage_html --cov-report=term-missing
}

# Run frontend tests only
run_frontend_tests() {
    log "Running frontend tests only..."
    
    cd "$PROJECT_ROOT/frontend"
    
    # Run Jest tests
    npm test -- --coverage --watchAll=false
    
    # Run type checking
    npm run type-check
    
    # Run linting
    npm run lint
    
    # Test build
    npm run build
}

# Run security tests
run_security_tests() {
    log "Running security tests..."
    
    cd "$PROJECT_ROOT"
    
    # Run security vulnerability assessment
    if [ -f "scripts/security/vulnerability_assessment.py" ]; then
        python3 scripts/security/vulnerability_assessment.py
    else
        warning "Security assessment script not found"
    fi
    
    # Run security tests
    cd backend
    source venv/bin/activate
    python -m pytest tests/test_security.py -v
}

# Run performance tests
run_performance_tests() {
    log "Running performance tests..."
    
    cd "$PROJECT_ROOT"
    
    # Run k6 load tests if available
    if command -v k6 &> /dev/null; then
        k6 run backend/tests/k6_load_test.js
    else
        warning "k6 not found - skipping load tests"
    fi
    
    # Run performance tests
    if [ -f "scripts/testing/performance_test.py" ]; then
        python3 scripts/testing/performance_test.py
    else
        warning "Performance test script not found"
    fi
}

# Run Docker tests
run_docker_tests() {
    log "Running Docker tests..."
    
    cd "$PROJECT_ROOT"
    
    if ! command -v docker &> /dev/null; then
        error "Docker not found"
        return 1
    fi
    
    # Test backend Docker build
    log "Testing backend Docker build..."
    docker build -t cloudmind-backend-test backend/
    
    # Test frontend Docker build
    log "Testing frontend Docker build..."
    docker build -t cloudmind-frontend-test frontend/
    
    # Clean up test images
    docker rmi cloudmind-backend-test cloudmind-frontend-test 2>/dev/null || true
    
    success "Docker tests completed"
}

# Run database tests
run_database_tests() {
    log "Running database tests..."
    
    cd "$PROJECT_ROOT/backend"
    source venv/bin/activate
    
    # Test migrations
    python -m alembic upgrade head
    
    success "Database tests completed"
}

# Show test coverage
show_coverage() {
    log "Generating test coverage report..."
    
    cd "$PROJECT_ROOT"
    
    # Backend coverage
    if [ -d "backend/coverage_html" ]; then
        log "Backend coverage report available at: backend/coverage_html/index.html"
    fi
    
    # Frontend coverage
    if [ -d "frontend/coverage" ]; then
        log "Frontend coverage report available at: frontend/coverage/lcov-report/index.html"
    fi
}

# Clean up test artifacts
cleanup() {
    log "Cleaning up test artifacts..."
    
    cd "$PROJECT_ROOT"
    
    # Remove coverage reports
    rm -rf backend/coverage_html
    rm -rf frontend/coverage
    
    # Remove test reports
    rm -f test_report_*.json
    rm -f test_results.log
    
    # Remove Docker test images
    docker rmi cloudmind-backend-test cloudmind-frontend-test 2>/dev/null || true
    
    success "Cleanup completed"
}

# Show help
show_help() {
    echo -e "${CYAN}CloudMind Test Suite${NC}"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  quick                    Run quick essential tests"
    echo "  comprehensive [OPTION]   Run comprehensive tests"
    echo "  backend                  Run backend tests only"
    echo "  frontend                 Run frontend tests only"
    echo "  security                 Run security tests"
    echo "  performance              Run performance tests"
    echo "  docker                   Run Docker build tests"
    echo "  database                 Run database migration tests"
    echo "  coverage                 Show test coverage"
    echo "  cleanup                  Clean up test artifacts"
    echo "  setup                    Setup testing environment"
    echo "  help                     Show this help message"
    echo ""
    echo "Comprehensive test options:"
    echo "  --stress                 Include stress tests"
    echo "  --chaos                  Include chaos engineering tests"
    echo "  --load                   Include load tests"
    echo "  --security               Include security vulnerability scan"
    echo "  --performance            Include performance tests"
    echo "  --all                    Include all optional tests"
    echo ""
    echo "Examples:"
    echo "  $0 quick                 # Run quick tests"
    echo "  $0 comprehensive --all   # Run all tests"
    echo "  $0 backend               # Run backend tests only"
    echo "  $0 security              # Run security tests"
}

# Main function
main() {
    case "${1:-help}" in
        "quick")
            check_requirements
            setup_python_env
            setup_node_env
            run_quick_tests
            ;;
        "comprehensive")
            check_requirements
            setup_python_env
            setup_node_env
            run_comprehensive_tests "$2"
            ;;
        "backend")
            check_requirements
            setup_python_env
            run_backend_tests
            ;;
        "frontend")
            check_requirements
            setup_node_env
            run_frontend_tests
            ;;
        "security")
            check_requirements
            setup_python_env
            run_security_tests
            ;;
        "performance")
            check_requirements
            setup_python_env
            run_performance_tests
            ;;
        "docker")
            run_docker_tests
            ;;
        "database")
            check_requirements
            setup_python_env
            run_database_tests
            ;;
        "coverage")
            show_coverage
            ;;
        "cleanup")
            cleanup
            ;;
        "setup")
            check_requirements
            setup_python_env
            setup_node_env
            success "Testing environment setup complete"
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
