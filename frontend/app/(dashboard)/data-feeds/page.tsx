'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Progress } from '@/components/ui/progress'
import { Separator } from '@/components/ui/separator'
import { 
  Database, 
  Zap, 
  Globe, 
  Activity, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  RefreshCw,
  Settings,
  Webhook,
  Pipeline,
  BarChart3,
  Brain,
  Target,
  Eye,
  Clock,
  ArrowRight,
  Play,
  Pause,
  RotateCcw
} from 'lucide-react'
import { dataFeedsApi } from '@/lib/api/client'

interface RealTimeFeedsStatus {
  active_feeds: number
  streaming_pipelines: number
  webhook_handlers: number
  data_quality_score: number
  processing_latency: number
  throughput: number
  feed_types: {
    cost: number
    security: number
    performance: number
    infrastructure: number
    threat_intelligence: number
  }
  ai_processing: {
    anomaly_detection_enabled: boolean
    pattern_recognition_enabled: boolean
    real_time_processing: boolean
    data_quality_threshold: number
  }
}

interface IntegrationsStatus {
  total_integrations: number
  active_integrations: number
  integration_types: {
    siem: number
    itsm: number
    communication: number
    ticketing: number
    cloud_provider: number
  }
  providers: Array<{
    name: string
    status: string
    last_sync: string
    data_volume: string
  }>
  webhook_metrics: {
    total_webhooks: number
    active_webhooks: number
    webhook_success_rate: number
    average_response_time: number
  }
}

interface DataPipelineMetrics {
  etl_pipelines: {
    total_pipelines: number
    active_pipelines: number
    success_rate: number
    average_processing_time: number
  }
  data_quality: {
    overall_score: number
    completeness: number
    accuracy: number
    consistency: number
    timeliness: number
  }
  data_lineage: {
    tracked_sources: number
    tracked_transformations: number
    tracked_destinations: number
    lineage_completeness: number
  }
  automated_refresh: {
    scheduled_jobs: number
    successful_refreshes: number
    failed_refreshes: number
    success_rate: number
  }
  ai_enhanced_processing: {
    anomaly_detections: number
    pattern_discoveries: number
    automated_corrections: number
    data_enrichment_applications: number
  }
}

export default function DataFeedsDashboard() {
  const [realTimeFeedsStatus, setRealTimeFeedsStatus] = useState<RealTimeFeedsStatus | null>(null)
  const [integrationsStatus, setIntegrationsStatus] = useState<IntegrationsStatus | null>(null)
  const [dataPipelineMetrics, setDataPipelineMetrics] = useState<DataPipelineMetrics | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    loadDataFeedsData()
    const interval = setInterval(loadDataFeedsData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const loadDataFeedsData = async () => {
    try {
      setIsLoading(true)
      const [feedsData, integrationsData, pipelineData] = await Promise.all([
        dataFeedsApi.getRealTimeFeedsStatus(),
        dataFeedsApi.getIntegrationsStatus(),
        dataFeedsApi.getDataPipelineMetrics()
      ])

      setRealTimeFeedsStatus(feedsData.data)
      setIntegrationsStatus(integrationsData.data)
      setDataPipelineMetrics(pipelineData.data)
    } catch (error) {
      console.error('Error loading data feeds data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const formatLatency = (latency: number) => {
    return `${(latency * 1000).toFixed(0)}ms`
  }

  const formatThroughput = (throughput: number) => {
    return `${throughput.toLocaleString()}/s`
  }

  const formatDataVolume = (volume: string) => {
    return volume
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
          <h1 className="text-3xl font-bold tracking-tight">Data Feeds & Integrations</h1>
          <p className="text-muted-foreground">
            Real-time streaming, third-party integrations, and automated data pipelines
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={loadDataFeedsData}>
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
      {realTimeFeedsStatus && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Feeds</CardTitle>
              <Database className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{realTimeFeedsStatus.active_feeds}</div>
              <p className="text-xs text-muted-foreground">
                Streaming pipelines: {realTimeFeedsStatus.streaming_pipelines}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Data Quality</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{realTimeFeedsStatus.data_quality_score.toFixed(1)}%</div>
              <p className="text-xs text-muted-foreground">
                Processing latency: {formatLatency(realTimeFeedsStatus.processing_latency)}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Throughput</CardTitle>
              <Activity className="h-4 w-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{formatThroughput(realTimeFeedsStatus.throughput)}</div>
              <p className="text-xs text-muted-foreground">
                Webhook handlers: {realTimeFeedsStatus.webhook_handlers}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">AI Processing</CardTitle>
              <Brain className="h-4 w-4 text-orange-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {realTimeFeedsStatus.ai_processing.anomaly_detection_enabled ? 'Active' : 'Inactive'}
              </div>
              <p className="text-xs text-muted-foreground">
                Pattern recognition: {realTimeFeedsStatus.ai_processing.pattern_recognition_enabled ? 'On' : 'Off'}
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
          <TabsTrigger value="pipelines">Pipelines</TabsTrigger>
          <TabsTrigger value="quality">Data Quality</TabsTrigger>
          <TabsTrigger value="lineage">Data Lineage</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Feed Types */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Database className="h-5 w-5 mr-2" />
                  Feed Types Distribution
                </CardTitle>
              </CardHeader>
              <CardContent>
                {realTimeFeedsStatus && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Cost Feeds</span>
                      <Badge variant="outline">{realTimeFeedsStatus.feed_types.cost}</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Security Feeds</span>
                      <Badge variant="outline">{realTimeFeedsStatus.feed_types.security}</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Performance Feeds</span>
                      <Badge variant="outline">{realTimeFeedsStatus.feed_types.performance}</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Infrastructure Feeds</span>
                      <Badge variant="outline">{realTimeFeedsStatus.feed_types.infrastructure}</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Threat Intelligence</span>
                      <Badge variant="outline">{realTimeFeedsStatus.feed_types.threat_intelligence}</Badge>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* AI Processing Status */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="h-5 w-5 mr-2" />
                  AI Processing Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                {realTimeFeedsStatus && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Anomaly Detection</span>
                      <Badge className={realTimeFeedsStatus.ai_processing.anomaly_detection_enabled ? "bg-green-500" : "bg-red-500"}>
                        {realTimeFeedsStatus.ai_processing.anomaly_detection_enabled ? "Enabled" : "Disabled"}
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Pattern Recognition</span>
                      <Badge className={realTimeFeedsStatus.ai_processing.pattern_recognition_enabled ? "bg-green-500" : "bg-red-500"}>
                        {realTimeFeedsStatus.ai_processing.pattern_recognition_enabled ? "Enabled" : "Disabled"}
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Real-time Processing</span>
                      <Badge className={realTimeFeedsStatus.ai_processing.real_time_processing ? "bg-green-500" : "bg-red-500"}>
                        {realTimeFeedsStatus.ai_processing.real_time_processing ? "Active" : "Inactive"}
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Quality Threshold</span>
                      <span className="font-medium">{(realTimeFeedsStatus.ai_processing.data_quality_threshold * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Integrations Tab */}
        <TabsContent value="integrations" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Integration Status */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Globe className="h-5 w-5 mr-2" />
                  Integration Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                {integrationsStatus && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Total Integrations</span>
                      <span className="font-medium">{integrationsStatus.total_integrations}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Active Integrations</span>
                      <span className="font-medium text-green-600">{integrationsStatus.active_integrations}</span>
                    </div>
                    <Separator />
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span>SIEM Integrations</span>
                        <Badge variant="outline">{integrationsStatus.integration_types.siem}</Badge>
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <span>ITSM Integrations</span>
                        <Badge variant="outline">{integrationsStatus.integration_types.itsm}</Badge>
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <span>Communication</span>
                        <Badge variant="outline">{integrationsStatus.integration_types.communication}</Badge>
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <span>Ticketing</span>
                        <Badge variant="outline">{integrationsStatus.integration_types.ticketing}</Badge>
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <span>Cloud Providers</span>
                        <Badge variant="outline">{integrationsStatus.integration_types.cloud_provider}</Badge>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Webhook Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Webhook className="h-5 w-5 mr-2" />
                  Webhook Metrics
                </CardTitle>
              </CardHeader>
              <CardContent>
                {integrationsStatus && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Total Webhooks</span>
                      <span className="font-medium">{integrationsStatus.webhook_metrics.total_webhooks}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Active Webhooks</span>
                      <span className="font-medium text-green-600">{integrationsStatus.webhook_metrics.active_webhooks}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Success Rate</span>
                      <span className="font-medium">{integrationsStatus.webhook_metrics.webhook_success_rate}%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Avg Response Time</span>
                      <span className="font-medium">{integrationsStatus.webhook_metrics.average_response_time}ms</span>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Integration Providers */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Globe className="h-5 w-5 mr-2" />
                Integration Providers
              </CardTitle>
            </CardHeader>
            <CardContent>
              {integrationsStatus && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {integrationsStatus.providers.map((provider) => (
                    <div key={provider.name} className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">{provider.name}</span>
                        <Badge className={provider.status === 'active' ? "bg-green-500" : "bg-red-500"}>
                          {provider.status}
                        </Badge>
                      </div>
                      <div className="text-sm text-muted-foreground space-y-1">
                        <div>Last sync: {new Date(provider.last_sync).toLocaleTimeString()}</div>
                        <div>Data volume: {provider.data_volume}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Pipelines Tab */}
        <TabsContent value="pipelines" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* ETL Pipelines */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Pipeline className="h-5 w-5 mr-2" />
                  ETL Pipelines
                </CardTitle>
              </CardHeader>
              <CardContent>
                {dataPipelineMetrics && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Total Pipelines</span>
                      <span className="font-medium">{dataPipelineMetrics.etl_pipelines.total_pipelines}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Active Pipelines</span>
                      <span className="font-medium text-green-600">{dataPipelineMetrics.etl_pipelines.active_pipelines}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Success Rate</span>
                      <span className="font-medium">{dataPipelineMetrics.etl_pipelines.success_rate}%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Avg Processing Time</span>
                      <span className="font-medium">{dataPipelineMetrics.etl_pipelines.average_processing_time}s</span>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* AI Enhanced Processing */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="h-5 w-5 mr-2" />
                  AI Enhanced Processing
                </CardTitle>
              </CardHeader>
              <CardContent>
                {dataPipelineMetrics && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Anomaly Detections</span>
                      <span className="font-medium">{dataPipelineMetrics.ai_enhanced_processing.anomaly_detections}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Pattern Discoveries</span>
                      <span className="font-medium">{dataPipelineMetrics.ai_enhanced_processing.pattern_discoveries}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Automated Corrections</span>
                      <span className="font-medium">{dataPipelineMetrics.ai_enhanced_processing.automated_corrections}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Data Enrichment</span>
                      <span className="font-medium">{dataPipelineMetrics.ai_enhanced_processing.data_enrichment_applications}</span>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Automated Refresh */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <RotateCcw className="h-5 w-5 mr-2" />
                Automated Refresh Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              {dataPipelineMetrics && (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold">{dataPipelineMetrics.automated_refresh.scheduled_jobs}</div>
                      <div className="text-xs text-muted-foreground">Scheduled Jobs</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">{dataPipelineMetrics.automated_refresh.successful_refreshes}</div>
                      <div className="text-xs text-muted-foreground">Successful</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-red-600">{dataPipelineMetrics.automated_refresh.failed_refreshes}</div>
                      <div className="text-xs text-muted-foreground">Failed</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold">{dataPipelineMetrics.automated_refresh.success_rate}%</div>
                      <div className="text-xs text-muted-foreground">Success Rate</div>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Data Quality Tab */}
        <TabsContent value="quality" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Data Quality Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="h-5 w-5 mr-2" />
                  Data Quality Metrics
                </CardTitle>
              </CardHeader>
              <CardContent>
                {dataPipelineMetrics && (
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Overall Score</span>
                        <span>{dataPipelineMetrics.data_quality.overall_score}/100</span>
                      </div>
                      <Progress value={dataPipelineMetrics.data_quality.overall_score} className="h-2" />
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Completeness</span>
                        <span>{dataPipelineMetrics.data_quality.completeness}/100</span>
                      </div>
                      <Progress value={dataPipelineMetrics.data_quality.completeness} className="h-2" />
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Accuracy</span>
                        <span>{dataPipelineMetrics.data_quality.accuracy}/100</span>
                      </div>
                      <Progress value={dataPipelineMetrics.data_quality.accuracy} className="h-2" />
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Consistency</span>
                        <span>{dataPipelineMetrics.data_quality.consistency}/100</span>
                      </div>
                      <Progress value={dataPipelineMetrics.data_quality.consistency} className="h-2" />
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Timeliness</span>
                        <span>{dataPipelineMetrics.data_quality.timeliness}/100</span>
                      </div>
                      <Progress value={dataPipelineMetrics.data_quality.timeliness} className="h-2" />
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Data Lineage */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BarChart3 className="h-5 w-5 mr-2" />
                  Data Lineage
                </CardTitle>
              </CardHeader>
              <CardContent>
                {dataPipelineMetrics && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Tracked Sources</span>
                      <span className="font-medium">{dataPipelineMetrics.data_lineage.tracked_sources}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Tracked Transformations</span>
                      <span className="font-medium">{dataPipelineMetrics.data_lineage.tracked_transformations}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Tracked Destinations</span>
                      <span className="font-medium">{dataPipelineMetrics.data_lineage.tracked_destinations}</span>
                    </div>
                    <Separator />
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Lineage Completeness</span>
                        <span>{dataPipelineMetrics.data_lineage.lineage_completeness}%</span>
                      </div>
                      <Progress value={dataPipelineMetrics.data_lineage.lineage_completeness} className="h-2" />
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Data Lineage Tab */}
        <TabsContent value="lineage" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <BarChart3 className="h-5 w-5 mr-2" />
                Data Flow Visualization
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {/* Sources */}
                <div>
                  <h3 className="font-medium mb-3">Data Sources</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">AWS Cost Explorer</span>
                        <Badge className="bg-blue-500">Real-time</Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Cloud provider cost data
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">Security Scanners</span>
                        <Badge className="bg-green-500">Hourly</Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Security vulnerability data
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">Performance Monitors</span>
                        <Badge className="bg-purple-500">Real-time</Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        System performance metrics
                      </div>
                    </div>
                  </div>
                </div>

                {/* Transformations */}
                <div>
                  <h3 className="font-medium mb-3">Data Transformations</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">Cost Normalization</span>
                        <Badge variant="outline">Processing</Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Normalize cost data across providers
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">Security Correlation</span>
                        <Badge variant="outline">AI Analysis</Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Correlate security events and threats
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">Performance Aggregation</span>
                        <Badge variant="outline">Aggregation</Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Aggregate performance metrics
                      </div>
                    </div>
                  </div>
                </div>

                {/* Destinations */}
                <div>
                  <h3 className="font-medium mb-3">Data Destinations</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">Cost Analysis Dashboard</span>
                        <Badge className="bg-blue-500">Visualization</Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Real-time cost analysis and insights
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">Security Alerts</span>
                        <Badge className="bg-red-500">Notification</Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Near real-time security alerts
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">Performance Reports</span>
                        <Badge className="bg-green-500">Reporting</Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Hourly performance reports
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
} 