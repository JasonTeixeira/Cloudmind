# 📖 **CloudMind API Documentation**

Complete API reference for CloudMind's REST API.

## 🚀 **Quick Start**

### **Base URL**
```
Production: https://api.cloudmind.com
Development: http://localhost:8000
```

### **Authentication**
All API requests require authentication using JWT tokens:

```bash
# Include in request headers
Authorization: Bearer <your-jwt-token>
```

### **Content Type**
All requests should use JSON:
```bash
Content-Type: application/json
```

## 🔐 **Authentication**

### **Register User**
```http
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "id": "user_123",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### **Login**
```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

## ☁️ **Cloud Management**

### **Scan Cloud Resources**
```http
POST /api/v1/cloud/scan
```

**Request Body:**
```json
{
  "providers": ["aws", "azure"],
  "scan_type": "comprehensive",
  "regions": ["us-east-1", "us-west-2"]
}
```

**Response:**
```json
{
  "scan_id": "scan_456",
  "status": "completed",
  "resources": [
    {
      "id": "i-1234567890abcdef0",
      "type": "ec2_instance",
      "provider": "aws",
      "region": "us-east-1",
      "instance_type": "t3.micro",
      "state": "running",
      "cost_per_month": 8.47
    }
  ],
  "total_cost": 1250.75,
  "scan_duration": 45.2
}
```

### **Get Cost Analysis**
```http
GET /api/v1/cloud/costs
```

**Query Parameters:**
- `provider` (optional): Filter by cloud provider
- `region` (optional): Filter by region
- `timeframe` (optional): Cost timeframe (daily, weekly, monthly)

**Response:**
```json
{
  "total_cost": 1250.75,
  "cost_by_service": {
    "ec2": 450.25,
    "rds": 300.50,
    "s3": 200.00,
    "lambda": 300.00
  },
  "cost_by_region": {
    "us-east-1": 800.25,
    "us-west-2": 450.50
  },
  "trends": {
    "daily": [1200, 1250, 1300, 1250],
    "weekly": [8500, 8750, 9000],
    "monthly": [35000, 37500]
  }
}
```

### **Get Optimization Recommendations**
```http
GET /api/v1/cloud/optimizations
```

**Response:**
```json
{
  "recommendations": [
    {
      "id": "opt_789",
      "type": "cost_optimization",
      "title": "Resize EC2 Instances",
      "description": "Downsize t3.large instances to t3.medium",
      "potential_savings": 150.00,
      "impact": "low",
      "effort": "medium"
    },
    {
      "id": "opt_790",
      "type": "performance_optimization",
      "title": "Enable Auto Scaling",
      "description": "Implement auto scaling for better performance",
      "potential_savings": 75.00,
      "impact": "high",
      "effort": "high"
    }
  ],
  "total_potential_savings": 225.00
}
```

## 🤖 **AI Analysis**

### **Get AI Insights**
```http
POST /api/v1/ai/analyze
```

**Request Body:**
```json
{
  "analysis_type": "cost_optimization",
  "data": {
    "resources": [...],
    "costs": {...},
    "usage_patterns": {...}
  },
  "providers": ["openai", "anthropic"]
}
```

**Response:**
```json
{
  "analysis_id": "ai_123",
  "insights": [
    {
      "type": "cost_optimization",
      "title": "Unused Resources Detected",
      "description": "Found 5 unused EBS volumes costing $25/month",
      "confidence": 0.95,
      "recommendations": [
        "Delete unused EBS volumes",
        "Implement automated cleanup"
      ]
    }
  ],
  "confidence_score": 0.92,
  "provider": "openai",
  "processing_time": 2.5
}
```

### **Get AI Predictions**
```http
POST /api/v1/ai/predict
```

**Request Body:**
```json
{
  "prediction_type": "cost_forecast",
  "timeframe": "3_months",
  "historical_data": [...]
}
```

**Response:**
```json
{
  "prediction_id": "pred_456",
  "forecast": {
    "next_month": 1350.00,
    "next_quarter": 4200.00,
    "next_year": 16800.00
  },
  "confidence_intervals": {
    "next_month": [1300, 1400],
    "next_quarter": [4000, 4400],
    "next_year": [16000, 17600]
  },
  "factors": [
    "Seasonal usage patterns",
    "Planned infrastructure changes",
    "Market price fluctuations"
  ]
}
```

## 🔒 **Security**

### **Get Security Scan Results**
```http
GET /api/v1/security/scan
```

**Response:**
```json
{
  "scan_id": "sec_789",
  "status": "completed",
  "findings": [
    {
      "id": "finding_123",
      "severity": "high",
      "title": "Public S3 Bucket",
      "description": "S3 bucket 'my-bucket' is publicly accessible",
      "resource": "arn:aws:s3:::my-bucket",
      "recommendation": "Remove public access and use IAM policies"
    }
  ],
  "summary": {
    "total_findings": 15,
    "high_severity": 3,
    "medium_severity": 8,
    "low_severity": 4
  }
}
```

### **Get Compliance Report**
```http
GET /api/v1/security/compliance
```

**Query Parameters:**
- `framework` (optional): Compliance framework (SOC2, HIPAA, GDPR, PCI-DSS)

**Response:**
```json
{
  "framework": "SOC2",
  "status": "compliant",
  "score": 95.5,
  "controls": [
    {
      "id": "CC6.1",
      "name": "Logical Access Security",
      "status": "compliant",
      "description": "Access to systems is restricted to authorized personnel"
    }
  ],
  "last_updated": "2024-01-01T00:00:00Z"
}
```

## 📊 **Monitoring**

### **Get System Health**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0",
  "environment": "production",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "security": "healthy"
  }
}
```

### **Get Metrics**
```http
GET /metrics
```

**Response:**
```
# Prometheus format metrics
http_requests_total{method="GET",endpoint="/api/v1/cloud/costs"} 1250
http_request_duration_seconds{method="POST",endpoint="/api/v1/ai/analyze"} 2.5
database_queries_total{operation="select"} 5000
ai_requests_total{provider="openai",model="gpt-4"} 150
```

## 🔧 **Error Handling**

### **Error Response Format**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email",
      "constraint": "must be valid email format"
    }
  },
  "timestamp": "2024-01-01T00:00:00Z",
  "request_id": "req_123"
}
```

### **Common Error Codes**
- `AUTHENTICATION_ERROR`: Invalid or missing authentication
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `VALIDATION_ERROR`: Invalid request data
- `RESOURCE_NOT_FOUND`: Requested resource not found
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_SERVER_ERROR`: Server error

## 📈 **Rate Limiting**

### **Rate Limits**
- **Authentication endpoints**: 5 requests per minute
- **API endpoints**: 1000 requests per minute
- **AI analysis**: 10 requests per minute
- **Cloud scanning**: 5 requests per minute

### **Rate Limit Headers**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## 📚 **SDK Examples**

### **Python SDK**
```python
from cloudmind import CloudMindClient

client = CloudMindClient(api_key="your-api-key")

# Scan cloud resources
scan_result = client.cloud.scan(providers=["aws", "azure"])

# Get cost analysis
costs = client.cloud.get_costs(timeframe="monthly")

# Get AI insights
insights = client.ai.analyze(
    analysis_type="cost_optimization",
    data=scan_result
)
```

### **JavaScript SDK**
```javascript
import { CloudMindClient } from '@cloudmind/sdk';

const client = new CloudMindClient({ apiKey: 'your-api-key' });

// Scan cloud resources
const scanResult = await client.cloud.scan({
  providers: ['aws', 'azure']
});

// Get cost analysis
const costs = await client.cloud.getCosts({
  timeframe: 'monthly'
});

// Get AI insights
const insights = await client.ai.analyze({
  analysisType: 'cost_optimization',
  data: scanResult
});
```

## 🔗 **Webhooks**

### **Webhook Events**
- `cloud.scan.completed`: Cloud scan completed
- `ai.analysis.completed`: AI analysis completed
- `security.alert.triggered`: Security alert triggered
- `cost.threshold.exceeded`: Cost threshold exceeded

### **Webhook Payload**
```json
{
  "event": "cloud.scan.completed",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "scan_id": "scan_123",
    "resources_found": 150,
    "total_cost": 1250.75
  }
}
```

## 📚 **Additional Resources**

- **[Authentication Guide](authentication.md)** - Detailed authentication documentation
- **[Error Codes](errors.md)** - Complete error code reference
- **[Rate Limiting](rate-limiting.md)** - Rate limiting details
- **[Webhooks](webhooks.md)** - Webhook configuration and events

## 🆘 **Support**

- **API Status**: [Status Page](https://status.cloudmind.com)
- **Documentation**: [Complete Documentation Hub](../README.md)
- **Support**: [Support Guide](../user-guides/support.md)
- **Issues**: [GitHub Issues](https://github.com/cloudmind/issues)

---

*For SDK documentation, see [SDK Documentation](sdk.md)* 