'use client'

import { useState, useEffect, useMemo } from 'react'
import DashboardLayout from '@/components/layouts/DashboardLayout'
import { 
  Shield, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  XCircle,
  BarChart3,
  PieChart,
  Settings,
  Download,
  RefreshCw,
  Plus,
  Filter,
  Search,
  Eye,
  EyeOff,
  Lock,
  Unlock,
  TrendingUp,
  Brain,
  Zap,
  Target,
  Award,
  Star,
  Rocket,
  Activity,
  Globe,
  Database,
  Server,
  Network,
  Cpu,
  HardDrive,
  Sparkles,
  ShieldCheck,
  AlertCircle,
  Info,
  ArrowUpRight,
  ArrowDownRight,
  Calendar,
  Timer,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon
} from 'lucide-react'

interface SecurityVulnerability {
  id: string
  title: string
  description: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  category: 'injection' | 'encryption' | 'access_control' | 'network' | 'configuration' | 'ai_detected'
  cveId: string | null
  cvssScore: number
  affectedResource: string
  status: 'open' | 'in_progress' | 'resolved' | 'false_positive'
  remediationSteps: string[]
  aiInsights: string[]
  confidence: number
  riskScore: number
  exploitability: 'high' | 'medium' | 'low'
  impact: 'critical' | 'high' | 'medium' | 'low'
  discoveredAt: string
  lastScanned: string
  tags: string[]
}

interface ComplianceFramework {
  name: string
  score: number
  status: 'compliant' | 'at_risk' | 'non_compliant'
  controls: { total: number; passed: number; failed: number; partial: number }
  lastAudit: string
  nextAudit: string
  requirements: string[]
  aiRecommendations: string[]
}

interface SecurityAlert {
  id: string
  title: string
  message: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  category: 'vulnerability' | 'access_control' | 'compliance' | 'anomaly' | 'ai_detected'
  affectedResource: string
  time: string
  status: 'active' | 'acknowledged' | 'resolved'
  aiAnalysis: string
  recommendedActions: string[]
}

export default function SecurityPage() {
  const [selectedPeriod, setSelectedPeriod] = useState('30d')
  const [selectedProject, setSelectedProject] = useState('all')
  const [isLoading, setIsLoading] = useState(false)
  const [viewMode, setViewMode] = useState('overview')
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false)

  // Enhanced state for real-time security monitoring
  const [realTimeThreats, setRealTimeThreats] = useState<any[]>([])
  const [securityScore, setSecurityScore] = useState(85)
  const [aiInsights, setAiInsights] = useState<string[]>([])

  // World-class vulnerabilities with AI insights
  const advancedVulnerabilities: SecurityVulnerability[] = [
    {
      id: 'vuln-001',
      title: 'SQL Injection Vulnerability',
      description: 'Application is vulnerable to SQL injection attacks due to improper input validation. AI analysis detected 95% confidence in exploitability.',
      severity: 'critical',
      category: 'injection',
      cveId: 'CVE-2024-1234',
      cvssScore: 9.8,
      affectedResource: 'web-application',
      status: 'open',
      confidence: 95,
      riskScore: 92,
      exploitability: 'high',
      impact: 'critical',
      discoveredAt: '2024-01-15T08:30:00Z',
      lastScanned: '2024-01-15T10:00:00Z',
      tags: ['SQL Injection', 'Web Application', 'Critical'],
      remediationSteps: [
        'Use parameterized queries with prepared statements',
        'Implement comprehensive input validation',
        'Use ORM frameworks with built-in protection',
        'Enable WAF protection with SQL injection rules',
        'Conduct security code review'
      ],
      aiInsights: [
        'AI detected 3 potential injection points in user input fields',
        'Historical analysis shows 85% of similar vulnerabilities are exploited within 24 hours',
        'Automated remediation can be applied with 92% confidence',
        'Risk assessment: Immediate action required'
      ]
    },
    {
      id: 'vuln-002',
      title: 'Missing Encryption at Rest',
      description: 'Database storage is not encrypted, exposing sensitive data. AI analysis indicates high compliance risk.',
      severity: 'high',
      category: 'encryption',
      cveId: null,
      cvssScore: 7.5,
      affectedResource: 'database-cluster',
      status: 'in_progress',
      confidence: 88,
      riskScore: 78,
      exploitability: 'medium',
      impact: 'high',
      discoveredAt: '2024-01-14T15:45:00Z',
      lastScanned: '2024-01-15T09:30:00Z',
      tags: ['Encryption', 'Database', 'Compliance'],
      remediationSteps: [
        'Enable encryption at rest for all database instances',
        'Use AWS KMS for key management',
        'Implement proper key rotation policies',
        'Audit encryption settings across all databases',
        'Update compliance documentation'
      ],
      aiInsights: [
        'AI analysis shows 40% of data is PII requiring encryption',
        'Compliance frameworks require encryption for 100% of sensitive data',
        'Automated encryption can be implemented with minimal downtime',
        'Risk assessment: High compliance impact'
      ]
    },
    {
      id: 'vuln-003',
      title: 'AI-Detected Anomalous Access Pattern',
      description: 'Machine learning detected unusual access patterns indicating potential security breach.',
      severity: 'high',
      category: 'ai_detected',
      cveId: null,
      cvssScore: 6.8,
      affectedResource: 'auth-service',
      status: 'open',
      confidence: 82,
      riskScore: 75,
      exploitability: 'medium',
      impact: 'high',
      discoveredAt: '2024-01-15T11:20:00Z',
      lastScanned: '2024-01-15T11:20:00Z',
      tags: ['AI Detection', 'Access Control', 'Anomaly'],
      remediationSteps: [
        'Investigate suspicious access patterns',
        'Implement additional authentication factors',
        'Enable real-time threat monitoring',
        'Review and update access policies',
        'Deploy AI-powered security monitoring'
      ],
      aiInsights: [
        'ML model detected 3x normal access attempts from new IP ranges',
        'Behavioral analysis shows 87% similarity to known attack patterns',
        'Automated response can block suspicious IPs immediately',
        'Risk assessment: Requires immediate investigation'
      ]
    }
  ]

  // Enhanced compliance frameworks
  const advancedComplianceFrameworks: ComplianceFramework[] = [
    {
      name: 'SOC2',
      score: 92,
      status: 'compliant',
      controls: { total: 50, passed: 46, failed: 2, partial: 2 },
      lastAudit: '2024-01-10T00:00:00Z',
      nextAudit: '2024-04-10T00:00:00Z',
      requirements: ['Access Control', 'Data Encryption', 'Audit Logging', 'Change Management'],
      aiRecommendations: [
        'Implement automated compliance monitoring',
        'Deploy AI-powered audit trail analysis',
        'Enable real-time compliance scoring',
        'Automate evidence collection for audits'
      ]
    },
    {
      name: 'HIPAA',
      score: 88,
      status: 'at_risk',
      controls: { total: 45, passed: 40, failed: 3, partial: 2 },
      lastAudit: '2024-01-05T00:00:00Z',
      nextAudit: '2024-07-05T00:00:00Z',
      requirements: ['PHI Protection', 'Access Controls', 'Audit Trails', 'Encryption'],
      aiRecommendations: [
        'Enhance PHI data encryption',
        'Implement automated access reviews',
        'Deploy AI-powered compliance monitoring',
        'Automate audit trail generation'
      ]
    },
    {
      name: 'CIS',
      score: 95,
      status: 'compliant',
      controls: { total: 60, passed: 57, failed: 1, partial: 2 },
      lastAudit: '2024-01-12T00:00:00Z',
      nextAudit: '2024-03-12T00:00:00Z',
      requirements: ['Security Configuration', 'Access Management', 'Audit Logging'],
      aiRecommendations: [
        'Automate security configuration checks',
        'Implement continuous compliance monitoring',
        'Deploy AI-powered security scoring',
        'Enable automated remediation'
      ]
    }
  ]

  // Real-time security alerts
  const realTimeSecurityAlerts: SecurityAlert[] = [
    {
      id: 'alert-001',
      title: 'AI-Detected Critical Vulnerability',
      message: 'Machine learning detected SQL injection vulnerability with 95% confidence',
      severity: 'critical',
      category: 'ai_detected',
      affectedResource: 'web-server-01',
      time: '1 hour ago',
      status: 'active',
      aiAnalysis: 'ML model analyzed 10,000+ similar patterns and identified high-risk vulnerability',
      recommendedActions: [
        'Immediately patch vulnerable endpoints',
        'Enable WAF protection',
        'Implement input validation',
        'Conduct security code review'
      ]
    },
    {
      id: 'alert-002',
      title: 'Unauthorized Access Attempt',
      message: 'Multiple failed login attempts detected from suspicious IP addresses',
      severity: 'high',
      category: 'access_control',
      affectedResource: 'auth-service',
      time: '3 hours ago',
      status: 'acknowledged',
      aiAnalysis: 'Behavioral analysis shows 87% similarity to known attack patterns',
      recommendedActions: [
        'Block suspicious IP addresses',
        'Enable multi-factor authentication',
        'Implement rate limiting',
        'Deploy AI-powered threat detection'
      ]
    },
    {
      id: 'alert-003',
      title: 'Compliance Check Failed',
      message: 'SOC2 control CC6.1 failed - missing encryption configuration',
      severity: 'medium',
      category: 'compliance',
      affectedResource: 'database-cluster',
      time: '1 day ago',
      status: 'active',
      aiAnalysis: 'AI analysis shows 40% of data requires encryption for compliance',
      recommendedActions: [
        'Enable encryption at rest',
        'Update compliance documentation',
        'Implement automated compliance monitoring',
        'Schedule compliance review'
      ]
    }
  ]

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-100 border-red-200'
      case 'high': return 'text-orange-600 bg-orange-100 border-orange-200'
      case 'medium': return 'text-yellow-600 bg-yellow-100 border-yellow-200'
      case 'low': return 'text-green-600 bg-green-100 border-green-200'
      default: return 'text-gray-600 bg-gray-100 border-gray-200'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'compliant': return 'text-green-600 bg-green-100'
      case 'at_risk': return 'text-yellow-600 bg-yellow-100'
      case 'non_compliant': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getAlertIcon = (severity: string) => {
    switch (severity) {
      case 'critical': return <XCircle className="w-5 h-5 text-red-500" />
      case 'high': return <AlertTriangle className="w-5 h-5 text-orange-500" />
      case 'medium': return <Clock className="w-5 h-5 text-yellow-500" />
      case 'low': return <CheckCircle className="w-5 h-5 text-green-500" />
      default: return <Shield className="w-5 h-5 text-gray-500" />
    }
  }

  // Real-time security monitoring
  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        // Simulate real-time security updates
        setSecurityScore(prev => Math.max(70, Math.min(100, prev + (Math.random() - 0.5) * 2)))
        
        // Update AI insights
        setAiInsights([
          "🔒 **Threat Detection**: AI detected 2 new potential threats in the last 5 minutes",
          "📊 **Security Score**: Your security posture improved by 3 points this week",
          "⚠️ **Vulnerability Alert**: 1 critical vulnerability requires immediate attention",
          "🎯 **Compliance Status**: All frameworks are within acceptable risk levels",
          "🚀 **AI Protection**: Machine learning blocked 15 suspicious activities today"
        ])
      }, 30000) // Update every 30 seconds

      return () => clearInterval(interval)
    }
  }, [autoRefresh])

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Enhanced Header with AI Security Insights */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Security Center</h1>
            <p className="text-gray-600">AI-powered security monitoring and threat detection.</p>
          </div>
          <div className="flex items-center space-x-3">
            <button 
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={`btn-secondary flex items-center space-x-2 ${autoRefresh ? 'bg-green-100 text-green-700' : ''}`}
            >
              <RefreshCw className={`w-4 h-4 ${autoRefresh ? 'animate-spin' : ''}`} />
              <span>{autoRefresh ? 'Live Monitoring ON' : 'Live Monitoring OFF'}</span>
            </button>
            <button className="btn-primary flex items-center space-x-2">
              <Plus className="w-4 h-4" />
              <span>New Scan</span>
            </button>
          </div>
        </div>

        {/* AI Security Insights Banner */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center space-x-3">
            <Brain className="w-6 h-6 text-blue-600" />
            <div className="flex-1">
              <h3 className="font-semibold text-blue-900">AI Security Insights</h3>
              <p className="text-sm text-blue-700">{aiInsights[0] || "🔒 AI monitoring active - no threats detected"}</p>
            </div>
            <button className="text-blue-600 hover:text-blue-700">
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Enhanced Security Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Security Score</p>
                <p className="text-2xl font-bold text-gray-900">{securityScore}/100</p>
                <div className="flex items-center mt-1">
                  <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">+3 points</span>
                </div>
                <div className="flex items-center mt-1">
                  <Award className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">Above industry average</span>
                </div>
              </div>
              <div className="p-3 bg-blue-100 rounded-lg">
                <Shield className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Threats</p>
                <p className="text-2xl font-bold text-gray-900">3</p>
                <div className="flex items-center mt-1">
                  <XCircle className="w-4 h-4 text-red-500 mr-1" />
                  <span className="text-sm text-red-600">1 critical</span>
                </div>
                <div className="flex items-center mt-1">
                  <Brain className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">AI detected</span>
                </div>
              </div>
              <div className="p-3 bg-red-100 rounded-lg">
                <AlertTriangle className="w-6 h-6 text-red-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Compliance</p>
                <p className="text-2xl font-bold text-gray-900">92%</p>
                <div className="flex items-center mt-1">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">SOC2 compliant</span>
                </div>
                <div className="flex items-center mt-1">
                  <Star className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">All frameworks</span>
                </div>
              </div>
              <div className="p-3 bg-green-100 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">AI Protection</p>
                <p className="text-2xl font-bold text-gray-900">15</p>
                <div className="flex items-center mt-1">
                  <Shield className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">Threats blocked</span>
                </div>
                <div className="flex items-center mt-1">
                  <Zap className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">Today</span>
                </div>
              </div>
              <div className="p-3 bg-purple-100 rounded-lg">
                <Brain className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </div>
        </div>

        {/* World-Class Vulnerability Analysis */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">AI-Powered Vulnerability Analysis</h3>
              <p className="text-sm text-gray-600">Machine learning analysis of security vulnerabilities with automated remediation</p>
            </div>
            <button className="btn-secondary flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Export Report</span>
            </button>
          </div>
          <div className="space-y-6">
            {advancedVulnerabilities.map((vuln) => (
              <div key={vuln.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-3">
                      <Shield className="w-4 h-4 text-gray-400" />
                      <h4 className="text-xl font-medium text-gray-900">{vuln.title}</h4>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getSeverityColor(vuln.severity)}`}>
                        {vuln.severity}
                      </span>
                      {vuln.cveId && (
                        <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                          {vuln.cveId}
                        </span>
                      )}
                      <div className="flex items-center space-x-1">
                        <Brain className="w-4 h-4 text-blue-600" />
                        <span className="text-xs text-blue-600">{vuln.confidence}% confidence</span>
                      </div>
                    </div>
                    
                    <p className="text-gray-600 mb-4">{vuln.description}</p>
                    
                    {/* Enhanced metrics grid */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                      <div className="bg-red-50 p-3 rounded-lg">
                        <span className="text-xs text-gray-500">CVSS Score</span>
                        <p className="text-lg font-bold text-red-600">{vuln.cvssScore}</p>
                      </div>
                      <div className="bg-orange-50 p-3 rounded-lg">
                        <span className="text-xs text-gray-500">Risk Score</span>
                        <p className="text-lg font-bold text-orange-600">{vuln.riskScore}</p>
                      </div>
                      <div className="bg-yellow-50 p-3 rounded-lg">
                        <span className="text-xs text-gray-500">Exploitability</span>
                        <p className="text-lg font-bold text-yellow-600 capitalize">{vuln.exploitability}</p>
                      </div>
                      <div className="bg-purple-50 p-3 rounded-lg">
                        <span className="text-xs text-gray-500">Impact</span>
                        <p className="text-lg font-bold text-purple-600 capitalize">{vuln.impact}</p>
                      </div>
                    </div>

                    {/* AI Insights */}
                    <div className="bg-blue-50 p-4 rounded-lg mb-4">
                      <div className="flex items-center space-x-2 mb-2">
                        <Brain className="w-4 h-4 text-blue-600" />
                        <span className="text-sm font-medium text-blue-900">AI Security Insights</span>
                      </div>
                      <ul className="space-y-1">
                        {vuln.aiInsights.map((insight, index) => (
                          <li key={index} className="text-sm text-blue-700 flex items-start space-x-2">
                            <span className="text-blue-500 mt-1">•</span>
                            <span>{insight}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Remediation steps */}
                    <div className="bg-gray-50 p-4 rounded-lg mb-4">
                      <h5 className="text-sm font-medium text-gray-900 mb-2">Remediation Steps</h5>
                      <ol className="space-y-1">
                        {vuln.remediationSteps.map((step, index) => (
                          <li key={index} className="text-sm text-gray-600 flex items-start space-x-2">
                            <span className="text-gray-500 mt-1">{index + 1}.</span>
                            <span>{step}</span>
                          </li>
                        ))}
                      </ol>
                    </div>

                    {/* Tags */}
                    <div className="flex items-center space-x-2 mb-4">
                      {vuln.tags.map((tag, index) => (
                        <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2 ml-4">
                    <button className="btn-primary text-sm px-4 py-2">
                      <Rocket className="w-4 h-4 mr-2" />
                      Remediate
                    </button>
                    <button className="btn-secondary text-sm px-4 py-2">
                      <Eye className="w-4 h-4 mr-2" />
                      Details
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Enhanced Compliance Status */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Compliance Frameworks</h3>
            <div className="space-y-4">
              {advancedComplianceFrameworks.map((framework) => (
                <div key={framework.name} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-medium text-gray-900">{framework.name}</h4>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(framework.status)}`}>
                      {framework.status.replace('_', ' ')}
                    </span>
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">Overall Score</span>
                    <span className="text-lg font-bold text-gray-900">{framework.score}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full" 
                      style={{ width: `${framework.score}%` }}
                    ></div>
                  </div>
                  <div className="grid grid-cols-3 gap-4 mt-3 text-sm">
                    <div>
                      <span className="text-gray-500">Passed:</span>
                      <span className="ml-1 font-medium text-green-600">{framework.controls.passed}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Failed:</span>
                      <span className="ml-1 font-medium text-red-600">{framework.controls.failed}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Partial:</span>
                      <span className="ml-1 font-medium text-yellow-600">{framework.controls.partial}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Real-time Security Alerts</h3>
            <div className="space-y-3">
              {realTimeSecurityAlerts.map((alert) => (
                <div key={alert.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                  {getAlertIcon(alert.severity)}
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <p className="text-sm font-medium text-gray-900">{alert.title}</p>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(alert.severity)}`}>
                        {alert.severity}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 mb-2">{alert.message}</p>
                    <div className="bg-blue-50 p-2 rounded mb-2">
                      <p className="text-xs text-blue-700 font-medium">AI Analysis:</p>
                      <p className="text-xs text-blue-600">{alert.aiAnalysis}</p>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-500">Resource: {alert.affectedResource}</span>
                      <span className="text-xs text-gray-500">{alert.time}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Security Metrics Dashboard */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Security Metrics Dashboard</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-24 h-24 mx-auto mb-3 relative">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#e5e7eb"
                    strokeWidth="2"
                  />
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#3b82f6"
                    strokeWidth="2"
                    strokeDasharray={`${securityScore}, 100`}
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-xl font-bold text-gray-900">{securityScore}%</span>
                </div>
              </div>
              <h4 className="font-medium text-gray-900">Security Score</h4>
              <p className="text-sm text-gray-600">Overall security posture</p>
            </div>
            <div className="text-center">
              <div className="w-24 h-24 mx-auto mb-3 relative">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#e5e7eb"
                    strokeWidth="2"
                  />
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#10b981"
                    strokeWidth="2"
                    strokeDasharray="92, 100"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-xl font-bold text-gray-900">92%</span>
                </div>
              </div>
              <h4 className="font-medium text-gray-900">Compliance Score</h4>
              <p className="text-sm text-gray-600">Regulatory compliance</p>
            </div>
            <div className="text-center">
              <div className="w-24 h-24 mx-auto mb-3 relative">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#e5e7eb"
                    strokeWidth="2"
                  />
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#f59e0b"
                    strokeWidth="2"
                    strokeDasharray="78, 100"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-xl font-bold text-gray-900">78%</span>
                </div>
              </div>
              <h4 className="font-medium text-gray-900">Threat Detection</h4>
              <p className="text-sm text-gray-600">AI-powered detection</p>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
} 