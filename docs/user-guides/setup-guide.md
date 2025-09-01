# 🚀 CloudMind Setup Guide

## Overview

CloudMind is now a **world-class, professional-grade cloud engineering platform** with real data, comprehensive AI insights, and enterprise-ready features. This guide will help you set up the complete environment.

## 🎯 What's New (Professional Features)

### ✅ **Real Data Integration**
- **No more mock data** - All dashboards now use real API calls
- **Comprehensive database** with realistic seed data
- **Professional authentication** with JWT tokens
- **Real-time data fetching** with React Query

### ✅ **Advanced AI Engine**
- **Local AI processing** - No external API dependencies
- **Intelligent cost analysis** with pattern recognition
- **Security insights** with vulnerability analysis
- **Performance optimization** recommendations
- **Resource utilization** analysis

### ✅ **Professional Frontend**
- **Real API integration** with proper error handling
- **Loading states** and user feedback
- **Authentication context** with persistent sessions
- **Data caching** and optimistic updates
- **Professional UI/UX** with modern components

### ✅ **Enterprise Backend**
- **Complete FastAPI application** with all endpoints
- **Database migrations** with Alembic
- **Comprehensive data seeding** with realistic data
- **Security middleware** with rate limiting
- **Professional logging** and monitoring

## 🛠️ Prerequisites

- **Docker & Docker Compose** (for database services)
- **Node.js 18+** (for frontend)
- **Python 3.11+** (for backend)
- **Git** (for version control)

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd cloudmind

# Run the automated setup script
./scripts/setup/setup.sh
```

This script will:
- ✅ Check all prerequisites
- ✅ Install dependencies
- ✅ Set up the database
- ✅ Run migrations
- ✅ Seed with realistic data
- ✅ Start all services
- ✅ Verify everything is working

### Option 2: Manual Setup

If you prefer manual setup, follow these steps:

#### 1. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit environment variables (optional)
nano .env
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

#### 3. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 4. Database Setup
```bash
# Start database services
docker-compose up -d postgres redis

# Run migrations
cd backend
source venv/bin/activate
alembic upgrade head

# Seed the database
python scripts/seed_data.py
```

#### 5. Start Services
```bash
# Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (in new terminal)
cd frontend
npm run dev
```

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/cloudmind

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Configuration
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_AI_API_KEY=your-google-key

# Cloud Providers
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AZURE_CLIENT_ID=your-azure-client-id
GCP_PROJECT_ID=your-gcp-project
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### End-to-End Tests
```bash
cd frontend
npm run test:e2e
```

## 🚀 Production Deployment

For production deployment, see the [Production Deployment Guide](../deployment/production.md).

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps
   
   # Restart database
   docker-compose restart postgres
   ```

2. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Kill the process
   kill -9 <PID>
   ```

3. **Frontend Build Errors**
   ```bash
   # Clear node modules and reinstall
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

## 📞 Support

- **Documentation**: [Complete Documentation Hub](../README.md)
- **Issues**: [GitHub Issues](https://github.com/cloudmind/issues)
- **Discussions**: [GitHub Discussions](https://github.com/cloudmind/discussions)

---

**CloudMind** - Making cloud management intelligent and effortless! 🚀
