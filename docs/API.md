# 🔌 CloudMind API Documentation

## Overview

The CloudMind API is a comprehensive RESTful API that provides access to all platform capabilities including cost optimization, security analysis, AI-powered insights, and infrastructure management.

## Base URL

```
Development: http://localhost:8000
Production:  https://api.cloudmind.io
```

## Authentication

CloudMind uses JWT-based authentication with refresh tokens.

### Authentication Flow

```bash
# 1. Login to get tokens
POST /api/v1/auth/login
{
  "email": "user@company.com",
  "password": "secure_password"
}

# Response
{
  "access_token": "eyJ0eXAiOiJKV1Q...",
  "refresh_token": "eyJ0eXAiOiJKV1Q...",
  "token_type": "bearer",
  "expires_in": 900
}

# 2. Use access token in requests
Authorization: Bearer eyJ0eXAiOiJKV1Q...

# 3. Refresh when needed
POST /api/v1/auth/refresh
Authorization: Bearer <refresh_token>
```

## API Endpoints

### 🤖 AI & Analytics

#### Chat with AI Assistant
```bash
POST /api/v1/ai/chat
{
  "message": "Analyze my cloud costs and suggest optimizations",
  "context": "cost_optimization",
  "provider": "openai"
}
```

#### Get AI Recommendations
```bash
GET /api/v1/ai/recommendations?type=cost&provider=aws
```

#### Analyze Infrastructure
```bash
POST /api/v1/ai/analyze
{
  "resource_type": "ec2_instances",
  "time_range": "30d",
  "analysis_type": "optimization"
}
```

### 💰 Cost Management

#### Cost Summary
```bash
GET /api/v1/costs/summary?period=30d&provider=all
```

#### Cost Trends
```bash
GET /api/v1/costs/trends/monthly?months=12
```

#### Cost Optimization
```bash
POST /api/v1/costs/optimize
{
  "provider": "aws",
  "service": "ec2",
  "optimization_level": "aggressive"
}
```

#### Budget Management
```bash
GET /api/v1/costs/budgets
POST /api/v1/costs/budgets
PUT /api/v1/costs/budgets/{budget_id}
DELETE /api/v1/costs/budgets/{budget_id}
```

### 🔒 Security

#### Vulnerability Scan
```bash
POST /api/v1/security/scan
{
  "targets": ["aws_account_123", "azure_subscription_456"],
  "scan_type": "comprehensive",
  "priority": "high"
}
```

#### Get Vulnerabilities
```bash
GET /api/v1/security/vulnerabilities?severity=high&status=open
```

#### Compliance Check
```bash
GET /api/v1/security/compliance/cis?provider=aws
```

#### Security Recommendations
```bash
GET /api/v1/security/recommendations?provider=azure&category=access
```

### 🏗️ Infrastructure

#### Resource Inventory
```bash
GET /api/v1/infrastructure/resources?provider=all&type=compute
```

#### Infrastructure Topology
```bash
GET /api/v1/infrastructure/topology/{account_id}
```

#### Infrastructure as Code
```bash
POST /api/v1/infrastructure/generate-iac
{
  "resources": ["subnet-123", "instance-456"],
  "format": "terraform",
  "provider": "aws"
}
```

### 📊 Reporting

#### Generate Report
```bash
POST /api/v1/reports/generate
{
  "type": "cost_analysis",
  "period": "monthly",
  "format": "pdf",
  "recipients": ["manager@company.com"]
}
```

#### Dashboard Metrics
```bash
GET /api/v1/dashboard/metrics?dashboard=executive&period=30d
```

### 👥 User Management

#### User Profile
```bash
GET /api/v1/users/me
PUT /api/v1/users/me
```

#### Organizations
```bash
GET /api/v1/organizations
POST /api/v1/organizations
PUT /api/v1/organizations/{org_id}
```

#### Teams
```bash
GET /api/v1/teams
POST /api/v1/teams
PUT /api/v1/teams/{team_id}
DELETE /api/v1/teams/{team_id}
```

## Response Format

### Success Response

```json
{
  "success": true,
  "data": {
    // Response data
  },
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_123456789",
    "api_version": "1.0.0"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "provider",
      "issue": "Must be one of: aws, azure, gcp"
    }
  },
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

## Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid request |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

## Rate Limiting

CloudMind implements intelligent rate limiting:

- **Default**: 60 requests/minute per user
- **Burst**: Up to 10 requests in quick succession
- **Enterprise**: Custom limits available

Rate limit headers:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642234567
```

## Pagination

Large result sets are paginated:

```bash
GET /api/v1/resources?page=1&size=50&sort=created_date&order=desc
```

Response includes pagination metadata:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "size": 50,
    "total": 1250,
    "total_pages": 25,
    "has_next": true,
    "has_prev": false
  }
}
```

## Filtering and Sorting

### Filtering
```bash
GET /api/v1/costs?provider=aws&service=ec2&date_from=2024-01-01&date_to=2024-01-31
```

### Sorting
```bash
GET /api/v1/vulnerabilities?sort=severity,-created_date&size=20
```

### Field Selection
```bash
GET /api/v1/resources?fields=id,name,cost,provider&size=100
```

## Webhooks

CloudMind supports webhooks for real-time notifications:

### Webhook Events

- `cost.anomaly.detected`
- `security.vulnerability.found`
- `infrastructure.resource.created`
- `ai.analysis.completed`

### Webhook Configuration

```bash
POST /api/v1/webhooks
{
  "url": "https://your-app.com/webhooks/cloudmind",
  "events": ["cost.anomaly.detected", "security.vulnerability.found"],
  "secret": "your_webhook_secret"
}
```

### Webhook Payload

```json
{
  "event": "cost.anomaly.detected",
  "data": {
    "account_id": "aws_account_123",
    "anomaly_type": "spike",
    "amount": 1250.00,
    "threshold": 800.00,
    "service": "ec2"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "webhook_id": "webhook_789"
}
```

## SDK Examples

### Python SDK

```python
from cloudmind import CloudMindClient

client = CloudMindClient(
    api_key="your_api_key",
    base_url="https://api.cloudmind.io"
)

# Get cost summary
costs = client.costs.get_summary(period="30d")

# Run security scan
scan = client.security.scan(
    targets=["aws_account_123"],
    scan_type="comprehensive"
)

# Get AI recommendations
recommendations = client.ai.get_recommendations(
    type="cost",
    provider="aws"
)
```

### JavaScript/TypeScript SDK

```typescript
import { CloudMindClient } from '@cloudmind/sdk';

const client = new CloudMindClient({
  apiKey: 'your_api_key',
  baseUrl: 'https://api.cloudmind.io'
});

// Get cost summary
const costs = await client.costs.getSummary({ period: '30d' });

// Run security scan
const scan = await client.security.scan({
  targets: ['aws_account_123'],
  scanType: 'comprehensive'
});

// Get AI recommendations
const recommendations = await client.ai.getRecommendations({
  type: 'cost',
  provider: 'aws'
});
```

## Error Handling

### Common Error Codes

| Code | Meaning |
|------|---------|
| `AUTHENTICATION_REQUIRED` | Valid authentication token required |
| `INSUFFICIENT_PERMISSIONS` | User lacks required permissions |
| `VALIDATION_ERROR` | Request validation failed |
| `RESOURCE_NOT_FOUND` | Requested resource does not exist |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `EXTERNAL_API_ERROR` | Error from external service (AWS, etc.) |
| `PROCESSING_ERROR` | Error during request processing |

### Error Handling Best Practices

1. **Always check the `success` field**
2. **Use the `request_id` for support**
3. **Implement exponential backoff for rate limits**
4. **Handle network errors gracefully**
5. **Log errors with correlation IDs**

## Testing

### API Testing Tools

CloudMind provides several tools for API testing:

1. **Interactive Swagger UI**: http://localhost:8000/docs
2. **Postman Collection**: Available in `/docs/api/postman/`
3. **Test Suite**: Run with `make test-api`

### Example Test Cases

```bash
# Health check
GET /health

# Authentication test
POST /api/v1/auth/login

# Cost API test
GET /api/v1/costs/summary

# Security API test
POST /api/v1/security/scan
```

## Support

- **📚 Documentation**: https://docs.cloudmind.io
- **💬 Community**: https://github.com/JasonTeixeira/Cloudmind/discussions
- **🐛 Issues**: https://github.com/JasonTeixeira/Cloudmind/issues
- **📧 Support**: api-support@cloudmind.io
