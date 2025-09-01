#!/bin/bash

# 🚀 CloudMind Local Setup Script
# Perfect for single-user setup with 100% free storage and database

echo "🚀 Setting up CloudMind for local use (100% FREE)..."

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

# Check if running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_status "Detected OS: $OS"

# Install PostgreSQL
print_status "Installing PostgreSQL..."
if [ "$OS" = "macos" ]; then
    if ! command -v brew &> /dev/null; then
        print_error "Homebrew not found. Please install Homebrew first: https://brew.sh/"
        exit 1
    fi
    
    brew install postgresql
    brew services start postgresql
elif [ "$OS" = "linux" ]; then
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# Install Redis
print_status "Installing Redis..."
if [ "$OS" = "macos" ]; then
    brew install redis
    brew services start redis
elif [ "$OS" = "linux" ]; then
    sudo apt install -y redis-server
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
fi

# Create database and user
print_status "Setting up database..."
if [ "$OS" = "macos" ]; then
    createdb cloudmind 2>/dev/null || print_warning "Database 'cloudmind' already exists"
    psql cloudmind -c "CREATE USER cloudmind WITH PASSWORD 'cloudmind123';" 2>/dev/null || print_warning "User 'cloudmind' already exists"
    psql cloudmind -c "GRANT ALL PRIVILEGES ON DATABASE cloudmind TO cloudmind;" 2>/dev/null || print_warning "Privileges already granted"
elif [ "$OS" = "linux" ]; then
    sudo -u postgres createdb cloudmind 2>/dev/null || print_warning "Database 'cloudmind' already exists"
    sudo -u postgres psql -c "CREATE USER cloudmind WITH PASSWORD 'cloudmind123';" 2>/dev/null || print_warning "User 'cloudmind' already exists"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cloudmind TO cloudmind;" 2>/dev/null || print_warning "Privileges already granted"
fi

# Create storage directories
print_status "Creating storage directories..."
mkdir -p ./storage
mkdir -p ./git-repos
mkdir -p ./templates
mkdir -p ./backups
mkdir -p ./logs

# Set permissions
chmod 755 ./storage
chmod 755 ./git-repos
chmod 755 ./templates
chmod 755 ./backups
chmod 755 ./logs

# Create .env file
print_status "Creating environment configuration..."
cat > .env << EOF
# CloudMind Local Configuration (100% FREE)
# Database - Local PostgreSQL
DATABASE_URL=postgresql://cloudmind:cloudmind123@localhost:5432/cloudmind

# Redis - Local Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Storage - Local filesystem (unlimited, free)
STORAGE_TYPE=local
LOCAL_STORAGE_ENABLED=true
LOCAL_STORAGE_PATH=./storage
GIT_REPOSITORIES_PATH=./git-repos
TEMPLATE_STORAGE_PATH=./templates

# File thresholds
SMALL_FILE_THRESHOLD=1048576
LARGE_FILE_THRESHOLD=104857600

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100

# File Processing
MAX_FILE_SIZE=104857600
ALLOWED_FILE_TYPES=[".txt", ".md", ".json", ".yaml", ".yml", ".xml", ".csv", ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".scss", ".java", ".cpp", ".c", ".h", ".go", ".rs", ".php", ".rb", ".env", ".config", ".ini", ".toml", ".conf", ".pdf", ".doc", ".docx", ".rtf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".zip", ".tar", ".gz", ".rar", ".7z", ".sql", ".sh", ".bat", ".ps1"]

# Git Configuration
GIT_MAX_REPO_SIZE=1073741824
GIT_TIMEOUT=300

# Template Configuration
TEMPLATE_MAX_SIZE=52428800
TEMPLATE_MAX_FILES=1000

# Backup Configuration
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
BACKUP_SCHEDULE=0 2 * * *

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090

# Disable cloud storage (using local only)
CLOUDFLARE_R2_ENABLED=false
BACKBLAZE_B2_ENABLED=false
SUPABASE_STORAGE_ENABLED=false
EOF

print_success "Environment configuration created!"

# Install Python dependencies
print_status "Installing Python dependencies..."
cd backend
pip install -r requirements.txt

# Create additional requirements for local setup
cat > requirements_local.txt << EOF
# Additional dependencies for local setup
psycopg2-binary==2.9.7
redis==4.6.0
boto3==1.28.0
jinja2==3.1.2
pyyaml==6.0.1
gitpython==3.1.31
aiofiles==23.2.1
python-multipart==0.0.6
uvicorn[standard]==0.23.2
fastapi==0.103.1
pydantic==2.4.2
pydantic-settings==2.0.3
sqlalchemy==2.0.21
alembic==1.12.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
httpx==0.24.1
pytest==7.4.2
pytest-asyncio==0.21.1
EOF

pip install -r requirements_local.txt
cd ..

# Test database connection
print_status "Testing database connection..."
cd backend
python -c "
import psycopg2
try:
    conn = psycopg2.connect('postgresql://cloudmind:cloudmind123@localhost:5432/cloudmind')
    print('✅ Database connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
"

# Test Redis connection
print_status "Testing Redis connection..."
python -c "
import redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print('✅ Redis connection successful!')
except Exception as e:
    print(f'❌ Redis connection failed: {e}')
    exit(1)
"

cd ..

# Create startup script
print_status "Creating startup script..."
cat > start_cloudmind.sh << 'EOF'
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
EOF

chmod +x start_cloudmind.sh

# Create README for local setup
cat > README_LOCAL.md << 'EOF'
# 🚀 CloudMind Local Setup (100% FREE)

## ✅ Setup Complete!

Your CloudMind instance is now configured for local use with:
- **Database**: Local PostgreSQL (unlimited)
- **Storage**: Local filesystem (unlimited)
- **Cache**: Local Redis (unlimited)
- **Cost**: $0/month

## 🚀 Quick Start

1. **Start CloudMind**:
   ```bash
   ./start_cloudmind.sh
   ```

2. **Access the API**:
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

3. **Frontend** (when ready):
   ```bash
   cd frontend
   npm run dev
   ```

## 📁 Storage Locations

- **Files**: `./storage/`
- **Git Repos**: `./git-repos/`
- **Templates**: `./templates/`
- **Backups**: `./backups/`
- **Logs**: `./logs/`

## 🔧 Configuration

All configuration is in `.env` file. Key settings:
- `DATABASE_URL`: Local PostgreSQL
- `STORAGE_TYPE`: local
- `LOCAL_STORAGE_PATH`: ./storage

## 🛠️ Management

- **Start PostgreSQL**: `brew services start postgresql` (macOS) or `sudo systemctl start postgresql` (Linux)
- **Start Redis**: `brew services start redis` (macOS) or `sudo systemctl start redis-server` (Linux)
- **View Logs**: Check `./logs/` directory

## 💾 Backup

Your data is stored locally:
- Database: PostgreSQL data directory
- Files: `./storage/` directory
- Git repos: `./git-repos/` directory

## 🔒 Security

- All data stays on your machine
- No internet required for operation
- Complete privacy and control

## 🆓 Cost

- **Monthly Cost**: $0
- **Storage**: Unlimited (your disk space)
- **Bandwidth**: N/A (local only)
- **API Calls**: Unlimited

Enjoy your free, unlimited CloudMind instance! 🚀
EOF

print_success "Setup complete! 🎉"
print_success ""
print_success "📋 Summary:"
print_success "✅ PostgreSQL installed and configured"
print_success "✅ Redis installed and configured"
print_success "✅ Storage directories created"
print_success "✅ Environment configuration created"
print_success "✅ Python dependencies installed"
print_success "✅ Database connection tested"
print_success "✅ Redis connection tested"
print_success "✅ Startup script created"
print_success ""
print_success "🚀 To start CloudMind:"
print_success "   ./start_cloudmind.sh"
print_success ""
print_success "📖 Read README_LOCAL.md for more information"
print_success ""
print_success "💰 Cost: $0/month (100% FREE!)"
print_success "💾 Storage: Unlimited (your disk space)"
print_success "🔒 Privacy: All data stays on your machine"
