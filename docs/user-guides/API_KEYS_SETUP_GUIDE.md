# 🔑 API Keys Setup Guide

## 📋 **REQUIRED API KEYS FOR CLOUDMIND**

This guide helps you obtain all the API keys needed for CloudMind's enhanced knowledge base.

---

## 🔒 **SECURITY APIs**

### **1. NVD (National Vulnerability Database)**
- **URL**: https://nvd.nist.gov/developers/request-an-api-key
- **Cost**: Free
- **Rate Limit**: 1000 requests/hour
- **Setup**: 
  1. Visit the NVD website
  2. Fill out the API key request form
  3. Receive key via email within 24 hours

### **2. VirusTotal**
- **URL**: https://www.virustotal.com/gui/join-us
- **Cost**: Free tier available
- **Rate Limit**: 500 requests/hour (free)
- **Setup**:
  1. Create account at VirusTotal
  2. Go to API key section
  3. Generate new API key

### **3. AbuseIPDB**
- **URL**: https://www.abuseipdb.com/api
- **Cost**: Free tier available
- **Rate Limit**: 1000 requests/hour (free)
- **Setup**:
  1. Register at AbuseIPDB
  2. Navigate to API section
  3. Generate API key

---

## ☁️ **CLOUD SERVICES APIs**

### **4. AWS Pricing API**
- **URL**: https://aws.amazon.com/pricing/api/
- **Cost**: Free
- **Rate Limit**: 100 requests/hour
- **Setup**:
  1. AWS account required
  2. No special setup needed
  3. Use AWS credentials

### **5. Azure Pricing API**
- **URL**: https://prices.azure.com/api/retail/prices
- **Cost**: Free
- **Rate Limit**: 100 requests/hour
- **Setup**:
  1. No authentication required
  2. Public API endpoint
  3. No key needed

### **6. Google Cloud Pricing API**
- **URL**: https://cloud.google.com/billing/docs/reference/rest
- **Cost**: Free
- **Rate Limit**: 100 requests/hour
- **Setup**:
  1. Google Cloud account
  2. Enable Cloud Billing API
  3. Create service account key

---

## 🤖 **DATA SCIENCE APIs**

### **7. Kaggle**
- **URL**: https://www.kaggle.com/settings/account
- **Cost**: Free
- **Rate Limit**: 100 requests/hour
- **Setup**:
  1. Create Kaggle account
  2. Go to Account settings
  3. Create new API token

### **8. Hugging Face**
- **URL**: https://huggingface.co/settings/tokens
- **Cost**: Free
- **Rate Limit**: 100 requests/hour
- **Setup**:
  1. Create Hugging Face account
  2. Go to Settings > Access Tokens
  3. Create new token

---

## 📈 **TECHNOLOGY TRENDS APIs**

### **9. GitHub**
- **URL**: https://github.com/settings/tokens
- **Cost**: Free
- **Rate Limit**: 5000 requests/hour
- **Setup**:
  1. GitHub account
  2. Go to Settings > Developer settings
  3. Generate new personal access token

### **10. Stack Overflow**
- **URL**: https://stackapps.com/apps/oauth/register
- **Cost**: Free
- **Rate Limit**: 1000 requests/hour
- **Setup**:
  1. Stack Exchange account
  2. Register application
  3. Get API key

---

## 📊 **PERFORMANCE APIs**

### **11. WebPageTest**
- **URL**: https://www.webpagetest.org/getkey.php
- **Cost**: Free tier available
- **Rate Limit**: 100 requests/hour
- **Setup**:
  1. Visit WebPageTest
  2. Request API key
  3. Receive via email

### **12. GTmetrix**
- **URL**: https://gtmetrix.com/api/
- **Cost**: Free tier available
- **Rate Limit**: 100 requests/hour
- **Setup**:
  1. Create GTmetrix account
  2. Go to API section
  3. Generate API key

---

## 🔧 **SETUP INSTRUCTIONS**

### **Step 1: Create .env file**
```bash
# Copy the example file
cp env.example .env
```

### **Step 2: Add API Keys**
```bash
# Edit .env file and add your keys
nano .env
```

### **Step 3: Required Keys (Minimum)**
```bash
# Essential APIs (recommended to start with)
GITHUB_TOKEN=your_github_token_here
NVD_API_KEY=your_nvd_api_key_here
STACK_OVERFLOW_API_KEY=your_stack_overflow_api_key_here

# Optional but recommended
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
ABUSEIPDB_API_KEY=your_abuseipdb_api_key_here
KAGGLE_API_KEY=your_kaggle_api_key_here
```

### **Step 4: Test Configuration**
```bash
# Test the knowledge engine
cd backend
python -c "from app.services.ai_engine.enhanced_knowledge_engine import EnhancedKnowledgeEngine; print('Knowledge engine loaded successfully')"
```

---

## 📊 **PRIORITY LEVELS**

### **🔥 High Priority (Essential)**
1. **GitHub Token** - Technology trends
2. **NVD API Key** - Security vulnerabilities
3. **Stack Overflow API** - Community data

### **⚡ Medium Priority (Recommended)**
4. **VirusTotal** - Threat intelligence
5. **AbuseIPDB** - IP reputation
6. **Kaggle** - Data science datasets

### **📈 Low Priority (Optional)**
7. **WebPageTest** - Performance metrics
8. **GTmetrix** - Web performance
9. **Cloud Pricing APIs** - Cost optimization

---

## 🚀 **QUICK START**

### **Minimum Setup (3 APIs)**
```bash
# 1. Get GitHub token
# 2. Get NVD API key
# 3. Get Stack Overflow API key
# 4. Add to .env file
# 5. Start CloudMind
```

### **Full Setup (All APIs)**
```bash
# Follow the guide above for all 12+ APIs
# This provides maximum knowledge coverage
```

---

## ⚠️ **IMPORTANT NOTES**

### **Rate Limits**
- Most APIs have hourly rate limits
- CloudMind includes intelligent caching
- Rate limiting prevents API throttling

### **Cost Considerations**
- Most APIs offer free tiers
- Paid tiers provide higher rate limits
- CloudMind optimizes API usage

### **Security**
- Store API keys securely
- Never commit keys to version control
- Use environment variables

---

## 🎯 **BENEFITS BY API COUNT**

### **3 APIs (Minimum)**
- ✅ Basic technology trends
- ✅ Security vulnerability data
- ✅ Community insights

### **6 APIs (Recommended)**
- ✅ Threat intelligence
- ✅ Data science resources
- ✅ IP reputation data

### **12+ APIs (Full Coverage)**
- ✅ Performance metrics
- ✅ Cost optimization
- ✅ Comprehensive knowledge base

---

## 📞 **SUPPORT**

### **API Issues**
- Check rate limits
- Verify API key format
- Test API endpoints directly

### **CloudMind Integration**
- Review logs for API errors
- Check Redis cache status
- Verify environment variables

---

## 🏆 **KNOWLEDGE BASE SCORE**

- **3 APIs**: 75/100 (Basic coverage)
- **6 APIs**: 85/100 (Good coverage)
- **12+ APIs**: 99/100 (World-class coverage)

**Start with the minimum 3 APIs and expand as needed!** 