# CloudMind

**Cloud cost visibility + security scanning dashboard**

```
┌─────────────────────────────────────────────────┐
│  WHAT THIS IS                                   │
├─────────────────────────────────────────────────┤
│  • Multi-cloud cost tracking (AWS/Azure/GCP)   │
│  • Security vulnerability scanning             │
│  • Next.js 14 frontend + FastAPI backend       │
│  • OpenAI integration for cost recommendations │
│  • Ambitious side project, partially built     │
└─────────────────────────────────────────────────┘
```

## Why I Built This

I got tired of logging into three different cloud consoles to check costs. AWS Cost Explorer is clunky, Azure's billing portal is confusing, and GCP's UI is... fine, but I wanted everything in one place.

CloudMind started as a weekend project to aggregate cloud costs into a single dashboard. Then I got ambitious and added security scanning. Then I thought "what if I used OpenAI to recommend cost optimizations?" Then I added 3D infrastructure visualization because why not.

The result is an over-engineered dashboard that does some useful things (cost tracking, basic security scans) and some experimental things (AI recommendations, 3D topology maps that are cool but not that useful).

## Architecture

```
┌──────────────────┐
│   Next.js 14     │  TypeScript, Tailwind CSS
│   (Frontend)     │  Three.js for 3D visualizations
└────────┬─────────┘
         │ HTTP/WebSocket
         ▼
┌──────────────────┐
│   FastAPI        │  Python 3.11
│   (Backend)      │  Celery for async tasks
└────────┬─────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌──────────┐ ┌──────────┐
│PostgreSQL│ │  Redis   │
│+ TimescaleDB│ │  Cache   │
└──────────┘ └──────────┘
```

**External APIs:**
- AWS Cost Explorer API (cost data)
- Azure Billing API (cost data)
- GCP Cloud Billing API (cost data)
- OpenAI GPT-4 (cost optimization recommendations)
- AWS Security Hub, Azure Security Center (vulnerability scans)

## What's Inside

**Frontend (`/frontend`):**
- `app/(dashboard)/finops/` - Multi-cloud cost tracking page
- `app/(dashboard)/security/` - Security scan results dashboard
- `app/(dashboard)/projects/` - Cloud resource inventory
- `app/(dashboard)/auto-healing/` - Experimental self-healing infrastructure (mostly UI mockups)
- Three.js components for 3D infrastructure topology

**Backend (`/backend`):**
- `app/api/` - REST endpoints for cost data, security scans, AI recommendations
- `app/services/cloud/` - AWS/Azure/GCP SDK integrations
- `app/services/ai/` - OpenAI API wrapper for cost analysis
- `app/middleware/` - Rate limiting, auth, security headers
- Celery tasks for scheduled cost data collection

**Infrastructure:**
- `docker-compose.yml` - Local dev environment (PostgreSQL, Redis, Celery)
- `deployment/` - Kubernetes manifests (not tested in production)
- `infrastructure/terraform/` - Basic AWS/GCP deployment configs (incomplete)

## What Works

**Cloud cost tracking:** I successfully integrated AWS Cost Explorer and can pull daily cost data. Azure and GCP integrations are stubbed out (I return mock data because I don't use those clouds regularly).

**Security scanning:** Basic integration with AWS Security Hub. It pulls findings and displays them in a table. No remediation workflows yet.

**AI cost recommendations:** OpenAI analyzes spending patterns and suggests optimizations. It's hit-or-miss—sometimes it suggests obvious things like "use Reserved Instances," sometimes it hallucinates services that don't exist.

**Dashboard UI:** The frontend is responsive and looks professional. I'm proud of the design.

## What Doesn't Work

**3D infrastructure visualization:** I spent a week building a Three.js topology map where nodes represent cloud resources and edges represent relationships. It looks cool in demos but it's useless for actual infrastructure management. Too many nodes make it unreadable. I should've just used a force-directed graph.

**Multi-region support:** CloudMind assumes everything is in a single AWS region. Multi-region deployments don't display correctly.

**Auto-healing infrastructure:** The UI exists but there's no backend logic. It's vaporware. I had grand plans for automated incident response but never got there.

**GCP/Azure:** I only have AWS credentials, so the Azure and GCP integrations return mock data. They'd work if you have API keys, but I haven't tested them.

## What Was Hard

**Cost Explorer API rate limits:** AWS Cost Explorer has aggressive rate limits (1 request per 5 seconds). I had to add Redis caching and batch requests, which made the code messy. Real-time cost updates are basically impossible.

**TimescaleDB vs PostgreSQL:** I added TimescaleDB for time-series cost data, but setup was a pain. Had to create custom extensions, migrate schemas, and the Docker image is 1GB+. Not sure it was worth it over just using PostgreSQL with partitioning.

**OpenAI cost:** Running GPT-4 on every cost analysis request adds up fast. I burned through $50 in API credits in the first month. Switched to GPT-3.5-turbo for most queries, but the recommendations got worse.

**Three.js learning curve:** I'd never used Three.js before this project. The 3D visualization took way longer than expected (2 weeks vs. planned 2 days). Camera controls, lighting, performance optimization—all harder than I thought.

**Authentication complexity:** JWT auth + OAuth2 + RBAC = overengineered for a personal project. Should've just used Clerk or Auth0.

## What I'd Do Differently

**Skip the 3D visualization:** Use a boring but functional 2D network graph library like Cytoscape.js or vis.js.

**Use a managed service for auth:** Clerk, Auth0, or Supabase Auth instead of rolling my own JWT system.

**Focus on AWS only:** Supporting three cloud providers tripled the integration work. AWS-only would've been fine for my use case.

**Skip AI recommendations:** They sound cool but aren't that useful. A static checklist of cost optimization best practices would've been faster to implement and more reliable.

**Use a lighter DB:** PostgreSQL alone would've been fine. TimescaleDB added complexity without clear benefits at my data volume (~10k cost records/month).

## Quick Start

**Prerequisites:**
- Docker + Docker Compose
- AWS credentials with Cost Explorer + Security Hub access
- OpenAI API key (optional, for AI recommendations)

**Local development:**
```bash
git clone https://github.com/JasonTeixeira/Cloudmind.git
cd Cloudmind

# Copy environment template
cp env.example .env
# Edit .env with your AWS keys and OpenAI key

# Start infrastructure (Postgres, Redis, Celery)
docker-compose up -d

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:3000  
Backend API: http://localhost:8000/api/docs

## Current Status

**Active features:** AWS cost tracking, basic security scanning, dashboard UI  
**Experimental:** AI recommendations (works but expensive)  
**Not implemented:** GCP/Azure (mock data only), auto-healing, multi-region support, 3D visualization (built but useless)

I use this for my personal AWS account (~$100/month spend). The cost dashboard is actually useful for tracking spending over time. The security scanner is decent for quick vulnerability checks.

Wouldn't recommend deploying this for anything production-critical. It's a side project, not a product.

---

**Built with:** Next.js 14, FastAPI, PostgreSQL, TimescaleDB, Redis, OpenAI GPT-4  
**Started:** August 2024  
**Status:** Active personal use, experimental features
