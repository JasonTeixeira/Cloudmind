# 🔑 **API Keys Setup Guide - CloudMind Configuration**

## 🎯 **Overview**

This guide will help you configure all the necessary API keys and external service integrations for CloudMind to function at full capacity.

## 🔧 **Required API Keys**

### **🤖 AI/ML Services**

#### **1. OpenAI API Key**
```bash
# Get your OpenAI API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Features enabled:**
- Cost optimization analysis
- Security vulnerability assessment
- Performance recommendations
- Natural language processing

#### **2. Anthropic Claude API Key**
```bash
# Get your Anthropic API key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
```

**Features enabled:**
- Advanced reasoning and analysis
- Complex problem solving
- Detailed explanations
- Alternative AI insights

#### **3. Google AI (Gemini) API Key**
```bash
# Get your Google AI API key from: https://makersuite.google.com/app/apikey
GOOGLE_AI_API_KEY=your-google-ai-api-key-here
```

**Features enabled:**
- Multi-modal analysis
- Code generation and review
- Technical documentation
- Google Cloud integration

#### **4. Ollama (Local AI) Configuration**
```bash
# For local AI processing (optional)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2:13b
```

**Features enabled:**
- Local AI processing
- Offline capabilities
- Privacy-focused analysis
- Custom model support

### **☁️ Cloud Provider APIs**

#### **1. AWS Configuration**
```bash
# Get your AWS credentials from: https://console.aws.amazon.com/iam/
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_DEFAULT_REGION=us-east-1
AWS_SESSION_TOKEN=your-session-token  # Optional, for temporary credentials
```

**Features enabled:**
- AWS resource monitoring
- Cost analysis and optimization
- Security scanning
- Infrastructure management

#### **2. Azure Configuration**
```bash
# Get your Azure credentials from: https://portal.azure.com/
AZURE_CLIENT_ID=your-azure-client-id
AZURE_CLIENT_SECRET=your-azure-client-secret
AZURE_TENANT_ID=your-azure-tenant-id
AZURE_SUBSCRIPTION_ID=your-azure-subscription-id
```

**Features enabled:**
- Azure resource monitoring
- Cost management
- Security assessment
- Resource optimization

#### **3. Google Cloud Platform (GCP)**
```bash
# Get your GCP credentials from: https://console.cloud.google.com/
GCP_PROJECT_ID=your-gcp-project-id
GCP_PRIVATE_KEY_ID=your-private-key-id
GCP_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
GCP_CLIENT_EMAIL=your-service-account@project.iam.gserviceaccount.com
GCP_CLIENT_ID=your-client-id
```

**Features enabled:**
- GCP resource monitoring
- Cost analysis
- Security scanning
- Performance optimization

### **🔍 Security & Monitoring**

#### **1. Sentry (Error Tracking)**
```bash
# Get your Sentry DSN from: https://sentry.io/
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

**Features enabled:**
- Error tracking and monitoring
- Performance monitoring
- Release tracking
- Issue management

#### **2. DataDog (Monitoring)**
```bash
# Get your DataDog API key from: https://app.datadoghq.com/
DATADOG_API_KEY=your-datadog-api-key
DATADOG_APP_KEY=your-datadog-app-key
```

**Features enabled:**
- Application performance monitoring
- Infrastructure monitoring
- Log aggregation
- Custom dashboards

## 🚀 **Quick Setup**

### **Option 1: Automated Setup**
```bash
# Run the automated setup script
./scripts/setup/setup_ai_keys.sh
```

This script will:
- ✅ Guide you through each API key setup
- ✅ Validate API keys
- ✅ Test connections
- ✅ Update your `.env` file
- ✅ Verify all integrations

### **Option 2: Manual Setup**

1. **Copy the environment template**
   ```bash
   cp env.example .env
   ```

2. **Edit the `.env` file**
   ```bash
   nano .env
   # Add your API keys to the appropriate variables
   ```

3. **Test the configuration**
   ```bash
   cd backend
   python scripts/test_connections.py
   ```

## 🔒 **Security Best Practices**

### **API Key Management**

#### **1. Environment Variables**
- ✅ Store API keys in environment variables
- ✅ Never commit API keys to version control
- ✅ Use `.env` files for local development
- ✅ Use secrets management in production

#### **2. Production Secrets**
```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
  --name cloudmind/api-keys \
  --secret-string '{"openai_key":"sk-...","anthropic_key":"sk-ant-..."}'

# Kubernetes Secrets
kubectl create secret generic cloudmind-api-keys \
  --from-literal=openai-key="sk-..." \
  --from-literal=anthropic-key="sk-ant-..."
```

#### **3. Key Rotation**
```bash
# Regular key rotation schedule
# - OpenAI: Every 90 days
# - Anthropic: Every 90 days
# - Google AI: Every 90 days
# - Cloud Provider keys: Every 60 days
```

### **Access Control**

#### **1. Principle of Least Privilege**
- ✅ Use service accounts with minimal permissions
- ✅ Enable API key restrictions where possible
- ✅ Monitor API usage and costs
- ✅ Set up billing alerts

#### **2. API Key Restrictions**
```bash
# OpenAI API key restrictions
# - Set usage limits
# - Restrict to specific IP addresses
# - Enable monitoring and alerts

# Cloud provider IAM policies
# - Read-only access for monitoring
# - Specific resource access
# - Cost management permissions
```

## 🧪 **Testing Your Configuration**

### **Connection Test Script**
```bash
cd backend
python scripts/test_connections.py
```

This will test:
- ✅ OpenAI API connectivity
- ✅ Anthropic API connectivity
- ✅ Google AI API connectivity
- ✅ AWS API connectivity
- ✅ Azure API connectivity
- ✅ GCP API connectivity
- ✅ Database connectivity
- ✅ Redis connectivity

### **Manual Testing**

#### **1. Test AI Services**
```bash
# Test OpenAI
curl -X POST "http://localhost:8000/api/v1/ai/test" \
  -H "Content-Type: application/json" \
  -d '{"provider": "openai", "prompt": "Hello, world!"}'

# Test Anthropic
curl -X POST "http://localhost:8000/api/v1/ai/test" \
  -H "Content-Type: application/json" \
  -d '{"provider": "anthropic", "prompt": "Hello, world!"}'
```

#### **2. Test Cloud Providers**
```bash
# Test AWS
curl -X GET "http://localhost:8000/api/v1/cloud/aws/test"

# Test Azure
curl -X GET "http://localhost:8000/api/v1/cloud/azure/test"

# Test GCP
curl -X GET "http://localhost:8000/api/v1/cloud/gcp/test"
```

## 💰 **Cost Management**

### **API Usage Monitoring**

#### **1. OpenAI Usage**
```bash
# Monitor OpenAI usage
curl -X GET "https://api.openai.com/v1/usage" \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### **2. Anthropic Usage**
```bash
# Monitor Anthropic usage
curl -X GET "https://api.anthropic.com/v1/usage" \
  -H "x-api-key: $ANTHROPIC_API_KEY"
```

#### **3. Cloud Provider Costs**
```bash
# AWS Cost Explorer
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost

# Azure Cost Management
az consumption usage list \
  --start-date 2024-01-01 \
  --end-date 2024-01-31
```

### **Cost Optimization**

#### **1. Set Usage Limits**
```python
# In your application
MAX_TOKENS_PER_REQUEST = 1000
MAX_REQUESTS_PER_MINUTE = 10
MAX_COST_PER_DAY = 10.00  # USD
```

#### **2. Implement Caching**
```python
# Cache AI responses
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_ai_response(prompt: str):
    cache_key = f"ai_response:{hash(prompt)}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    return None
```

## 🆘 **Troubleshooting**

### **Common Issues**

#### **1. API Key Invalid**
```bash
# Check API key format
echo $OPENAI_API_KEY | head -c 10  # Should start with "sk-"
echo $ANTHROPIC_API_KEY | head -c 10  # Should start with "sk-ant-"
```

#### **2. Rate Limiting**
```bash
# Check rate limits
curl -I "https://api.openai.com/v1/models" \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### **3. Network Issues**
```bash
# Test connectivity
curl -X GET "https://api.openai.com/v1/models" \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### **Support Resources**

- **OpenAI**: https://help.openai.com/
- **Anthropic**: https://docs.anthropic.com/
- **Google AI**: https://ai.google.dev/docs
- **AWS**: https://docs.aws.amazon.com/
- **Azure**: https://docs.microsoft.com/azure/
- **GCP**: https://cloud.google.com/docs

## 📊 **Monitoring Dashboard**

Once configured, you can monitor all API usage and costs from the CloudMind dashboard:

- **API Usage**: Real-time monitoring of all API calls
- **Cost Tracking**: Daily, weekly, and monthly cost analysis
- **Performance**: Response times and success rates
- **Alerts**: Automated alerts for high usage or costs

---

## 🎯 **Summary**

This guide provides:

- ✅ **Complete API key setup** for all services
- ✅ **Security best practices** for key management
- ✅ **Testing procedures** to verify configuration
- ✅ **Cost management** strategies
- ✅ **Troubleshooting** for common issues

**Your CloudMind instance is now fully configured and ready for production use!** 🚀
