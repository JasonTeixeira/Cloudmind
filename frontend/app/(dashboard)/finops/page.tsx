'use client'

import { useState, useEffect, useMemo } from 'react'
import DashboardLayout from '@/components/layouts/DashboardLayout'
import { 
  DollarSign, 
  TrendingUp, 
  TrendingDown, 
  BarChart3,
  PieChart,
  LineChart,
  Target,
  AlertTriangle,
  CheckCircle,
  Clock,
  Users,
  Activity,
  Settings,
  Download,
  RefreshCw,
  Plus,
  Filter,
  Search,
  Eye,
  Edit,
  Share2,
  Zap,
  Shield,
  Globe,
  Database,
  Server,
  Brain,
  Award,
  Star,
  Rocket,
  Sparkles,
  Info,
  ArrowUpRight,
  ArrowDownRight,
  Calendar,
  Timer,
  TrendingUpIcon,
  TrendingDownIcon,
  Calculator,
  PieChartIcon,
  BarChart3Icon,
  LineChartIcon
} from 'lucide-react'

interface FinOpsMetrics {
  totalSpend: number
  budgetVariance: number
  costEfficiency: number
  unitEconomics: {
    costPerUser: number
    costPerTransaction: number
    costPerRequest: number
    revenuePerUser: number
    profitMargin: number
  }
  savings: {
    potential: number
    implemented: number
    pending: number
    automated: number
  }
  forecasts: {
    nextMonth: number
    nextQuarter: number
    confidence: number
    accuracy: number
  }
  aiInsights: string[]
}

interface CostDriver {
  service: string
  cost: number
  percentage: number
  trend: number
  optimization: number
  efficiency: number
  aiRecommendations: string[]
}

interface OptimizationOpportunity {
  id: string
  title: string
  description: string
  category: 'compute' | 'storage' | 'network' | 'database' | 'ai_ml' | 'automation'
  priority: 'critical' | 'high' | 'medium' | 'low'
  potentialSavings: number
  implementationEffort: 'low' | 'medium' | 'high'
  riskLevel: 'low' | 'medium' | 'high'
  roi: number
  paybackPeriod: number
  status: 'pending' | 'in_progress' | 'approved' | 'completed'
  aiConfidence: number
  automated: boolean
  tags: string[]
  implementationSteps: string[]
  aiInsights: string[]
}

interface UnitEconomics {
  metric: string
  current: number
  target: number
  trend: number
  industry: number
  efficiency: number
  aiRecommendations: string[]
}

export default function FinOpsPage() {
  const [selectedPeriod, setSelectedPeriod] = useState('30d')
  const [selectedProject, setSelectedProject] = useState('all')
  const [viewMode, setViewMode] = useState('overview')
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false)

  // Enhanced state for real-time FinOps monitoring
  const [realTimeMetrics, setRealTimeMetrics] = useState<any[]>([])
  const [aiInsights, setAiInsights] = useState<string[]>([])

  // World-class FinOps metrics with AI insights
  const advancedFinOpsMetrics: FinOpsMetrics = {
    totalSpend: 124500,
    budgetVariance: -8.2,
    costEfficiency: 87.5,
    unitEconomics: {
      costPerUser: 2.45,
      costPerTransaction: 0.15,
      costPerRequest: 0.003,
      revenuePerUser: 15.80,
      profitMargin: 84.5
    },
    savings: {
      potential: 18500,
      implemented: 8200,
      pending: 10300,
      automated: 4500
    },
    forecasts: {
      nextMonth: 118000,
      nextQuarter: 345000,
      confidence: 92.5,
      accuracy: 94.2
    },
    aiInsights: [
      "🚀 **Cost Trend Analysis**: Your costs are trending 8% below forecast with 92% confidence",
      "💡 **Optimization Opportunity**: AI identified $18,500 in potential savings",
      "📊 **Efficiency Score**: Your infrastructure efficiency is 87%, above industry average",
      "🎯 **Unit Economics**: Cost per user is 15% below industry average",
      "⚡ **Automation Impact**: Automated optimizations saved $4,500 this month"
    ]
  }

  // Enhanced cost drivers with AI analysis
  const advancedCostDrivers: CostDriver[] = [
    { 
      service: 'EC2', 
      cost: 45000, 
      percentage: 36.1, 
      trend: -5.2, 
      optimization: 15, 
      efficiency: 85,
      aiRecommendations: [
        'Implement auto-scaling for 20% cost reduction',
        'Use reserved instances for predictable workloads',
        'Right-size instances based on usage patterns'
      ]
    },
    { 
      service: 'RDS', 
      cost: 28000, 
      percentage: 22.5, 
      trend: 2.1, 
      optimization: 8, 
      efficiency: 92,
      aiRecommendations: [
        'Enable read replicas for better performance',
        'Implement automated storage scaling',
        'Consider Aurora Serverless for variable workloads'
      ]
    },
    { 
      service: 'S3', 
      cost: 22000, 
      percentage: 17.7, 
      trend: 1.8, 
      optimization: 12, 
      efficiency: 88,
      aiRecommendations: [
        'Implement lifecycle policies for 25% savings',
        'Enable intelligent tiering for infrequently accessed data',
        'Optimize storage class selection'
      ]
    },
    { 
      service: 'CloudFront', 
      cost: 15000, 
      percentage: 12.0, 
      trend: 0.5, 
      optimization: 5, 
      efficiency: 95,
      aiRecommendations: [
        'Optimize cache hit rates for better performance',
        'Implement compression for bandwidth savings',
        'Use regional edge caches for lower latency'
      ]
    },
    { 
      service: 'Lambda', 
      cost: 8500, 
      percentage: 6.8, 
      trend: 12.3, 
      optimization: 3, 
      efficiency: 78,
      aiRecommendations: [
        'Optimize function execution time',
        'Use provisioned concurrency for consistent performance',
        'Implement proper error handling and retries'
      ]
    },
    { 
      service: 'Other', 
      cost: 5000, 
      percentage: 4.9, 
      trend: -1.2, 
      optimization: 2, 
      efficiency: 90,
      aiRecommendations: [
        'Review and optimize service usage',
        'Implement cost allocation tags',
        'Set up budget alerts and monitoring'
      ]
    }
  ]

  // World-class optimization opportunities
  const advancedOptimizationOpportunities: OptimizationOpportunity[] = [
    {
      id: 'opt-001',
      title: 'AI-Powered Reserved Instance Optimization',
      description: 'Machine learning analysis of workload patterns to optimize reserved instance purchases with 95% confidence.',
      category: 'compute',
      priority: 'high',
      potentialSavings: 8500,
      implementationEffort: 'medium',
      riskLevel: 'low',
      roi: 340,
      paybackPeriod: 3,
      status: 'pending',
      aiConfidence: 95,
      automated: true,
      tags: ['EC2', 'Reserved Instances', 'AI Optimization', 'Automated'],
      implementationSteps: [
        'AI analysis of 6-month usage patterns',
        'Identify instances with >70% utilization',
        'Purchase 1-year reserved instances',
        'Monitor cost savings monthly'
      ],
      aiInsights: [
        'ML model predicts workload patterns with 95% accuracy',
        'Historical data shows 15% cost reduction potential',
        'Automated purchasing can save 5% on upfront costs',
        'Risk assessment: Low impact on performance'
      ]
    },
    {
      id: 'opt-002',
      title: 'Intelligent Storage Lifecycle Management',
      description: 'AI-driven storage optimization with automated lifecycle policies and intelligent tiering.',
      category: 'storage',
      priority: 'critical',
      potentialSavings: 4200,
      implementationEffort: 'low',
      riskLevel: 'low',
      roi: 280,
      paybackPeriod: 2,
      status: 'in_progress',
      aiConfidence: 92,
      automated: true,
      tags: ['S3', 'Lifecycle', 'AI Automation', 'Storage'],
      implementationSteps: [
        'AI analysis of access patterns for all S3 buckets',
        'Automated lifecycle policy configuration',
        'Intelligent tiering implementation',
        'Continuous monitoring and optimization'
      ],
      aiInsights: [
        'AI detected 40% of data accessed less than monthly',
        'Automated tiering can save 25% on storage costs',
        'Zero risk of data loss with proper configuration',
        'Real-time optimization based on usage patterns'
      ]
    },
    {
      id: 'opt-003',
      title: 'ML-Based Auto-scaling Optimization',
      description: 'Machine learning algorithms to optimize auto-scaling policies and reduce over-provisioning.',
      category: 'automation',
      priority: 'high',
      potentialSavings: 3800,
      implementationEffort: 'high',
      riskLevel: 'medium',
      roi: 190,
      paybackPeriod: 4,
      status: 'approved',
      aiConfidence: 88,
      automated: true,
      tags: ['Auto Scaling', 'ML', 'Performance', 'Automation'],
      implementationSteps: [
        'Deploy ML-based scaling algorithms',
        'Configure predictive scaling policies',
        'Set up monitoring and alerting',
        'Gradual rollout with fallback options'
      ],
      aiInsights: [
        'ML model predicts traffic patterns with 89% accuracy',
        'Can reduce over-provisioning by 35%',
        'Performance impact: <2% latency increase',
        'Automated scaling reduces manual intervention'
      ]
    }
  ]

  // Enhanced unit economics with AI recommendations
  const advancedUnitEconomics: UnitEconomics[] = [
    { 
      metric: 'Cost per User', 
      current: 2.45, 
      target: 2.00, 
      trend: -8.2, 
      industry: 3.20, 
      efficiency: 85,
      aiRecommendations: [
        'Implement user-based cost allocation',
        'Optimize resource usage per user',
        'Consider serverless for variable workloads'
      ]
    },
    { 
      metric: 'Cost per Transaction', 
      current: 0.15, 
      target: 0.12, 
      trend: -5.1, 
      industry: 0.18, 
      efficiency: 92,
      aiRecommendations: [
        'Optimize database queries for faster transactions',
        'Implement caching for frequently accessed data',
        'Use CDN for static content delivery'
      ]
    },
    { 
      metric: 'Cost per Request', 
      current: 0.003, 
      target: 0.002, 
      trend: -12.3, 
      industry: 0.005, 
      efficiency: 78,
      aiRecommendations: [
        'Optimize Lambda function execution time',
        'Implement request batching where possible',
        'Use API Gateway caching for repeated requests'
      ]
    },
    { 
      metric: 'Revenue per User', 
      current: 15.80, 
      target: 18.00, 
      trend: 8.5, 
      industry: 12.50, 
      efficiency: 95,
      aiRecommendations: [
        'Focus on user engagement and retention',
        'Implement upselling opportunities',
        'Optimize conversion funnels'
      ]
    },
    { 
      metric: 'Profit Margin', 
      current: 84.5, 
      target: 88.9, 
      trend: 2.1, 
      industry: 75.0, 
      efficiency: 89,
      aiRecommendations: [
        'Continue cost optimization efforts',
        'Scale high-margin services',
        'Automate low-value manual processes'
      ]
    }
  ]

  const getTrendColor = (trend: number) => {
    return trend >= 0 ? 'text-red-500' : 'text-green-500'
  }

  const getOptimizationColor = (percentage: number) => {
    if (percentage >= 15) return 'text-red-600'
    if (percentage >= 8) return 'text-yellow-600'
    return 'text-green-600'
  }

  const getEfficiencyColor = (efficiency: number) => {
    if (efficiency >= 90) return 'text-green-600'
    if (efficiency >= 80) return 'text-yellow-600'
    return 'text-red-600'
  }

  // Real-time FinOps monitoring simulation
  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        // Simulate real-time metrics updates
        setRealTimeMetrics(prev => [...prev, {
          timestamp: new Date().toISOString(),
          spend: Math.random() * 1000 + 120000,
          efficiency: Math.random() * 10 + 85,
          savings: Math.random() * 500 + 1000
        }])
        
        // Update AI insights
        setAiInsights([
          "🚀 **Real-time Alert**: Cost efficiency improved by 2.3% this hour",
          "💡 **AI Recommendation**: Consider implementing auto-scaling for 15% cost reduction",
          "📊 **Forecast Update**: Next month's spend predicted at $118,000 with 92% confidence",
          "🎯 **Optimization**: 3 new cost optimization opportunities identified",
          "⚡ **Automation**: AI saved $450 in the last 30 minutes"
        ])
      }, 30000) // Update every 30 seconds

      return () => clearInterval(interval)
    }
  }, [autoRefresh])

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Enhanced Header with AI FinOps Insights */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">FinOps Center</h1>
            <p className="text-gray-600">AI-powered financial operations and cost optimization.</p>
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
              <span>New Analysis</span>
            </button>
          </div>
        </div>

        {/* AI FinOps Insights Banner */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center space-x-3">
            <Brain className="w-6 h-6 text-blue-600" />
            <div className="flex-1">
              <h3 className="font-semibold text-blue-900">AI FinOps Insights</h3>
              <p className="text-sm text-blue-700">{aiInsights[0] || "🚀 AI monitoring active - financial operations optimized"}</p>
            </div>
            <button className="text-blue-600 hover:text-blue-700">
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Enhanced FinOps Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Spend</p>
                <p className="text-2xl font-bold text-gray-900">${(advancedFinOpsMetrics.totalSpend/100).toFixed(2)}</p>
                <div className="flex items-center mt-1">
                  <TrendingDown className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">{advancedFinOpsMetrics.budgetVariance}% vs budget</span>
                </div>
                <div className="flex items-center mt-1">
                  <Brain className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">AI optimized</span>
                </div>
              </div>
              <div className="p-3 bg-blue-100 rounded-lg">
                <DollarSign className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Cost Efficiency</p>
                <p className="text-2xl font-bold text-gray-900">{advancedFinOpsMetrics.costEfficiency}%</p>
                <div className="flex items-center mt-1">
                  <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">+2.3% this month</span>
                </div>
                <div className="flex items-center mt-1">
                  <Award className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">Above average</span>
                </div>
              </div>
              <div className="p-3 bg-green-100 rounded-lg">
                <Target className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Potential Savings</p>
                <p className="text-2xl font-bold text-gray-900">${(advancedFinOpsMetrics.savings.potential/100).toFixed(2)}</p>
                <div className="flex items-center mt-1">
                  <AlertTriangle className="w-4 h-4 text-yellow-500 mr-1" />
                  <span className="text-sm text-yellow-600">15 opportunities</span>
                </div>
                <div className="flex items-center mt-1">
                  <Zap className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">AI identified</span>
                </div>
              </div>
              <div className="p-3 bg-yellow-100 rounded-lg">
                <Zap className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Forecast Accuracy</p>
                <p className="text-2xl font-bold text-gray-900">{advancedFinOpsMetrics.forecasts.confidence}%</p>
                <div className="flex items-center mt-1">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">High confidence</span>
                </div>
                <div className="flex items-center mt-1">
                  <Star className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">ML powered</span>
                </div>
              </div>
              <div className="p-3 bg-purple-100 rounded-lg">
                <BarChart3 className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Enhanced Unit Economics */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">AI-Powered Unit Economics</h3>
            <div className="flex items-center space-x-2">
              <button 
                onClick={() => setViewMode('overview')}
                className={`px-3 py-1 rounded-md text-sm font-medium ${
                  viewMode === 'overview' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                Overview
              </button>
              <button 
                onClick={() => setViewMode('detailed')}
                className={`px-3 py-1 rounded-md text-sm font-medium ${
                  viewMode === 'detailed' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                Detailed
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-4">Key Metrics with AI Insights</h4>
              <div className="space-y-4">
                {advancedUnitEconomics.map((metric, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <p className="text-sm font-medium text-gray-900">{metric.metric}</p>
                      <p className="text-xs text-gray-500">Target: {metric.target} | Industry: {metric.industry}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-bold text-gray-900">{metric.current}</p>
                      <div className="flex items-center">
                        <span className={`text-xs ${getTrendColor(metric.trend)}`}>
                          {metric.trend >= 0 ? '+' : ''}{metric.trend}%
                        </span>
                        <span className={`text-xs ml-2 ${getEfficiencyColor(metric.efficiency)}`}>
                          {metric.efficiency}% efficient
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900 mb-4">Cost per User Trend</h4>
              <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <LineChart className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-500">Interactive chart showing cost per user over time</p>
                  <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Brain className="w-4 h-4 text-blue-600" />
                      <span className="text-sm text-blue-700">AI Analysis: 15% below industry average</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* World-Class Cost Drivers Analysis */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">AI-Powered Cost Drivers Analysis</h3>
          <div className="space-y-4">
            {advancedCostDrivers.map((driver, index) => (
              <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div className="flex items-center space-x-4">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    {driver.service === 'EC2' && <Server className="w-5 h-5 text-blue-600" />}
                    {driver.service === 'RDS' && <Database className="w-5 h-5 text-blue-600" />}
                    {driver.service === 'S3' && <Globe className="w-5 h-5 text-blue-600" />}
                    {driver.service === 'CloudFront' && <Activity className="w-5 h-5 text-blue-600" />}
                    {driver.service === 'Lambda' && <Zap className="w-5 h-5 text-blue-600" />}
                    {driver.service === 'Other' && <Settings className="w-5 h-5 text-blue-600" />}
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">{driver.service}</h4>
                    <p className="text-sm text-gray-500">{driver.percentage}% of total spend</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-6">
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Cost</p>
                    <p className="font-medium text-gray-900">${(driver.cost/100).toFixed(2)}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Trend</p>
                    <p className={`font-medium ${getTrendColor(driver.trend)}`}>
                      {driver.trend >= 0 ? '+' : ''}{driver.trend}%
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Optimization</p>
                    <p className={`font-medium ${getOptimizationColor(driver.optimization)}`}>
                      {driver.optimization}%
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Efficiency</p>
                    <p className={`font-medium ${getEfficiencyColor(driver.efficiency)}`}>
                      {driver.efficiency}%
                    </p>
                  </div>
                  <button className="btn-secondary text-sm px-3 py-1">
                    <Brain className="w-4 h-4 mr-1" />
                    Optimize
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* World-Class Optimization Opportunities */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">AI-Powered Optimization Opportunities</h3>
              <p className="text-sm text-gray-600">Machine learning analysis for maximum cost savings and efficiency</p>
            </div>
            <button className="btn-secondary flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Export Report</span>
            </button>
          </div>
          
          <div className="space-y-6">
            {advancedOptimizationOpportunities.map((opportunity) => (
              <div key={opportunity.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className="p-2 bg-blue-100 rounded-lg">
                        <DollarSign className="w-4 h-4 text-blue-600" />
                      </div>
                      <h4 className="text-xl font-medium text-gray-900">{opportunity.title}</h4>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        opportunity.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        opportunity.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                        opportunity.status === 'approved' ? 'bg-green-100 text-green-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {opportunity.status.replace('_', ' ')}
                      </span>
                      <div className="flex items-center space-x-1">
                        <Brain className="w-4 h-4 text-blue-600" />
                        <span className="text-xs text-blue-600">{opportunity.aiConfidence}% confidence</span>
                      </div>
                      {opportunity.automated && (
                        <div className="flex items-center space-x-1">
                          <Zap className="w-4 h-4 text-green-600" />
                          <span className="text-xs text-green-600">Automated</span>
                        </div>
                      )}
                    </div>
                    
                    <p className="text-gray-600 mb-4">{opportunity.description}</p>
                    
                    {/* Enhanced metrics grid */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                      <div className="bg-green-50 p-3 rounded-lg">
                        <span className="text-xs text-gray-500">Potential Savings</span>
                        <p className="text-lg font-bold text-green-600">${(opportunity.potentialSavings/100).toFixed(2)}</p>
                      </div>
                      <div className="bg-blue-50 p-3 rounded-lg">
                        <span className="text-xs text-gray-500">ROI</span>
                        <p className="text-lg font-bold text-blue-600">{opportunity.roi}%</p>
                      </div>
                      <div className="bg-purple-50 p-3 rounded-lg">
                        <span className="text-xs text-gray-500">Payback Period</span>
                        <p className="text-lg font-bold text-purple-600">{opportunity.paybackPeriod} months</p>
                      </div>
                      <div className="bg-yellow-50 p-3 rounded-lg">
                        <span className="text-xs text-gray-500">Risk Level</span>
                        <p className="text-lg font-bold text-yellow-600 capitalize">{opportunity.riskLevel}</p>
                      </div>
                    </div>

                    {/* AI Insights */}
                    <div className="bg-blue-50 p-4 rounded-lg mb-4">
                      <div className="flex items-center space-x-2 mb-2">
                        <Brain className="w-4 h-4 text-blue-600" />
                        <span className="text-sm font-medium text-blue-900">AI FinOps Insights</span>
                      </div>
                      <ul className="space-y-1">
                        {opportunity.aiInsights.map((insight, index) => (
                          <li key={index} className="text-sm text-blue-700 flex items-start space-x-2">
                            <span className="text-blue-500 mt-1">•</span>
                            <span>{insight}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Implementation steps */}
                    <div className="bg-gray-50 p-4 rounded-lg mb-4">
                      <h5 className="text-sm font-medium text-gray-900 mb-2">Implementation Steps</h5>
                      <ol className="space-y-1">
                        {opportunity.implementationSteps.map((step, index) => (
                          <li key={index} className="text-sm text-gray-600 flex items-start space-x-2">
                            <span className="text-gray-500 mt-1">{index + 1}.</span>
                            <span>{step}</span>
                          </li>
                        ))}
                      </ol>
                    </div>

                    {/* Tags */}
                    <div className="flex items-center space-x-2 mb-4">
                      {opportunity.tags.map((tag, index) => (
                        <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2 ml-4">
                    <button className="btn-primary text-sm px-4 py-2">
                      <Rocket className="w-4 h-4 mr-2" />
                      Implement
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

        {/* Enhanced Budget Management */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Budget vs Actual with AI Forecasting</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="text-sm font-medium text-gray-900">Monthly Budget</p>
                  <p className="text-xs text-gray-500">Target spending</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-gray-900">$135,000</p>
                  <p className="text-xs text-gray-500">100%</p>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div>
                  <p className="text-sm font-medium text-gray-900">Actual Spend</p>
                  <p className="text-xs text-gray-500">Current month</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-green-600">${(advancedFinOpsMetrics.totalSpend/100).toFixed(2)}</p>
                  <p className="text-xs text-green-600">92.2%</p>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <div>
                  <p className="text-sm font-medium text-gray-900">Remaining</p>
                  <p className="text-xs text-gray-500">Available budget</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-blue-600">$10,500</p>
                  <p className="text-xs text-blue-600">7.8%</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">AI-Powered Forecast vs Actual</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Forecast Accuracy</span>
                <span className="text-sm font-medium text-gray-900">{advancedFinOpsMetrics.forecasts.confidence}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-green-600 h-2 rounded-full" style={{ width: `${advancedFinOpsMetrics.forecasts.confidence}%` }}></div>
              </div>
              
              <div className="grid grid-cols-2 gap-4 mt-4">
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-500">Next Month</p>
                  <p className="text-lg font-bold text-gray-900">${(advancedFinOpsMetrics.forecasts.nextMonth/100).toFixed(2)}</p>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-500">Next Quarter</p>
                  <p className="text-lg font-bold text-gray-900">${(advancedFinOpsMetrics.forecasts.nextQuarter/100).toFixed(2)}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
} 