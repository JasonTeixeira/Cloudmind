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

# Seed data
python -m app.scripts.seed_data
```

#### 5. Start All Services
```bash
docker-compose up -d
```

## 🌐 Access Points

Once setup is complete, you can access:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Grafana Dashboard**: http://localhost:3001

## 👤 Demo Credentials

Use these credentials to log in:

- **Email**: `demo@cloudmind.local`
- **Password**: `password123`

Additional demo users:
- `admin@cloudmind.local` / `password123` (Admin)
- `john.doe@acme.com` / `password123` (User)
- `sarah.smith@techcorp.com` / `password123` (User)

## 📊 What You'll See

### Dashboard Features
- **Real-time cost data** with trends and analysis
- **Security insights** with vulnerability tracking
- **Infrastructure monitoring** with resource utilization
- **AI-powered recommendations** for optimization
- **Professional charts** and visualizations

### Sample Data
The system comes pre-loaded with:
- **5 realistic projects** (E-commerce, Mobile App, Data Analytics, etc.)
- **6 months of cost data** with realistic variations
- **Security scans** with vulnerabilities and recommendations
- **Infrastructure resources** with utilization metrics
- **AI insights** with actionable recommendations

## 🔧 Development Commands

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run test         # Run tests
npm run lint         # Lint code
```

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload  # Start development server
pytest                          # Run tests
alembic revision --autogenerate # Create migration
alembic upgrade head            # Apply migrations
```

### Database Management
```bash
# View logs
docker-compose logs -f

# Reset database
docker-compose down
docker volume rm cloudmind_postgres_data
docker-compose up -d postgres redis
cd backend && source venv/bin/activate
alembic upgrade head
python -m app.scripts.seed_data

# Backup database
docker-compose exec postgres pg_dump -U cloudmind cloudmind > backup.sql
```

## 🏗️ Architecture Overview

### Frontend Stack
- **Next.js 14** with App Router
- **React 18** with concurrent features
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **React Query** for data fetching
- **Zustand** for state management

### Backend Stack
- **FastAPI** with async support
- **SQLAlchemy** ORM
- **PostgreSQL** with TimescaleDB
- **Redis** for caching
- **Alembic** for migrations
- **Pydantic** for validation

### AI/ML Features
- **Local AI processing** (no external APIs)
- **Cost pattern analysis**
- **Security vulnerability detection**
- **Resource optimization insights**
- **Performance recommendations**

## 🔒 Security Features

- **JWT authentication** with refresh tokens
- **Password hashing** with bcrypt
- **Rate limiting** middleware
- **Input validation** and sanitization
- **Security headers** (HSTS, CSP, XSS Protection)
- **CORS configuration**

## 📈 Monitoring & Observability

- **Prometheus** metrics collection
- **Grafana** dashboards
- **Structured logging** with correlation IDs
- **Health checks** for all services
- **Performance monitoring**

## 🚀 Production Deployment

For production deployment:

1. **Set up SSL certificates**
2. **Configure environment variables**
3. **Set up monitoring alerts**
4. **Configure automated backups**
5. **Set up CI/CD pipeline**

## 🐛 Troubleshooting

### Common Issues

**Frontend not loading:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Backend not starting:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Database connection issues:**
```bash
docker-compose down
docker-compose up -d postgres redis
# Wait 30 seconds, then try again
```

**Migration errors:**
```bash
cd backend
source venv/bin/activate
alembic stamp head
alembic upgrade head
```

## 📚 Next Steps

1. **Explore the dashboard** and see real data in action
2. **Try the AI insights** and recommendations
3. **Create new projects** and analyze costs
4. **Run security scans** and review vulnerabilities
5. **Customize the platform** for your needs

## 🎉 Congratulations!

You now have a **world-class cloud engineering platform** running locally with:

- ✅ **Real data integration** (no more mock data)
- ✅ **Professional AI insights** (local processing)
- ✅ **Enterprise security** (JWT, rate limiting, etc.)
- ✅ **Modern UI/UX** (Next.js, React, TypeScript)
- ✅ **Comprehensive monitoring** (Prometheus, Grafana)
- ✅ **Production-ready architecture** (Docker, migrations, etc.)

**CloudMind is now ready for professional use!** 🚀 