"""
Enhanced Knowledge Engine with Real-time API Integrations
World-class knowledge base with live data from multiple authoritative sources
"""

import asyncio
import aiohttp
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import hashlib
import redis
from cachetools import TTLCache

from app.core.config import settings

logger = logging.getLogger(__name__)

class KnowledgeSource(Enum):
    """Knowledge source types"""
    SECURITY_VULNERABILITIES = "security_vulnerabilities"
    CLOUD_SERVICES = "cloud_services"
    NETWORKING_STANDARDS = "networking_standards"
    TECHNOLOGY_TRENDS = "technology_trends"
    COMPLIANCE_FRAMEWORKS = "compliance_frameworks"
    ARCHITECTURE_PATTERNS = "architecture_patterns"
    PERFORMANCE_BENCHMARKS = "performance_benchmarks"
    COST_DATA = "cost_data"

@dataclass
class KnowledgeEntry:
    """Knowledge base entry"""
    id: str
    source: KnowledgeSource
    title: str
    content: Dict[str, Any]
    last_updated: datetime
    confidence_score: float
    source_url: Optional[str] = None
    tags: List[str] = None

@dataclass
class APIIntegration:
    """API integration configuration"""
    name: str
    base_url: str
    api_key: Optional[str] = None
    headers: Dict[str, str] = None
    rate_limit: int = 100
    cache_ttl: int = 3600
    enabled: bool = True

class EnhancedKnowledgeEngine:
    """World-class knowledge engine with real-time API integrations"""
    
    def __init__(self):
        self.redis_client = redis.Redis.from_url(settings.REDIS_URL)
        self.cache = TTLCache(maxsize=1000, ttl=3600)
        self.api_integrations = self._initialize_api_integrations()
        self.knowledge_sources = self._initialize_knowledge_sources()
        self.last_sync = {}
        
    def _initialize_api_integrations(self) -> Dict[str, APIIntegration]:
        """Initialize API integrations for real-time data"""
        return {
            # Security & Vulnerability APIs
            "nvd": APIIntegration(
                name="NVD",
                base_url="https://services.nvd.nist.gov/rest/json/cves/2.0/",
                rate_limit=1000,
                cache_ttl=1800
            ),
            "cve_search": APIIntegration(
                name="CVE Search",
                base_url="https://cve.circl.lu/api/",
                rate_limit=100,
                cache_ttl=3600
            ),
            "security_advisories": APIIntegration(
                name="Security Advisories",
                base_url="https://api.github.com/repos/",
                api_key=settings.GITHUB_TOKEN,
                rate_limit=5000,
                cache_ttl=7200
            ),
            "virustotal": APIIntegration(
                name="VirusTotal",
                base_url="https://www.virustotal.com/vtapi/v2/",
                api_key=settings.VIRUSTOTAL_API_KEY,
                rate_limit=500,
                cache_ttl=3600
            ),
            "abuseipdb": APIIntegration(
                name="AbuseIPDB",
                base_url="https://api.abuseipdb.com/api/v2/",
                api_key=settings.ABUSEIPDB_API_KEY,
                rate_limit=1000,
                cache_ttl=7200
            ),
            
            # Cloud Services APIs
            "aws_pricing": APIIntegration(
                name="AWS Pricing",
                base_url="https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/",
                rate_limit=100,
                cache_ttl=86400
            ),
            "azure_pricing": APIIntegration(
                name="Azure Pricing",
                base_url="https://prices.azure.com/api/retail/prices",
                rate_limit=100,
                cache_ttl=86400
            ),
            "gcp_pricing": APIIntegration(
                name="GCP Pricing",
                base_url="https://cloudbilling.googleapis.com/v1/services",
                api_key=settings.GCP_PRICING_API_KEY,
                rate_limit=100,
                cache_ttl=86400
            ),
            "aws_architecture": APIIntegration(
                name="AWS Architecture",
                base_url="https://aws.amazon.com/architecture/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "azure_architecture": APIIntegration(
                name="Azure Architecture",
                base_url="https://docs.microsoft.com/en-us/azure/architecture/",
                rate_limit=50,
                cache_ttl=86400
            ),
            
            # Networking APIs
            "ipapi": APIIntegration(
                name="IP Geolocation",
                base_url="http://ip-api.com/json/",
                rate_limit=1000,
                cache_ttl=3600
            ),
            "bgpview": APIIntegration(
                name="BGP Information",
                base_url="https://api.bgpview.io/",
                rate_limit=100,
                cache_ttl=7200
            ),
            "dns_google": APIIntegration(
                name="Google DNS",
                base_url="https://dns.google/resolve",
                rate_limit=1000,
                cache_ttl=3600
            ),
            "iana_protocols": APIIntegration(
                name="IANA Protocols",
                base_url="https://www.iana.org/assignments/protocol-numbers/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "rfc_standards": APIIntegration(
                name="RFC Standards",
                base_url="https://tools.ietf.org/html/",
                rate_limit=100,
                cache_ttl=86400
            ),
            
            # Data Science & ML APIs
            "huggingface": APIIntegration(
                name="Hugging Face",
                base_url="https://huggingface.co/api/models",
                rate_limit=100,
                cache_ttl=7200
            ),
            "tensorflow_hub": APIIntegration(
                name="TensorFlow Hub",
                base_url="https://tfhub.dev/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "pytorch_hub": APIIntegration(
                name="PyTorch Hub",
                base_url="https://pytorch.org/hub/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "kaggle_datasets": APIIntegration(
                name="Kaggle Datasets",
                base_url="https://www.kaggle.com/api/v1/",
                api_key=settings.KAGGLE_API_KEY,
                rate_limit=100,
                cache_ttl=7200
            ),
            "bigquery_datasets": APIIntegration(
                name="BigQuery Datasets",
                base_url="https://cloud.google.com/bigquery/public-data",
                rate_limit=50,
                cache_ttl=86400
            ),
            
            # Technology Trends & Community APIs
            "stackoverflow": APIIntegration(
                name="Stack Overflow",
                base_url="https://api.stackexchange.com/2.3/",
                rate_limit=1000,
                cache_ttl=3600
            ),
            "github_trends": APIIntegration(
                name="GitHub Trends",
                base_url="https://github.com/trending",
                rate_limit=100,
                cache_ttl=7200
            ),
            "techempower": APIIntegration(
                name="TechEmpower Benchmarks",
                base_url="https://www.techempower.com/benchmarks/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "db_engines": APIIntegration(
                name="DB-Engines Rankings",
                base_url="https://db-engines.com/en/ranking",
                rate_limit=50,
                cache_ttl=86400
            ),
            
            # Compliance & Standards APIs
            "nist_cybersecurity": APIIntegration(
                name="NIST Cybersecurity",
                base_url="https://www.nist.gov/cyberframework",
                rate_limit=50,
                cache_ttl=86400
            ),
            "iso_standards": APIIntegration(
                name="ISO Standards",
                base_url="https://www.iso.org/standards.html",
                rate_limit=50,
                cache_ttl=86400
            ),
            "owasp": APIIntegration(
                name="OWASP",
                base_url="https://owasp.org/www-project-top-ten/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "itil": APIIntegration(
                name="ITIL Framework",
                base_url="https://www.axelos.com/best-practice-solutions/itil",
                rate_limit=50,
                cache_ttl=86400
            ),
            
            # Infrastructure & DevOps APIs
            "terraform_registry": APIIntegration(
                name="Terraform Registry",
                base_url="https://registry.terraform.io/v1/providers",
                rate_limit=100,
                cache_ttl=7200
            ),
            "docker_hub": APIIntegration(
                name="Docker Hub",
                base_url="https://hub.docker.com/api/",
                rate_limit=100,
                cache_ttl=7200
            ),
            "kubernetes": APIIntegration(
                name="Kubernetes",
                base_url="https://kubernetes.io/docs/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "prometheus": APIIntegration(
                name="Prometheus",
                base_url="https://prometheus.io/docs/",
                rate_limit=50,
                cache_ttl=86400
            ),
            
            # Performance & Monitoring APIs
            "lighthouse": APIIntegration(
                name="Lighthouse",
                base_url="https://developers.google.com/web/tools/lighthouse",
                rate_limit=50,
                cache_ttl=86400
            ),
            "webpagetest": APIIntegration(
                name="WebPageTest",
                base_url="https://www.webpagetest.org/api/",
                rate_limit=100,
                cache_ttl=7200
            ),
            "gtmetrix": APIIntegration(
                name="GTmetrix",
                base_url="https://gtmetrix.com/api/",
                rate_limit=100,
                cache_ttl=7200
            ),
            
            # Advanced Networking APIs
            "cisco_devnet": APIIntegration(
                name="Cisco DevNet",
                base_url="https://developer.cisco.com/api/",
                rate_limit=100,
                cache_ttl=3600
            ),
            "juniper_api": APIIntegration(
                name="Juniper Networks",
                base_url="https://www.juniper.net/documentation/api/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "arista_api": APIIntegration(
                name="Arista Networks",
                base_url="https://www.arista.com/en/support/api/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "fortinet_api": APIIntegration(
                name="Fortinet",
                base_url="https://docs.fortinet.com/api/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "palo_alto_api": APIIntegration(
                name="Palo Alto Networks",
                base_url="https://docs.paloaltonetworks.com/api/",
                rate_limit=50,
                cache_ttl=86400
            ),
            
            # Advanced Security APIs
            "mitre_attack": APIIntegration(
                name="MITRE ATT&CK",
                base_url="https://attack.mitre.org/api/",
                rate_limit=100,
                cache_ttl=7200
            ),
            "malware_bazaar": APIIntegration(
                name="MalwareBazaar",
                base_url="https://bazaar.abuse.ch/api/",
                rate_limit=100,
                cache_ttl=3600
            ),
            "urlhaus": APIIntegration(
                name="URLhaus",
                base_url="https://urlhaus.abuse.ch/api/",
                rate_limit=100,
                cache_ttl=3600
            ),
            "phishtank": APIIntegration(
                name="PhishTank",
                base_url="https://data.phishtank.com/data/",
                rate_limit=100,
                cache_ttl=3600
            ),
            "haveibeenpwned": APIIntegration(
                name="HaveIBeenPwned",
                base_url="https://haveibeenpwned.com/api/v3/",
                api_key=settings.HIBP_API_KEY,
                rate_limit=100,
                cache_ttl=7200
            ),
            
            # Advanced Cloud APIs
            "aws_cloudformation": APIIntegration(
                name="AWS CloudFormation",
                base_url="https://docs.aws.amazon.com/cloudformation/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "azure_arm": APIIntegration(
                name="Azure Resource Manager",
                base_url="https://docs.microsoft.com/en-us/rest/api/azure/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "gcp_cloud_build": APIIntegration(
                name="Google Cloud Build",
                base_url="https://cloud.google.com/build/docs/api/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "terraform_cloud": APIIntegration(
                name="Terraform Cloud",
                base_url="https://www.terraform.io/cloud-docs/api-docs/",
                api_key=settings.TERRAFORM_CLOUD_TOKEN,
                rate_limit=100,
                cache_ttl=7200
            ),
            "ansible_galaxy": APIIntegration(
                name="Ansible Galaxy",
                base_url="https://galaxy.ansible.com/api/v1/",
                rate_limit=100,
                cache_ttl=7200
            ),
            
            # Enterprise & Compliance APIs
            "pci_dss": APIIntegration(
                name="PCI DSS",
                base_url="https://www.pcisecuritystandards.org/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "sox_compliance": APIIntegration(
                name="SOX Compliance",
                base_url="https://www.sec.gov/sox/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "gdpr_api": APIIntegration(
                name="GDPR Compliance",
                base_url="https://gdpr.eu/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "hipaa_api": APIIntegration(
                name="HIPAA Compliance",
                base_url="https://www.hhs.gov/hipaa/",
                rate_limit=50,
                cache_ttl=86400
            ),
            
            # Advanced Monitoring & Observability
            "datadog_api": APIIntegration(
                name="Datadog",
                base_url="https://docs.datadoghq.com/api/",
                api_key=settings.DATADOG_API_KEY,
                rate_limit=100,
                cache_ttl=3600
            ),
            "new_relic_api": APIIntegration(
                name="New Relic",
                base_url="https://docs.newrelic.com/docs/apis/",
                api_key=settings.NEW_RELIC_API_KEY,
                rate_limit=100,
                cache_ttl=3600
            ),
            "splunk_api": APIIntegration(
                name="Splunk",
                base_url="https://docs.splunk.com/Documentation/Splunk/",
                rate_limit=100,
                cache_ttl=3600
            ),
            "elastic_api": APIIntegration(
                name="Elasticsearch",
                base_url="https://www.elastic.co/guide/en/elasticsearch/reference/",
                rate_limit=100,
                cache_ttl=3600
            ),
            
            # Advanced Data Science & ML
            "openai_api": APIIntegration(
                name="OpenAI",
                base_url="https://api.openai.com/v1/",
                api_key=settings.OPENAI_API_KEY,
                rate_limit=1000,
                cache_ttl=3600
            ),
            "anthropic_api": APIIntegration(
                name="Anthropic",
                base_url="https://api.anthropic.com/v1/",
                api_key=settings.ANTHROPIC_API_KEY,
                rate_limit=1000,
                cache_ttl=3600
            ),
            "google_ai": APIIntegration(
                name="Google AI",
                base_url="https://generativelanguage.googleapis.com/",
                api_key=settings.GOOGLE_AI_API_KEY,
                rate_limit=1000,
                cache_ttl=3600
            ),
            "azure_openai": APIIntegration(
                name="Azure OpenAI",
                base_url="https://api.openai.com/v1/",
                api_key=settings.AZURE_OPENAI_API_KEY,
                rate_limit=1000,
                cache_ttl=3600
            ),
            
            # Advanced Infrastructure & DevOps
            "jenkins_api": APIIntegration(
                name="Jenkins",
                base_url="https://www.jenkins.io/doc/book/using/remote-access-api/",
                rate_limit=100,
                cache_ttl=3600
            ),
            "gitlab_api": APIIntegration(
                name="GitLab",
                base_url="https://docs.gitlab.com/ee/api/",
                api_key=settings.GITLAB_API_KEY,
                rate_limit=1000,
                cache_ttl=3600
            ),
            "bitbucket_api": APIIntegration(
                name="Bitbucket",
                base_url="https://developer.atlassian.com/cloud/bitbucket/rest/",
                api_key=settings.BITBUCKET_API_KEY,
                rate_limit=1000,
                cache_ttl=3600
            ),
            "jira_api": APIIntegration(
                name="Jira",
                base_url="https://developer.atlassian.com/cloud/jira/platform/rest/v3/",
                api_key=settings.JIRA_API_KEY,
                rate_limit=1000,
                cache_ttl=3600
            ),
            
            # Advanced Database & Storage
            "mongodb_atlas": APIIntegration(
                name="MongoDB Atlas",
                base_url="https://docs.atlas.mongodb.com/api/",
                api_key=settings.MONGODB_ATLAS_API_KEY,
                rate_limit=100,
                cache_ttl=3600
            ),
            "redis_cloud": APIIntegration(
                name="Redis Cloud",
                base_url="https://redis.io/commands/",
                rate_limit=100,
                cache_ttl=3600
            ),
            "aws_rds": APIIntegration(
                name="AWS RDS",
                base_url="https://docs.aws.amazon.com/rds/",
                rate_limit=50,
                cache_ttl=86400
            ),
            "azure_sql": APIIntegration(
                name="Azure SQL",
                base_url="https://docs.microsoft.com/en-us/azure/azure-sql/",
                rate_limit=50,
                cache_ttl=86400
            ),
            
            # Advanced Networking Protocols
            "bgp_tools": APIIntegration(
                name="BGP Tools",
                base_url="https://bgp.tools/api/",
                rate_limit=100,
                cache_ttl=3600
            ),
            "ripe_stat": APIIntegration(
                name="RIPE Stat",
                base_url="https://stat.ripe.net/api/",
                rate_limit=100,
                cache_ttl=3600
            ),
            "arin_api": APIIntegration(
                name="ARIN",
                base_url="https://www.arin.net/reference/materials/",
                rate_limit=100,
                cache_ttl=3600
            ),
            "apnic_api": APIIntegration(
                name="APNIC",
                base_url="https://www.apnic.net/support/",
                rate_limit=100,
                cache_ttl=3600
            ),
            
            # Advanced Security Frameworks
            "nist_cyber": APIIntegration(
                name="NIST Cybersecurity",
                base_url="https://www.nist.gov/cyberframework",
                rate_limit=50,
                cache_ttl=86400
            ),
            "iso_27001": APIIntegration(
                name="ISO 27001",
                base_url="https://www.iso.org/isoiec-27001-information-security.html",
                rate_limit=50,
                cache_ttl=86400
            ),
            "cobit": APIIntegration(
                name="COBIT",
                base_url="https://www.isaca.org/resources/cobit",
                rate_limit=50,
                cache_ttl=86400
            ),
            "itil": APIIntegration(
                name="ITIL",
                base_url="https://www.axelos.com/best-practice-solutions/itil",
                rate_limit=50,
                cache_ttl=86400
            )
        }
    
    def _initialize_knowledge_sources(self) -> Dict[str, Any]:
        """Initialize knowledge source configurations"""
        return {
            "security_vulnerabilities": {
                "sources": ["nvd", "cve_search", "security_advisories"],
                "update_interval": 3600,  # 1 hour
                "priority": "high"
            },
            "cloud_services": {
                "sources": ["aws_pricing", "azure_pricing", "gcp_pricing"],
                "update_interval": 86400,  # 24 hours
                "priority": "medium"
            },
            "technology_trends": {
                "sources": ["stack_overflow", "github_trends"],
                "update_interval": 7200,  # 2 hours
                "priority": "medium"
            },
            "compliance_frameworks": {
                "sources": ["nist_frameworks", "iso_standards"],
                "update_interval": 86400,  # 24 hours
                "priority": "low"
            },
            "performance_benchmarks": {
                "sources": ["tech_empower", "db_engines"],
                "update_interval": 86400,  # 24 hours
                "priority": "medium"
            },
            "networking_standards": {
                "sources": ["iana_protocols", "rfc_standards"],
                "update_interval": 86400,  # 24 hours
                "priority": "low"
            }
        }
    
    async def get_real_time_knowledge(
        self,
        category: str,
        query: str,
        force_refresh: bool = False
    ) -> List[KnowledgeEntry]:
        """Get real-time knowledge from multiple sources"""
        try:
            cache_key = f"knowledge:{category}:{hashlib.md5(query.encode()).hexdigest()}"
            
            # Check cache first
            if not force_refresh:
                cached_data = await self._get_cached_knowledge(cache_key)
                if cached_data:
                    return cached_data
            
            # Fetch from multiple sources
            knowledge_entries = []
            
            if category in self.knowledge_sources:
                sources = self.knowledge_sources[category]["sources"]
                
                # Fetch from all sources concurrently
                tasks = []
                for source in sources:
                    if source in self.api_integrations:
                        task = self._fetch_from_api(source, query, category)
                        tasks.append(task)
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, list):
                        knowledge_entries.extend(result)
            
            # Cache the results
            await self._cache_knowledge(cache_key, knowledge_entries)
            
            return knowledge_entries
            
        except Exception as e:
            logger.error(f"Error fetching real-time knowledge: {e}")
            return []
    
    async def _fetch_from_api(
        self,
        api_name: str,
        query: str,
        category: str
    ) -> List[KnowledgeEntry]:
        """Fetch data from specific API"""
        try:
            integration = self.api_integrations[api_name]
            
            if not integration.enabled:
                return []
            
            # Check rate limiting
            if not await self._check_rate_limit(api_name):
                logger.warning(f"Rate limit exceeded for {api_name}")
                return []
            
            async with aiohttp.ClientSession() as session:
                url = await self._build_api_url(api_name, query, category)
                headers = await self._build_api_headers(api_name)
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return await self._parse_api_response(api_name, data, category)
                    else:
                        logger.error(f"API {api_name} returned status {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error fetching from API {api_name}: {e}")
            return []
    
    async def _build_api_url(self, api_name: str, query: str, category: str) -> str:
        """Build API URL based on source and query"""
        base_url = self.api_integrations[api_name].base_url
        
        if api_name == "nvd":
            return f"{base_url}?keyword={query}&pubStartDate=2024-01-01T00:00:00:000 UTC-05:00"
        elif api_name == "stack_overflow":
            return f"{base_url}search/advanced?order=desc&sort=activity&tagged={query}&site=stackoverflow"
        elif api_name == "github_trends":
            return f"{base_url}?q={query}&sort=stars&order=desc"
        elif api_name == "aws_pricing":
            return f"{base_url}AmazonEC2/current/us-east-1/index.json"
        else:
            return f"{base_url}{query}"
    
    async def _build_api_headers(self, api_name: str) -> Dict[str, str]:
        """Build API headers"""
        integration = self.api_integrations[api_name]
        headers = {
            "User-Agent": "CloudMind-Enhanced-Knowledge-Engine/1.0",
            "Accept": "application/json"
        }
        
        if integration.api_key:
            if api_name == "github_trends":
                headers["Authorization"] = f"token {integration.api_key}"
            else:
                headers["X-API-Key"] = integration.api_key
        
        if integration.headers:
            headers.update(integration.headers)
        
        return headers
    
    async def _parse_api_response(
        self,
        api_name: str,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse API response into knowledge entries"""
        entries = []
        
        try:
            if api_name == "nvd":
                entries = await self._parse_nvd_response(data, category)
            elif api_name == "stack_overflow":
                entries = await self._parse_stackoverflow_response(data, category)
            elif api_name == "github_trends":
                entries = await self._parse_github_response(data, category)
            elif api_name == "aws_pricing":
                entries = await self._parse_aws_pricing_response(data, category)
            elif api_name == "virustotal":
                entries = await self._parse_virustotal_response(data, category)
            elif api_name == "abuseipdb":
                entries = await self._parse_abuseipdb_response(data, category)
            elif api_name == "ipapi":
                entries = await self._parse_ipapi_response(data, category)
            elif api_name == "bgpview":
                entries = await self._parse_bgpview_response(data, category)
            elif api_name == "huggingface":
                entries = await self._parse_huggingface_response(data, category)
            elif api_name == "kaggle_datasets":
                entries = await self._parse_kaggle_response(data, category)
            elif api_name == "techempower":
                entries = await self._parse_techempower_response(data, category)
            elif api_name == "db_engines":
                entries = await self._parse_dbengines_response(data, category)
            elif api_name == "terraform_registry":
                entries = await self._parse_terraform_response(data, category)
            elif api_name == "docker_hub":
                entries = await self._parse_dockerhub_response(data, category)
            elif api_name == "cisco_devnet":
                entries = await self._parse_cisco_response(data, category)
            elif api_name == "mitre_attack":
                entries = await self._parse_mitre_response(data, category)
            elif api_name == "malware_bazaar":
                entries = await self._parse_malwarebazaar_response(data, category)
            elif api_name == "haveibeenpwned":
                entries = await self._parse_hibp_response(data, category)
            elif api_name == "datadog_api":
                entries = await self._parse_datadog_response(data, category)
            elif api_name == "new_relic_api":
                entries = await self._parse_newrelic_response(data, category)
            elif api_name == "openai_api":
                entries = await self._parse_openai_response(data, category)
            elif api_name == "anthropic_api":
                entries = await self._parse_anthropic_response(data, category)
            elif api_name == "gitlab_api":
                entries = await self._parse_gitlab_response(data, category)
            elif api_name == "mongodb_atlas":
                entries = await self._parse_mongodb_response(data, category)
            elif api_name == "bgp_tools":
                entries = await self._parse_bgptools_response(data, category)
            elif api_name == "ripe_stat":
                entries = await self._parse_ripestat_response(data, category)
            else:
                # Generic parsing
                entries = await self._parse_generic_response(api_name, data, category)
                
        except Exception as e:
            logger.error(f"Error parsing {api_name} response: {e}")
        
        return entries
    
    async def _parse_nvd_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse NVD vulnerability data"""
        entries = []
        
        for vuln in data.get("vulnerabilities", []):
            cve = vuln.get("cve", {})
            
            entry = KnowledgeEntry(
                id=cve.get("id", ""),
                source=KnowledgeSource.SECURITY_VULNERABILITIES,
                title=cve.get("description", {}).get("description_data", [{}])[0].get("value", ""),
                content={
                    "severity": cve.get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("baseSeverity", ""),
                    "score": cve.get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("baseScore", 0),
                    "published_date": cve.get("publishedDate", ""),
                    "last_modified": cve.get("lastModifiedDate", ""),
                    "references": [ref.get("url", "") for ref in cve.get("references", {}).get("reference_data", [])]
                },
                last_updated=datetime.now(),
                confidence_score=0.95,
                source_url=f"https://nvd.nist.gov/vuln/detail/{cve.get('id', '')}",
                tags=["security", "vulnerability", "cve"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_stackoverflow_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse Stack Overflow technology trends"""
        entries = []
        
        for item in data.get("items", []):
            entry = KnowledgeEntry(
                id=str(item.get("question_id", "")),
                source=KnowledgeSource.TECHNOLOGY_TRENDS,
                title=item.get("title", ""),
                content={
                    "tags": item.get("tags", []),
                    "score": item.get("score", 0),
                    "answer_count": item.get("answer_count", 0),
                    "view_count": item.get("view_count", 0),
                    "creation_date": item.get("creation_date", ""),
                    "link": item.get("link", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                source_url=item.get("link", ""),
                tags=["technology", "trends", "stackoverflow"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_github_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse GitHub trends data"""
        entries = []
        
        for repo in data.get("items", []):
            entry = KnowledgeEntry(
                id=str(repo.get("id", "")),
                source=KnowledgeSource.TECHNOLOGY_TRENDS,
                title=repo.get("name", ""),
                content={
                    "description": repo.get("description", ""),
                    "language": repo.get("language", ""),
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0),
                    "topics": repo.get("topics", []),
                    "created_at": repo.get("created_at", ""),
                    "updated_at": repo.get("updated_at", ""),
                    "url": repo.get("html_url", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.90,
                source_url=repo.get("html_url", ""),
                tags=["github", "trends", "open-source"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_aws_pricing_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse AWS pricing data"""
        entries = []
        
        for product in data.get("products", {}).values():
            entry = KnowledgeEntry(
                id=product.get("sku", ""),
                source=KnowledgeSource.CLOUD_SERVICES,
                title=product.get("productFamily", ""),
                content={
                    "attributes": product.get("attributes", {}),
                    "pricing": product.get("pricing", {}),
                    "service_code": product.get("servicecode", ""),
                    "location": product.get("attributes", {}).get("location", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.95,
                tags=["aws", "pricing", "cloud"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_generic_response(
        self,
        api_name: str,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Generic API response parser"""
        entries = []
        
        # Try to extract meaningful data
        if isinstance(data, dict):
            entry = KnowledgeEntry(
                id=f"{api_name}_{int(time.time())}",
                source=KnowledgeSource(category),
                title=data.get("title", data.get("name", f"{api_name} data")),
                content=data,
                last_updated=datetime.now(),
                confidence_score=0.70,
                tags=[api_name, category]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_virustotal_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse VirusTotal threat intelligence data"""
        entries = []
        
        entry = KnowledgeEntry(
            id=data.get("scan_id", ""),
            source=KnowledgeSource.SECURITY_VULNERABILITIES,
            title=f"Threat Analysis: {data.get('resource', '')}",
            content={
                "positives": data.get("positives", 0),
                "total": data.get("total", 0),
                "scan_date": data.get("scan_date", ""),
                "permalink": data.get("permalink", ""),
                "scans": data.get("scans", {}),
                "resource": data.get("resource", "")
            },
            last_updated=datetime.now(),
            confidence_score=0.90,
            source_url=data.get("permalink", ""),
            tags=["security", "threat-intelligence", "virustotal"]
        )
        entries.append(entry)
        
        return entries
    
    async def _parse_abuseipdb_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse AbuseIPDB threat data"""
        entries = []
        
        for report in data.get("data", []):
            entry = KnowledgeEntry(
                id=report.get("ipAddress", ""),
                source=KnowledgeSource.SECURITY_VULNERABILITIES,
                title=f"IP Threat: {report.get('ipAddress', '')}",
                content={
                    "abuse_confidence_score": report.get("abuseConfidenceScore", 0),
                    "country_code": report.get("countryCode", ""),
                    "usage_type": report.get("usageType", ""),
                    "isp": report.get("isp", ""),
                    "domain": report.get("domain", ""),
                    "total_reports": report.get("totalReports", 0),
                    "last_reported_at": report.get("lastReportedAt", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                tags=["security", "threat-intelligence", "abuseipdb"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_ipapi_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse IP geolocation data"""
        entries = []
        
        entry = KnowledgeEntry(
            id=data.get("query", ""),
            source=KnowledgeSource.NETWORKING_STANDARDS,
            title=f"IP Location: {data.get('query', '')}",
            content={
                "country": data.get("country", ""),
                "region": data.get("regionName", ""),
                "city": data.get("city", ""),
                "isp": data.get("isp", ""),
                "org": data.get("org", ""),
                "as": data.get("as", ""),
                "timezone": data.get("timezone", ""),
                "lat": data.get("lat", 0),
                "lon": data.get("lon", 0)
            },
            last_updated=datetime.now(),
            confidence_score=0.95,
            tags=["networking", "geolocation", "ipapi"]
        )
        entries.append(entry)
        
        return entries
    
    async def _parse_bgpview_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse BGP routing information"""
        entries = []
        
        for prefix in data.get("data", {}).get("prefixes", []):
            entry = KnowledgeEntry(
                id=prefix.get("prefix", ""),
                source=KnowledgeSource.NETWORKING_STANDARDS,
                title=f"BGP Route: {prefix.get('prefix', '')}",
                content={
                    "asn": prefix.get("asn", {}).get("asn", ""),
                    "description": prefix.get("asn", {}).get("description", ""),
                    "country_code": prefix.get("asn", {}).get("country_code", ""),
                    "name": prefix.get("asn", {}).get("name", ""),
                    "prefix": prefix.get("prefix", ""),
                    "max_length": prefix.get("max_length", 0),
                    "min_length": prefix.get("min_length", 0)
                },
                last_updated=datetime.now(),
                confidence_score=0.90,
                tags=["networking", "bgp", "routing", "bgpview"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_huggingface_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse Hugging Face model data"""
        entries = []
        
        for model in data:
            entry = KnowledgeEntry(
                id=model.get("id", ""),
                source=KnowledgeSource.TECHNOLOGY_TRENDS,
                title=model.get("id", ""),
                content={
                    "author": model.get("author", ""),
                    "last_modified": model.get("lastModified", ""),
                    "downloads": model.get("downloads", 0),
                    "likes": model.get("likes", 0),
                    "tags": model.get("tags", []),
                    "pipeline_tag": model.get("pipeline_tag", ""),
                    "library_name": model.get("library_name", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                source_url=f"https://huggingface.co/{model.get('id', '')}",
                tags=["ml", "ai", "models", "huggingface"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_kaggle_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse Kaggle dataset information"""
        entries = []
        
        for dataset in data.get("datasets", []):
            entry = KnowledgeEntry(
                id=dataset.get("ref", ""),
                source=KnowledgeSource.TECHNOLOGY_TRENDS,
                title=dataset.get("title", ""),
                content={
                    "description": dataset.get("description", ""),
                    "size": dataset.get("size", 0),
                    "downloads": dataset.get("downloads", 0),
                    "votes": dataset.get("votes", 0),
                    "tags": dataset.get("tags", []),
                    "license": dataset.get("license", ""),
                    "last_updated": dataset.get("lastUpdated", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.80,
                source_url=f"https://www.kaggle.com/datasets/{dataset.get('ref', '')}",
                tags=["data-science", "datasets", "kaggle"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_techempower_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse TechEmpower benchmark data"""
        entries = []
        
        for benchmark in data.get("benchmarks", []):
            entry = KnowledgeEntry(
                id=benchmark.get("name", ""),
                source=KnowledgeSource.PERFORMANCE_BENCHMARKS,
                title=f"Performance Benchmark: {benchmark.get('name', '')}",
                content={
                    "framework": benchmark.get("framework", ""),
                    "language": benchmark.get("language", ""),
                    "requests_per_second": benchmark.get("requests_per_second", 0),
                    "latency": benchmark.get("latency", 0),
                    "throughput": benchmark.get("throughput", 0),
                    "errors": benchmark.get("errors", 0),
                    "version": benchmark.get("version", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.95,
                tags=["performance", "benchmarks", "techempower"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_dbengines_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse DB-Engines ranking data"""
        entries = []
        
        for db in data.get("rankings", []):
            entry = KnowledgeEntry(
                id=db.get("name", ""),
                source=KnowledgeSource.TECHNOLOGY_TRENDS,
                title=f"Database: {db.get('name', '')}",
                content={
                    "score": db.get("score", 0),
                    "rank": db.get("rank", 0),
                    "category": db.get("category", ""),
                    "description": db.get("description", ""),
                    "website": db.get("website", ""),
                    "license": db.get("license", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.90,
                tags=["databases", "rankings", "db-engines"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_terraform_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse Terraform provider data"""
        entries = []
        
        for provider in data.get("providers", []):
            entry = KnowledgeEntry(
                id=provider.get("id", ""),
                source=KnowledgeSource.ARCHITECTURE_PATTERNS,
                title=f"Terraform Provider: {provider.get('id', '')}",
                content={
                    "name": provider.get("name", ""),
                    "namespace": provider.get("namespace", ""),
                    "version": provider.get("version", ""),
                    "downloads": provider.get("downloads", 0),
                    "description": provider.get("description", ""),
                    "source": provider.get("source", ""),
                    "published_at": provider.get("published_at", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                tags=["terraform", "iac", "providers"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_dockerhub_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse Docker Hub image data"""
        entries = []
        
        for image in data.get("results", []):
            entry = KnowledgeEntry(
                id=image.get("name", ""),
                source=KnowledgeSource.ARCHITECTURE_PATTERNS,
                title=f"Docker Image: {image.get('name', '')}",
                content={
                    "description": image.get("description", ""),
                    "star_count": image.get("star_count", 0),
                    "pull_count": image.get("pull_count", 0),
                    "last_updated": image.get("last_updated", ""),
                    "official": image.get("is_official", False),
                    "automated": image.get("is_automated", False),
                    "namespace": image.get("namespace", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.80,
                tags=["docker", "containers", "images"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_cisco_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse Cisco DevNet data"""
        entries = []
        
        for item in data.get("data", []):
            entry = KnowledgeEntry(
                id=item.get("id", ""),
                source=KnowledgeSource.ARCHITECTURE_PATTERNS,
                title=item.get("name", ""),
                content={
                    "description": item.get("description", ""),
                    "documentation_url": item.get("documentation_url", ""),
                    "api_endpoints": item.get("api_endpoints", []),
                    "version": item.get("version", ""),
                    "last_updated": item.get("last_updated", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                source_url=item.get("documentation_url", ""),
                tags=["networking", "cisco", "devnet"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_mitre_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse MITRE ATT&CK data"""
        entries = []
        
        for technique in data.get("techniques", []):
            entry = KnowledgeEntry(
                id=technique.get("id", ""),
                source=KnowledgeSource.SECURITY_VULNERABILITIES,
                title=technique.get("name", ""),
                content={
                    "id": technique.get("id", ""),
                    "name": technique.get("name", ""),
                    "description": technique.get("description", ""),
                    "tactic": technique.get("tactic", []),
                    "platform": technique.get("platform", []),
                    "software": technique.get("software", []),
                    "mitigation": technique.get("mitigation", []),
                    "detection": technique.get("detection", []),
                    "data_sources": technique.get("data_sources", []),
                    "permissions_required": technique.get("permissions_required", []),
                    "effective_permissions": technique.get("effective_permissions", []),
                    "detection_level": technique.get("detection_level", ""),
                    "impact_level": technique.get("impact_level", ""),
                    "external_references": technique.get("external_references", [])
                },
                last_updated=datetime.now(),
                confidence_score=0.90,
                source_url=f"https://attack.mitre.org/techniques/{technique.get('id', '')}",
                tags=["security", "threat-intelligence", "mitre"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_malwarebazaar_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse MalwareBazaar data"""
        entries = []
        
        for item in data.get("data", []):
            entry = KnowledgeEntry(
                id=item.get("md5", ""),
                source=KnowledgeSource.SECURITY_VULNERABILITIES,
                title=f"Malware: {item.get('file_name', '')}",
                content={
                    "md5": item.get("md5", ""),
                    "sha256": item.get("sha256", ""),
                    "file_name": item.get("file_name", ""),
                    "file_size": item.get("file_size", 0),
                    "signature": item.get("signature", ""),
                    "threat_name": item.get("threat_name", ""),
                    "first_seen": item.get("first_seen", ""),
                    "last_seen": item.get("last_seen", ""),
                    "reporter": item.get("reporter", ""),
                    "tags": item.get("tags", [])
                },
                last_updated=datetime.now(),
                confidence_score=0.95,
                source_url=f"https://bazaar.abuse.ch/browse.php?search={item.get('md5', '')}",
                tags=["security", "malware", "bazaar"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_hibp_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse HaveIBeenPwned data"""
        entries = []
        
        for breach in data.get("breaches", []):
            entry = KnowledgeEntry(
                id=breach.get("Name", ""),
                source=KnowledgeSource.SECURITY_VULNERABILITIES,
                title=f"Data Breach: {breach.get('Name', '')}",
                content={
                    "Name": breach.get("Name", ""),
                    "Domain": breach.get("Domain", ""),
                    "BreachDate": breach.get("BreachDate", ""),
                    "AddedDate": breach.get("AddedDate", ""),
                    "ModifiedDate": breach.get("ModifiedDate", ""),
                    "PwnCount": breach.get("PwnCount", 0),
                    "Description": breach.get("Description", ""),
                    "DataClasses": breach.get("DataClasses", []),
                    "IsVerified": breach.get("IsVerified", False),
                    "IsSensitive": breach.get("IsSensitive", False),
                    "IsRetired": breach.get("IsRetired", False),
                    "IsSpamList": breach.get("IsSpamList", False),
                    "LogoPath": breach.get("LogoPath", ""),
                    "BreachRank": breach.get("BreachRank", 0)
                },
                last_updated=datetime.now(),
                confidence_score=0.90,
                source_url=f"https://haveibeenpwned.com/breaches/{breach.get('Name', '')}",
                tags=["security", "data-breach", "hibp"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_datadog_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse Datadog data"""
        entries = []
        
        for item in data.get("data", []):
            entry = KnowledgeEntry(
                id=item.get("id", ""),
                source=KnowledgeSource.SECURITY_VULNERABILITIES,
                title=item.get("name", ""),
                content={
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "description": item.get("description", ""),
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", ""),
                    "type": item.get("type", ""),
                    "options": item.get("options", {}),
                    "api_key": item.get("api_key", ""),
                    "api_url": item.get("api_url", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                source_url=f"https://docs.datadoghq.com/api/{item.get('type', '')}/",
                tags=["monitoring", "datadog"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_newrelic_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse New Relic data"""
        entries = []
        
        for item in data.get("data", []):
            entry = KnowledgeEntry(
                id=item.get("id", ""),
                source=KnowledgeSource.SECURITY_VULNERABILITIES,
                title=item.get("name", ""),
                content={
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "description": item.get("description", ""),
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", ""),
                    "type": item.get("type", ""),
                    "options": item.get("options", {}),
                    "api_key": item.get("api_key", ""),
                    "api_url": item.get("api_url", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                source_url=f"https://docs.newrelic.com/docs/apis/{item.get('type', '')}/",
                tags=["monitoring", "new-relic"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_openai_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse OpenAI data"""
        entries = []
        
        for item in data.get("data", []):
            entry = KnowledgeEntry(
                id=item.get("id", ""),
                source=KnowledgeSource.TECHNOLOGY_TRENDS,
                title=item.get("name", ""),
                content={
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "description": item.get("description", ""),
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", ""),
                    "type": item.get("type", ""),
                    "options": item.get("options", {}),
                    "api_key": item.get("api_key", ""),
                    "api_url": item.get("api_url", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                source_url=f"https://api.openai.com/v1/{item.get('type', '')}/",
                tags=["ai", "openai"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_anthropic_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse Anthropic data"""
        entries = []
        
        for item in data.get("data", []):
            entry = KnowledgeEntry(
                id=item.get("id", ""),
                source=KnowledgeSource.TECHNOLOGY_TRENDS,
                title=item.get("name", ""),
                content={
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "description": item.get("description", ""),
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", ""),
                    "type": item.get("type", ""),
                    "options": item.get("options", {}),
                    "api_key": item.get("api_key", ""),
                    "api_url": item.get("api_url", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                source_url=f"https://api.anthropic.com/v1/{item.get('type', '')}/",
                tags=["ai", "anthropic"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_gitlab_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse GitLab data"""
        entries = []
        
        for item in data.get("data", []):
            entry = KnowledgeEntry(
                id=item.get("id", ""),
                source=KnowledgeSource.ARCHITECTURE_PATTERNS,
                title=item.get("name", ""),
                content={
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "description": item.get("description", ""),
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", ""),
                    "type": item.get("type", ""),
                    "options": item.get("options", {}),
                    "api_key": item.get("api_key", ""),
                    "api_url": item.get("api_url", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                source_url=f"https://docs.gitlab.com/ee/api/{item.get('type', '')}/",
                tags=["devops", "gitlab"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_mongodb_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse MongoDB Atlas data"""
        entries = []
        
        for item in data.get("data", []):
            entry = KnowledgeEntry(
                id=item.get("id", ""),
                source=KnowledgeSource.ARCHITECTURE_PATTERNS,
                title=item.get("name", ""),
                content={
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "description": item.get("description", ""),
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", ""),
                    "type": item.get("type", ""),
                    "options": item.get("options", {}),
                    "api_key": item.get("api_key", ""),
                    "api_url": item.get("api_url", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                source_url=f"https://docs.atlas.mongodb.com/api/{item.get('type', '')}/",
                tags=["databases", "mongodb"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_bgptools_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse BGP Tools data"""
        entries = []
        
        for item in data.get("data", []):
            entry = KnowledgeEntry(
                id=item.get("id", ""),
                source=KnowledgeSource.NETWORKING_STANDARDS,
                title=item.get("name", ""),
                content={
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "description": item.get("description", ""),
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", ""),
                    "type": item.get("type", ""),
                    "options": item.get("options", {}),
                    "api_key": item.get("api_key", ""),
                    "api_url": item.get("api_url", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                source_url=f"https://bgp.tools/api/{item.get('type', '')}/",
                tags=["networking", "bgp"]
            )
            entries.append(entry)
        
        return entries
    
    async def _parse_ripestat_response(
        self,
        data: Dict[str, Any],
        category: str
    ) -> List[KnowledgeEntry]:
        """Parse RIPE Stat data"""
        entries = []
        
        for item in data.get("data", []):
            entry = KnowledgeEntry(
                id=item.get("id", ""),
                source=KnowledgeSource.NETWORKING_STANDARDS,
                title=item.get("name", ""),
                content={
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "description": item.get("description", ""),
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", ""),
                    "type": item.get("type", ""),
                    "options": item.get("options", {}),
                    "api_key": item.get("api_key", ""),
                    "api_url": item.get("api_url", "")
                },
                last_updated=datetime.now(),
                confidence_score=0.85,
                source_url=f"https://stat.ripe.net/api/{item.get('type', '')}/",
                tags=["networking", "ripe"]
            )
            entries.append(entry)
        
        return entries
    
    async def _check_rate_limit(self, api_name: str) -> bool:
        """Check API rate limiting"""
        try:
            integration = self.api_integrations[api_name]
            key = f"rate_limit:{api_name}"
            
            current_count = await self.redis_client.get(key)
            if current_count and int(current_count) >= integration.rate_limit:
                return False
            
            # Increment counter
            await self.redis_client.incr(key)
            await self.redis_client.expire(key, 3600)  # 1 hour window
            
            return True
            
        except Exception as e:
            logger.error(f"Rate limit check failed for {api_name}: {e}")
            return True  # Allow if check fails
    
    async def _get_cached_knowledge(self, cache_key: str) -> Optional[List[KnowledgeEntry]]:
        """Get cached knowledge"""
        try:
            cached_data = await self.redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            logger.error(f"Cache retrieval failed: {e}")
        return None
    
    async def _cache_knowledge(self, cache_key: str, entries: List[KnowledgeEntry]):
        """Cache knowledge entries"""
        try:
            # Convert to JSON-serializable format
            serializable_entries = []
            for entry in entries:
                serializable_entry = {
                    "id": entry.id,
                    "source": entry.source.value,
                    "title": entry.title,
                    "content": entry.content,
                    "last_updated": entry.last_updated.isoformat(),
                    "confidence_score": entry.confidence_score,
                    "source_url": entry.source_url,
                    "tags": entry.tags or []
                }
                serializable_entries.append(serializable_entry)
            
            await self.redis_client.setex(
                cache_key,
                3600,  # 1 hour TTL
                json.dumps(serializable_entries)
            )
            
        except Exception as e:
            logger.error(f"Cache storage failed: {e}")
    
    async def get_comprehensive_knowledge(
        self,
        requirements: Dict[str, Any]
    ) -> Dict[str, List[KnowledgeEntry]]:
        """Get comprehensive knowledge for architecture recommendations"""
        try:
            # Extract relevant categories from requirements
            categories = self._extract_knowledge_categories(requirements)
            
            # Fetch knowledge for each category
            knowledge_results = {}
            
            for category in categories:
                query = self._build_knowledge_query(requirements, category)
                entries = await self.get_real_time_knowledge(category, query)
                knowledge_results[category] = entries
            
            return knowledge_results
            
        except Exception as e:
            logger.error(f"Comprehensive knowledge fetch failed: {e}")
            return {}
    
    def _extract_knowledge_categories(self, requirements: Dict[str, Any]) -> List[str]:
        """Extract relevant knowledge categories from requirements"""
        categories = []
        
        # Analyze requirements for relevant categories
        if any(word in str(requirements).lower() for word in ["security", "vulnerability", "threat"]):
            categories.append("security_vulnerabilities")
        
        if any(word in str(requirements).lower() for word in ["cloud", "aws", "azure", "gcp", "cost"]):
            categories.append("cloud_services")
        
        if any(word in str(requirements).lower() for word in ["trend", "popular", "adoption"]):
            categories.append("technology_trends")
        
        if any(word in str(requirements).lower() for word in ["compliance", "standard", "framework"]):
            categories.append("compliance_frameworks")
        
        if any(word in str(requirements).lower() for word in ["performance", "benchmark", "speed"]):
            categories.append("performance_benchmarks")
        
        if any(word in str(requirements).lower() for word in ["network", "protocol", "rfc"]):
            categories.append("networking_standards")
        
        return categories
    
    def _build_knowledge_query(self, requirements: Dict[str, Any], category: str) -> str:
        """Build optimized query for knowledge search"""
        # Extract key terms from requirements
        terms = []
        
        if "technologies" in requirements:
            terms.extend(requirements["technologies"])
        
        if "architecture" in requirements:
            terms.append(requirements["architecture"])
        
        if "domain" in requirements:
            terms.append(requirements["domain"])
        
        # Add category-specific terms
        if category == "security_vulnerabilities":
            terms.extend(["security", "vulnerability", "threat"])
        elif category == "cloud_services":
            terms.extend(["cloud", "aws", "azure", "gcp"])
        elif category == "technology_trends":
            terms.extend(["trend", "popular", "adoption"])
        
        return " ".join(terms) if terms else category
    
    async def start_knowledge_sync(self):
        """Start background knowledge synchronization"""
        try:
            while True:
                for category, config in self.knowledge_sources.items():
                    if await self._should_sync_category(category, config):
                        await self._sync_category(category, config)
                
                # Wait before next sync cycle
                await asyncio.sleep(300)  # 5 minutes
                
        except Exception as e:
            logger.error(f"Knowledge sync failed: {e}")
    
    async def _should_sync_category(self, category: str, config: Dict[str, Any]) -> bool:
        """Check if category should be synced"""
        last_sync_key = f"last_sync:{category}"
        last_sync = await self.redis_client.get(last_sync_key)
        
        if not last_sync:
            return True
        
        last_sync_time = datetime.fromisoformat(last_sync.decode())
        interval = timedelta(seconds=config["update_interval"])
        
        return datetime.now() - last_sync_time > interval
    
    async def _sync_category(self, category: str, config: Dict[str, Any]):
        """Sync knowledge for specific category"""
        try:
            logger.info(f"Syncing knowledge category: {category}")
            
            for source in config["sources"]:
                if source in self.api_integrations:
                    await self._fetch_from_api(source, category, category)
            
            # Update last sync time
            await self.redis_client.set(
                f"last_sync:{category}",
                datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Category sync failed for {category}: {e}") 