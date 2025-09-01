'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Progress } from '@/components/ui/progress'
import { Separator } from '@/components/ui/separator'
import { 
  Activity, 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  TrendingUp, 
  TrendingDown,
  Zap,
  Shield,
  Database,
  Server,
  Globe,
  BarChart3,
  Gauge,
  Target,
  Eye,
  Brain,
  AlertCircle,
  RefreshCw,
  Play,
  Pause,
  Settings,
  Users
} from 'lucide-react'
import { monitoringApi, autoHealingApi } from '@/lib/api/client'

interface RealTimeMetrics {
  system_health: {
    uptime: number
    response_time_p95: number
    error_rate: number
    throughput: number
    active_users: number
    cost_savings: number
    security_score: number
    infrastructure_health: number
  }
  ai_insights: {
    anomalies_detected: number
    predictions_made: number
    accuracy_rate: number
    optimization_opportunities: number
    threats_prevented: number
  }
  business_kpis: {
    cost_efficiency: number
    security_posture: number
    performance_score: number
    user_satisfaction: number
    system_uptime: number
  }
  alerts: {
    active: number
    critical: number
    resolved_today: number
  }
}

interface ServiceHealth {
  name: string
  status: string
  health_score: number
  response_time: number
  error_rate: number
}

interface MonitoringAlert {
  id: string
  title: string
  message: string
  severity: string
  category: string
  timestamp: string
  resolved: boolean
  ai_insights?: string
}

export default function MonitoringDashboard() {
  const [realTimeMetrics, setRealTimeMetrics] = useState<RealTimeMetrics | null>(null)
  const [serviceHealth, setServiceHealth] = useState<ServiceHealth[]>([])
  const [alerts, setAlerts] = useState<MonitoringAlert[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    loadMonitoringData()
    const interval = setInterval(loadMonitoringData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const loadMonitoringData = async () => {
    try {
      setIsLoading(true)
      const [metricsData, alertsData, servicesData] = await Promise.all([
        monitoringApi.getRealTimeMetrics(),
        monitoringApi.getAlerts(),
        autoHealingApi.getAllServicesHealth()
      ])

      setRealTimeMetrics(metricsData.data)
      setAlerts(alertsData.data.alerts || [])
      setServiceHealth(servicesData.data.services || [])
    } catch (error) {
      console.error('Error loading monitoring data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'healthy':
        return 'bg-green-500'
      case 'degraded':
        return 'bg-yellow-500'
      case 'unhealthy':
        return 'bg-orange-500'
      case 'critical':
        return 'bg-red-500'
      default:
        return 'bg-gray-500'
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return 'bg-red-500 text-white'
      case 'warning':
        return 'bg-yellow-500 text-white'
      case 'info':
        return 'bg-blue-500 text-white'
      default:
        return 'bg-gray-500 text-white'
    }
  }

  const formatUptime = (uptime: number) => {
    return `${uptime.toFixed(2)}%`
  }

  const formatResponseTime = (time: number) => {
    return `${(time * 1000).toFixed(0)}ms`
  }

  const formatErrorRate = (rate: number) => {
    return `${(rate * 100).toFixed(2)}%`
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Monitoring Dashboard</h1>
          <p className="text-muted-foreground">
            Real-time system monitoring with AI-powered insights
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={loadMonitoringData}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button variant="outline" size="sm">
            <Settings className="h-4 w-4 mr-2" />
            Settings
          </Button>
        </div>
      </div>

      {/* Real-time Metrics Overview */}
      {realTimeMetrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">System Uptime</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{formatUptime(realTimeMetrics.system_health.uptime)}</div>
              <p className="text-xs text-muted-foreground">
                Response time: {formatResponseTime(realTimeMetrics.system_health.response_time_p95)}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Users</CardTitle>
              <Users className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{realTimeMetrics.system_health.active_users}</div>
              <p className="text-xs text-muted-foreground">
                Throughput: {realTimeMetrics.system_health.throughput.toLocaleString()}/s
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Error Rate</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{formatErrorRate(realTimeMetrics.system_health.error_rate)}</div>
              <p className="text-xs text-muted-foreground">
                {realTimeMetrics.alerts.active} active alerts
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Cost Savings</CardTitle>
              <TrendingUp className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">${realTimeMetrics.system_health.cost_savings.toLocaleString()}</div>
              <p className="text-xs text-muted-foreground">
                Efficiency: {realTimeMetrics.business_kpis.cost_efficiency}%
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="services">Services</TabsTrigger>
          <TabsTrigger value="alerts">Alerts</TabsTrigger>
          <TabsTrigger value="ai-insights">AI Insights</TabsTrigger>
          <TabsTrigger value="tracing">Tracing</TabsTrigger>
          <TabsTrigger value="auto-healing">Auto-Healing</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* System Health */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Activity className="h-5 w-5 mr-2" />
                  System Health
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {realTimeMetrics && (
                  <>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Security Score</span>
                        <span>{realTimeMetrics.system_health.security_score}/100</span>
                      </div>
                      <Progress value={realTimeMetrics.system_health.security_score} className="h-2" />
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Infrastructure Health</span>
                        <span>{realTimeMetrics.system_health.infrastructure_health}/100</span>
                      </div>
                      <Progress value={realTimeMetrics.system_health.infrastructure_health} className="h-2" />
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Performance Score</span>
                        <span>{realTimeMetrics.business_kpis.performance_score}/100</span>
                      </div>
                      <Progress value={realTimeMetrics.business_kpis.performance_score} className="h-2" />
                    </div>
                  </>
                )}
              </CardContent>
            </Card>

            {/* AI Insights Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="h-5 w-5 mr-2" />
                  AI Insights
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {realTimeMetrics && (
                  <>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">
                          {realTimeMetrics.ai_insights.anomalies_detected}
                        </div>
                        <div className="text-xs text-muted-foreground">Anomalies Detected</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">
                          {realTimeMetrics.ai_insights.threats_prevented}
                        </div>
                        <div className="text-xs text-muted-foreground">Threats Prevented</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-purple-600">
                          {realTimeMetrics.ai_insights.optimization_opportunities}
                        </div>
                        <div className="text-xs text-muted-foreground">Optimization Opportunities</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-orange-600">
                          {(realTimeMetrics.ai_insights.accuracy_rate * 100).toFixed(1)}%
                        </div>
                        <div className="text-xs text-muted-foreground">AI Accuracy</div>
                      </div>
                    </div>
                  </>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Services Tab */}
        <TabsContent value="services" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Server className="h-5 w-5 mr-2" />
                Service Health Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {serviceHealth.map((service) => (
                  <div key={service.name} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-4">
                      <div className={`w-3 h-3 rounded-full ${getStatusColor(service.status)}`}></div>
                      <div>
                        <div className="font-medium">{service.name}</div>
                        <div className="text-sm text-muted-foreground">
                          Health: {service.health_score}/100
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm">
                        Response: {formatResponseTime(service.response_time)}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Error Rate: {formatErrorRate(service.error_rate)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Alerts Tab */}
        <TabsContent value="alerts" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <AlertCircle className="h-5 w-5 mr-2" />
                Active Alerts
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {alerts.filter(alert => !alert.resolved).map((alert) => (
                  <Alert key={alert.id} className="border-l-4 border-l-red-500">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium">{alert.title}</div>
                          <div className="text-sm text-muted-foreground">{alert.message}</div>
                          {alert.ai_insights && (
                            <div className="text-sm text-blue-600 mt-1">
                              AI Insight: {alert.ai_insights}
                            </div>
                          )}
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge className={getSeverityColor(alert.severity)}>
                            {alert.severity}
                          </Badge>
                          <Badge variant="outline">{alert.category}</Badge>
                        </div>
                      </div>
                    </AlertDescription>
                  </Alert>
                ))}
                {alerts.filter(alert => !alert.resolved).length === 0 && (
                  <div className="text-center py-8 text-muted-foreground">
                    <CheckCircle className="h-12 w-12 mx-auto mb-4 text-green-600" />
                    <p>No active alerts</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* AI Insights Tab */}
        <TabsContent value="ai-insights" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="h-5 w-5 mr-2" />
                  Predictive Analytics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">Cost Forecast</span>
                      <TrendingDown className="h-4 w-4 text-green-600" />
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Next month: $125,000 (92% confidence)
                    </div>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">Security Threats</span>
                      <Shield className="h-4 w-4 text-blue-600" />
                    </div>
                    <div className="text-sm text-muted-foreground">
                      8% probability (89% confidence)
                    </div>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">Performance</span>
                      <Gauge className="h-4 w-4 text-orange-600" />
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Scale up needed in 2 weeks (91% confidence)
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="h-5 w-5 mr-2" />
                  Optimization Recommendations
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">Right-size Resources</span>
                      <Badge className="bg-green-500">High Priority</Badge>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Potential savings: $8,500
                    </div>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">Add Caching Layer</span>
                      <Badge className="bg-yellow-500">Medium Priority</Badge>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Performance improvement: 25%
                    </div>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">Security Monitoring</span>
                      <Badge className="bg-red-500">Critical</Badge>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Risk reduction: 15%
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Tracing Tab */}
        <TabsContent value="tracing" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <BarChart3 className="h-5 w-5 mr-2" />
                Distributed Tracing
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center justify-between mb-4">
                    <span className="font-medium">Service Map</span>
                    <Badge variant="outline">5 Services</Badge>
                  </div>
                  <div className="grid grid-cols-5 gap-4 text-center">
                    <div className="p-2 border rounded">
                      <div className="font-medium">Frontend</div>
                      <div className="text-xs text-muted-foreground">98% Health</div>
                    </div>
                    <div className="p-2 border rounded">
                      <div className="font-medium">Backend</div>
                      <div className="text-xs text-muted-foreground">95% Health</div>
                    </div>
                    <div className="p-2 border rounded">
                      <div className="font-medium">Database</div>
                      <div className="text-xs text-muted-foreground">92% Health</div>
                    </div>
                    <div className="p-2 border rounded">
                      <div className="font-medium">Redis</div>
                      <div className="text-xs text-muted-foreground">96% Health</div>
                    </div>
                    <div className="p-2 border rounded">
                      <div className="font-medium">AI Engine</div>
                      <div className="text-xs text-muted-foreground">94% Health</div>
                    </div>
                  </div>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="font-medium mb-2">Recent Traces</div>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span>Cost Analysis Request</span>
                      <span className="text-muted-foreground">1.2s</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>Security Scan</span>
                      <span className="text-muted-foreground">0.8s</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>Infrastructure Sync</span>
                      <span className="text-muted-foreground">2.1s</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Auto-Healing Tab */}
        <TabsContent value="auto-healing" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Zap className="h-5 w-5 mr-2" />
                  Auto-Scaling Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span>Current Instances</span>
                    <span className="font-medium">5</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>CPU Utilization</span>
                    <span className="font-medium">65%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Memory Utilization</span>
                    <span className="font-medium">72%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Response Time</span>
                    <span className="font-medium">800ms</span>
                  </div>
                  <Separator />
                  <div className="text-sm text-muted-foreground">
                    <div className="flex items-center justify-between">
                      <span>Predicted Scaling Needs</span>
                      <span className="text-green-600">Stable</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>AI Confidence</span>
                      <span>89%</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <RefreshCw className="h-5 w-5 mr-2" />
                  Recovery History
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span>Total Recoveries</span>
                    <span className="font-medium">12</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Success Rate</span>
                    <span className="font-medium text-green-600">92%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Average Recovery Time</span>
                    <span className="font-medium">2.3s</span>
                  </div>
                  <Separator />
                  <div className="text-sm text-muted-foreground">
                    <div className="flex items-center justify-between">
                      <span>Retry Strategy</span>
                      <span>85% success</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Scale Up Strategy</span>
                      <span>88% success</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Rollback Strategy</span>
                      <span>95% success</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
} 