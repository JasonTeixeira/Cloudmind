# 🔧 **CloudMind Development Guide**

Complete guide for developers working on CloudMind.

## 🎯 **Overview**

CloudMind is built with modern technologies and follows enterprise-grade development practices:

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Next.js (React/TypeScript)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Containerization**: Docker & Docker Compose
- **Monitoring**: Prometheus & Grafana

## 🚀 **Getting Started**

### **Prerequisites**
```bash
# Required software
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git
- PostgreSQL (for local development)
- Redis (for local development)
```

### **Development Setup**
```bash
# 1. Clone repository
git clone https://github.com/your-org/cloudmind.git
cd cloudmind

# 2. Set up backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Set up frontend
cd ../frontend
npm install

# 4. Configure environment
cp ../env.example .env.local
# Edit .env.local with your development settings
```

## 🏗️ **Project Architecture**

### **Backend Structure**
```
backend/
├── app/
│   ├── api/              # API endpoints
│   │   └── v1/          # API versioning
│   ├── core/            # Core functionality
│   │   ├── config.py    # Configuration management
│   │   ├── database.py  # Database connection
│   │   └── monitoring.py # Monitoring setup
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic services
│   │   ├── ai_engine/   # AI/ML services
│   │   ├── scanner/     # Cloud scanning services
│   │   └── ...          # Other services
│   └── middleware/      # Custom middleware
├── tests/               # Test suite
├── alembic/            # Database migrations
└── scripts/            # Development scripts
```

### **Frontend Structure**
```
frontend/
├── app/                # Next.js app directory
│   ├── (auth)/         # Authentication routes
│   ├── (dashboard)/    # Dashboard routes
│   └── globals.css     # Global styles
├── components/         # Reusable components
│   ├── ui/            # UI components
│   ├── layouts/       # Layout components
│   └── auth/          # Authentication components
├── lib/               # Utility libraries
│   ├── api/           # API client
│   ├── contexts/      # React contexts
│   └── utils.ts       # Utility functions
└── __tests__/         # Test files
```

## 🔧 **Development Workflow**

### **1. Code Standards**
```bash
# Backend (Python)
black .                    # Code formatting
isort .                    # Import sorting
flake8 .                   # Linting
mypy .                     # Type checking

# Frontend (TypeScript)
npm run lint              # ESLint
npm run type-check        # TypeScript checking
npm run format            # Prettier formatting
```

### **2. Testing**
```bash
# Backend tests
cd backend
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/test_api.py  # Run specific test file

# Frontend tests
cd frontend
npm test                  # Run tests
npm run test:watch        # Watch mode
npm run test:coverage     # Coverage report
```

### **3. Database Management**
```bash
# Create migration
cd backend
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### **4. Development Server**
```bash
# Backend development
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend development
cd frontend
npm run dev
```

## 📝 **Coding Guidelines**

### **Python (Backend)**
```python
# Use type hints
def process_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process data with proper documentation."""
    pass

# Use async/await for I/O operations
async def fetch_data() -> Dict[str, Any]:
    """Fetch data asynchronously."""
    pass

# Use Pydantic for data validation
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
```

### **TypeScript (Frontend)**
```typescript
// Use TypeScript interfaces
interface User {
  id: string;
  email: string;
  name: string;
}

// Use React hooks properly
const useUser = (): User | null => {
  const [user, setUser] = useState<User | null>(null);
  return user;
};

// Use proper error handling
try {
  const data = await api.getUser();
} catch (error) {
  console.error('Failed to fetch user:', error);
}
```

## 🧪 **Testing Guidelines**

### **Backend Testing**
```python
# Unit tests
def test_user_creation():
    """Test user creation functionality."""
    user_data = {"email": "test@example.com", "password": "password123"}
    user = create_user(user_data)
    assert user.email == user_data["email"]

# Integration tests
async def test_api_endpoint():
    """Test API endpoint integration."""
    async with TestClient(app) as client:
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
```

### **Frontend Testing**
```typescript
// Component tests
describe('UserProfile', () => {
  it('renders user information correctly', () => {
    render(<UserProfile user={mockUser} />);
    expect(screen.getByText(mockUser.name)).toBeInTheDocument();
  });
});

// API tests
describe('API Client', () => {
  it('handles authentication correctly', async () => {
    const token = await api.authenticate(credentials);
    expect(token).toBeDefined();
  });
});
```

## 🔒 **Security Guidelines**

### **Backend Security**
```python
# Always validate input
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    email: str
    
    @validator('email')
    def validate_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError('Invalid email format')
        return v

# Use proper authentication
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    # Validate JWT token
    pass
```

### **Frontend Security**
```typescript
// Sanitize user input
import DOMPurify from 'dompurify';

const sanitizedInput = DOMPurify.sanitize(userInput);

// Use secure storage
const secureStorage = {
  set: (key: string, value: string) => {
    sessionStorage.setItem(key, value);
  },
  get: (key: string) => {
    return sessionStorage.getItem(key);
  }
};
```

## 📊 **Performance Guidelines**

### **Backend Performance**
```python
# Use connection pooling
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)

# Use caching
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(data):
    # Cache expensive operations
    pass
```

### **Frontend Performance**
```typescript
// Use React.memo for expensive components
const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{processData(data)}</div>;
});

// Use proper loading states
const [isLoading, setIsLoading] = useState(false);
const [data, setData] = useState(null);

useEffect(() => {
  setIsLoading(true);
  fetchData().then(setData).finally(() => setIsLoading(false));
}, []);
```

## 🔄 **Git Workflow**

### **Branch Naming**
```bash
# Feature branches
feature/user-authentication
feature/cloud-scanning
feature/ai-integration

# Bug fixes
fix/database-connection
fix/api-endpoint-error

# Hotfixes
hotfix/security-vulnerability
hotfix/critical-bug
```

### **Commit Messages**
```bash
# Use conventional commits
feat: add user authentication system
fix: resolve database connection issue
docs: update API documentation
test: add unit tests for user service
refactor: improve code organization
```

## 📚 **Resources**

### **Documentation**
- **[API Documentation](../api/README.md)** - Complete API reference
- **[Architecture Overview](architecture.md)** - System architecture
- **[Testing Guide](testing.md)** - Testing best practices
- **[Deployment Guide](../deployment/README.md)** - Deployment procedures

### **Tools & Libraries**
- **[FastAPI Documentation](https://fastapi.tiangolo.com/)**
- **[Next.js Documentation](https://nextjs.org/docs)**
- **[SQLAlchemy Documentation](https://docs.sqlalchemy.org/)**
- **[Pydantic Documentation](https://pydantic-docs.helpmanual.io/)**

## 🆘 **Getting Help**

- **Issues**: [GitHub Issues](https://github.com/cloudmind/issues)
- **Discussions**: [GitHub Discussions](https://github.com/cloudmind/discussions)
- **Documentation**: [Complete Documentation Hub](../README.md)
- **Code Review**: Submit pull requests for review

---

*For architecture details, see [Architecture Overview](architecture.md)*
