'use client'

import { useState, useEffect } from 'react'
import DashboardLayout from '@/components/layouts/DashboardLayout'
import { 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  DollarSign,
  Shield,
  Activity,
  BarChart3,
  PieChart,
  LineChart,
  RefreshCw,
  AlertCircle,
  Users,
  Globe,
  Database,
  Cpu,
  Memory,
  HardDrive,
  Network,
  Zap,
  Target,
  Award,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Minus,
  Eye,
  EyeOff,
  Settings,
  Download,
  Share2,
  Filter,
  Calendar,
  Clock as ClockIcon,
  Star,
  StarHalf,
  StarOff
} from 'lucide-react'

interface ExecutiveMetrics {
  revenue: {
    current: number
    previous: number
    trend: 'up' | 'down' | 'stable'
    percentage: number
  }
  users: {
    total: number
    active: number
    new: number
    growth: number
  }
  performance: {
    uptime: number
    response_time: number
    error_rate: number
    throughput: number
  }
  security: {
    score: number
    vulnerabilities: number
    incidents: number
    compliance: string
  }
  costs: {
    total: number
    savings: number
    optimization: number
    forecast: number
  }
  ai_insights: {
    total: number
    high_priority: number
    implemented: number
    accuracy: number
  }
}

interface RealTimeMetric {
  name: string
  value: number
  unit: string
  trend: 'up' | 'down' | 'stable'
  change: number
  status: 'healthy' | 'warning' | 'critical'
}

interface Alert {
  id: string
  type: 'security' | 'performance' | 'cost' | 'ai'
  severity: 'low' | 'medium' | 'high' | 'critical'
  title: string
  description: string
  timestamp: string
  resolved: boolean
}

export default function MasterDashboardPage() {
  const [selectedPeriod, setSelectedPeriod] = useState('30d')
  const [refreshInterval, setRefreshInterval] = useState(30)
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [showAdvancedMetrics, setShowAdvancedMetrics] = useState(false)
  const [metrics, setMetrics] = useState<ExecutiveMetrics | null>(null)
  const [realTimeMetrics, setRealTimeMetrics] = useState<RealTimeMetric[]>([])
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Simulate real-time data updates
  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true)
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Mock executive metrics
        const mockMetrics: ExecutiveMetrics = {
          revenue: {
            current: 2847500,
            previous: 2650000,
            trend: 'up',
            percentage: 7.45
          },
          users: {
            total: 15420,
            active: 12850,
            new: 1250,
            growth: 8.8
          },
          performance: {
            uptime: 99.97,
            response_time: 145,
            error_rate: 0.03,
            throughput: 1250
          },
          security: {
            score: 98,
            vulnerabilities: 2,
            incidents: 0,
            compliance: 'SOC2, HIPAA, ISO27001'
          },
          costs: {
            total: 125000,
            savings: 45000,
            optimization: 26.5,
            forecast: 98000
          },
          ai_insights: {
            total: 156,
            high_priority: 23,
            implemented: 89,
            accuracy: 94.2
          }
        }
        
        setMetrics(mockMetrics)
        
        // Mock real-time metrics
        const mockRealTimeMetrics: RealTimeMetric[] = [
          {
            name: 'Active Users',
            value: 12850,
            unit: 'users',
            trend: 'up',
            change: 2.3,
            status: 'healthy'
          },
          {
            name: 'Response Time',
            value: 145,
            unit: 'ms',
            trend: 'down',
            change: -5.2,
            status: 'healthy'
          },
          {
            name: 'CPU Usage',
            value: 68,
            unit: '%',
            trend: 'up',
            change: 3.1,
            status: 'warning'
          },
          {
            name: 'Memory Usage',
            value: 72,
            unit: '%',
            trend: 'up',
            change: 1.8,
            status: 'healthy'
          },
          {
            name: 'Database Connections',
            value: 45,
            unit: 'connections',
            trend: 'stable',
            change: 0,
            status: 'healthy'
          },
          {
            name: 'Error Rate',
            value: 0.03,
            unit: '%',
            trend: 'down',
            change: -0.01,
            status: 'healthy'
          }
        ]
        
        setRealTimeMetrics(mockRealTimeMetrics)
        
        // Mock alerts
        const mockAlerts: Alert[] = [
          {
            id: '1',
            type: 'performance',
            severity: 'medium',
            title: 'High CPU Usage Detected',
            description: 'CPU usage has increased to 68% in the last 5 minutes',
            timestamp: new Date().toISOString(),
            resolved: false
          },
          {
            id: '2',
            type: 'ai',
            severity: 'low',
            title: 'New AI Insight Available',
            description: 'AI has identified a potential cost optimization opportunity',
            timestamp: new Date(Date.now() - 300000).toISOString(),
            resolved: false
          }
        ]
        
        setAlerts(mockAlerts)
        setError(null)
        
      } catch (err) {
        setError('Failed to load dashboard data')
        console.error('Dashboard data fetch error:', err)
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()

    // Set up auto-refresh
    if (autoRefresh) {
      const interval = setInterval(fetchData, refreshInterval * 1000)
      return () => clearInterval(interval)
    }
  }, [refreshInterval, autoRefresh])

  const getTrendIcon = (trend: 'up' | 'down' | 'stable') => {
    switch (trend) {
      case 'up':
        return <TrendingUpIcon className="w-4 h-4 text-green-500" />
      case 'down':
        return <TrendingDownIcon className="w-4 h-4 text-red-500" />
      default:
        return <Minus className="w-4 h-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-600 bg-green-100'
      case 'warning':
        return 'text-yellow-600 bg-yellow-100'
      case 'critical':
        return 'text-red-600 bg-red-100'
      default:
        return 'text-gray-600 bg-gray-100'
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'border-red-500 bg-red-50'
      case 'high':
        return 'border-orange-500 bg-orange-50'
      case 'medium':
        return 'border-yellow-500 bg-yellow-50'
      case 'low':
        return 'border-blue-500 bg-blue-50'
      default:
        return 'border-gray-500 bg-gray-50'
    }
  }

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="flex items-center space-x-2">
            <RefreshCw className="w-5 h-5 animate-spin text-blue-600" />
            <span className="text-gray-600">Loading executive dashboard...</span>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Error Loading Dashboard</h3>
            <p className="text-gray-600 mb-4">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="btn-primary"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Retry
            </button>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Executive Dashboard</h1>
            <p className="text-gray-600">Real-time business intelligence and system health overview</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setAutoRefresh(!autoRefresh)}
                className={`p-2 rounded-lg ${autoRefresh ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'}`}
                title={autoRefresh ? 'Auto-refresh enabled' : 'Auto-refresh disabled'}
              >
                {autoRefresh ? <RefreshCw className="w-4 h-4" /> : <ClockIcon className="w-4 h-4" />}
              </button>
              <select
                value={refreshInterval}
                onChange={(e) => setRefreshInterval(Number(e.target.value))}
                className="input-field text-sm"
              >
                <option value={15}>15s</option>
                <option value={30}>30s</option>
                <option value={60}>1m</option>
                <option value={300}>5m</option>
              </select>
            </div>
            <button
              onClick={() => setShowAdvancedMetrics(!showAdvancedMetrics)}
              className="btn-secondary"
            >
              {showAdvancedMetrics ? <EyeOff className="w-4 h-4 mr-2" /> : <Eye className="w-4 h-4 mr-2" />}
              {showAdvancedMetrics ? 'Hide' : 'Show'} Advanced
            </button>
            <select
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
              className="input-field"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
            </select>
          </div>
        </div>

        {/* Key Performance Indicators */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Revenue */}
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Revenue</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${metrics?.revenue.current.toLocaleString() || '0'}
                </p>
                <div className="flex items-center mt-1">
                  {getTrendIcon(metrics?.revenue.trend || 'stable')}
                  <span className={`text-sm ${metrics?.revenue.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                    {metrics?.revenue.percentage || 0}% from last period
                  </span>
                </div>
              </div>
              <div className="p-3 bg-green-100 rounded-lg">
                <DollarSign className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>

          {/* Users */}
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Users</p>
                <p className="text-2xl font-bold text-gray-900">
                  {metrics?.users.active.toLocaleString() || '0'}
                </p>
                <div className="flex items-center mt-1">
                  {getTrendIcon('up')}
                  <span className="text-sm text-green-600">
                    +{metrics?.users.growth || 0}% growth
                  </span>
                </div>
              </div>
              <div className="p-3 bg-blue-100 rounded-lg">
                <Users className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          {/* Performance */}
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Uptime</p>
                <p className="text-2xl font-bold text-gray-900">
                  {metrics?.performance.uptime || 0}%
                </p>
                <div className="flex items-center mt-1">
                  <span className="text-sm text-green-600">
                    {metrics?.performance.response_time || 0}ms avg response
                  </span>
                </div>
              </div>
              <div className="p-3 bg-purple-100 rounded-lg">
                <Activity className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </div>

          {/* Security Score */}
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Security Score</p>
                <p className="text-2xl font-bold text-gray-900">
                  {metrics?.security.score || 0}/100
                </p>
                <div className="flex items-center mt-1">
                  <span className="text-sm text-green-600">
                    {metrics?.security.vulnerabilities || 0} vulnerabilities
                  </span>
                </div>
              </div>
              <div className="p-3 bg-red-100 rounded-lg">
                <Shield className="w-6 h-6 text-red-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Real-time Metrics Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* System Health */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">System Health</h3>
              <div className="flex items-center space-x-2">
                <Cpu className="w-4 h-4 text-gray-400" />
                <span className="text-sm text-gray-500">Real-time</span>
              </div>
            </div>
            <div className="space-y-4">
              {realTimeMetrics.slice(0, 3).map((metric) => (
                <div key={metric.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${getStatusColor(metric.status).split(' ')[1]}`}></div>
                    <span className="text-sm font-medium text-gray-700">{metric.name}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-bold text-gray-900">
                      {metric.value.toLocaleString()}{metric.unit}
                    </span>
                    <div className="flex items-center space-x-1">
                      {getTrendIcon(metric.trend)}
                      <span className={`text-xs ${metric.trend === 'up' ? 'text-green-600' : metric.trend === 'down' ? 'text-red-600' : 'text-gray-600'}`}>
                        {metric.change > 0 ? '+' : ''}{metric.change}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Cost Optimization */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Cost Optimization</h3>
              <Target className="w-4 h-4 text-gray-400" />
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Total Cost</span>
                <span className="text-sm font-bold text-gray-900">${metrics?.costs.total.toLocaleString() || '0'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Savings</span>
                <span className="text-sm font-bold text-green-600">${metrics?.costs.savings.toLocaleString() || '0'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Optimization</span>
                <span className="text-sm font-bold text-blue-600">{metrics?.costs.optimization || 0}%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Forecast</span>
                <span className="text-sm font-bold text-purple-600">${metrics?.costs.forecast.toLocaleString() || '0'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* AI Insights & Alerts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* AI Insights */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">AI Insights</h3>
              <Zap className="w-4 h-4 text-gray-400" />
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Total Insights</span>
                <span className="text-sm font-bold text-gray-900">{metrics?.ai_insights.total || 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">High Priority</span>
                <span className="text-sm font-bold text-red-600">{metrics?.ai_insights.high_priority || 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Implemented</span>
                <span className="text-sm font-bold text-green-600">{metrics?.ai_insights.implemented || 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Accuracy</span>
                <span className="text-sm font-bold text-blue-600">{metrics?.ai_insights.accuracy || 0}%</span>
              </div>
            </div>
          </div>

          {/* Active Alerts */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Active Alerts</h3>
              <AlertTriangle className="w-4 h-4 text-gray-400" />
            </div>
            <div className="space-y-3">
              {alerts.length > 0 ? (
                alerts.map((alert) => (
                  <div key={alert.id} className={`p-3 rounded-lg border-l-4 ${getSeverityColor(alert.severity)}`}>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">{alert.title}</p>
                        <p className="text-xs text-gray-600 mt-1">{alert.description}</p>
                        <p className="text-xs text-gray-500 mt-2">
                          {new Date(alert.timestamp).toLocaleString()}
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          alert.severity === 'critical' ? 'bg-red-100 text-red-800' :
                          alert.severity === 'high' ? 'bg-orange-100 text-orange-800' :
                          alert.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-blue-100 text-blue-800'
                        }`}>
                          {alert.severity}
                        </span>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-4">
                  <CheckCircle className="w-8 h-8 text-green-500 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">No active alerts</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Advanced Metrics (Conditional) */}
        {showAdvancedMetrics && (
          <div className="card">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900">Advanced System Metrics</h3>
              <div className="flex items-center space-x-2">
                <Settings className="w-4 h-4 text-gray-400" />
                <span className="text-sm text-gray-500">Technical Details</span>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {realTimeMetrics.slice(3).map((metric) => (
                <div key={metric.name} className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">{metric.name}</span>
                    <div className={`w-2 h-2 rounded-full ${getStatusColor(metric.status).split(' ')[1]}`}></div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-lg font-bold text-gray-900">
                      {metric.value.toLocaleString()}{metric.unit}
                    </span>
                    <div className="flex items-center space-x-1">
                      {getTrendIcon(metric.trend)}
                      <span className={`text-xs ${metric.trend === 'up' ? 'text-green-600' : metric.trend === 'down' ? 'text-red-600' : 'text-gray-600'}`}>
                        {metric.change > 0 ? '+' : ''}{metric.change}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button className="flex items-center space-x-3 p-4 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors duration-200">
              <BarChart3 className="w-5 h-5 text-blue-600" />
              <span className="text-sm font-medium text-blue-900">Generate Report</span>
            </button>
            <button className="flex items-center space-x-3 p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors duration-200">
              <Shield className="w-5 h-5 text-green-600" />
              <span className="text-sm font-medium text-green-900">Security Scan</span>
            </button>
            <button className="flex items-center space-x-3 p-4 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors duration-200">
              <Zap className="w-5 h-5 text-purple-600" />
              <span className="text-sm font-medium text-purple-900">AI Analysis</span>
            </button>
            <button className="flex items-center space-x-3 p-4 bg-yellow-50 hover:bg-yellow-100 rounded-lg transition-colors duration-200">
              <Download className="w-5 h-5 text-yellow-600" />
              <span className="text-sm font-medium text-yellow-900">Export Data</span>
            </button>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
} 