'use client'

import { useState, useEffect, useMemo } from 'react'
import DashboardLayout from '@/components/layouts/DashboardLayout'
import { useInfrastructures, useResources } from '@/lib/hooks/useApi'
import { 
  Globe, 
  Server, 
  Database, 
  Cloud, 
  Activity,
  Plus,
  Settings,
  Eye,
  EyeOff,
  RefreshCw,
  Download,
  Filter,
  Search,
  AlertTriangle,
  CheckCircle,
  Clock,
  BarChart3,
  PieChart,
  Network,
  HardDrive,
  Cpu,
  Memory,
  Brain,
  Zap,
  Target,
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
  Layers,
  Grid3X3,
  Cube,
  Monitor,
  Gauge,
  Thermometer,
  Wifi,
  Shield,
  Lock,
  Unlock
} from 'lucide-react'

interface InfrastructureResource {
  id: string
  name: string
  type: string
  region: string
  status: 'running' | 'stopped' | 'terminated' | 'starting' | 'stopping'
  instanceType: string
  cpu: number
  memory: number
  storage: number
  network: number
  cost: number
  tags: string[]
  securityScore: number
  efficiencyScore: number
  lastUpdated: string
  aiInsights: string[]
  recommendations: string[]
  performanceMetrics: {
    responseTime: number
    throughput: number
    errorRate: number
    availability: number
  }
}

interface RegionData {
  name: string
  resources: number
  cost: number
  performance: number
  availability: number
  latency: number
  securityScore: number
}

interface ServiceData {
  name: string
  count: number
  cost: number
  status: 'healthy' | 'warning' | 'critical' | 'degraded'
  performance: number
  efficiency: number
  recommendations: string[]
}

export default function InfrastructurePage() {
  const [selectedRegion, setSelectedRegion] = useState('all')
  const [selectedService, setSelectedService] = useState('all')
  const [viewMode, setViewMode] = useState('list')
  const [isLoading, setIsLoading] = useState(false)
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false)
  const [selectedResource, setSelectedResource] = useState<any | null>(null)
  const [selectedInfraId, setSelectedInfraId] = useState<string | null>(null)

  // Enhanced state for real-time monitoring
  const [realTimeMetrics, setRealTimeMetrics] = useState<any[]>([])
  const [aiInsights, setAiInsights] = useState<string[]>([])

  // Live infrastructure summary
  const infrastructures = useInfrastructures()
  const totalResourcesLive = (infrastructures.data || []).reduce(
    (sum: number, infra: any) => sum + (infra.total_resources || 0),
    0
  )
  const liveResources = useResources(selectedInfraId || undefined)

  // World-class infrastructure resources with AI insights
  const advancedResources: InfrastructureResource[] = [
    {
      id: 'web-server-01',
      name: 'web-server-01',
      type: 'EC2',
      region: 'us-east-1',
      status: 'running',
      instanceType: 't3.large',
      cpu: 85,
      memory: 60,
      storage: 40,
      network: 75,
      cost: 120,
      tags: ['production', 'web', 'frontend', 'auto-scaling'],
      securityScore: 92,
      efficiencyScore: 87,
      lastUpdated: '2024-01-15T10:30:00Z',
      aiInsights: [
        'CPU utilization trending upward - consider scaling',
        'Memory usage stable with 40% headroom',
        'Network performance optimal for current load',
        'Security posture excellent with no vulnerabilities'
      ],
      recommendations: [
        'Consider upgrading to t3.xlarge for better performance',
        'Implement auto-scaling based on CPU metrics',
        'Enable CloudWatch detailed monitoring',
        'Set up cost optimization alerts'
      ],
      performanceMetrics: {
        responseTime: 45,
        throughput: 1200,
        errorRate: 0.1,
        availability: 99.9
      }
    },
    {
      id: 'db-cluster-01',
      name: 'db-cluster-01',
      type: 'RDS',
      region: 'us-east-1',
      status: 'running',
      instanceType: 'db.r5.large',
      cpu: 45,
      memory: 75,
      storage: 80,
      network: 60,
      cost: 200,
      tags: ['production', 'database', 'postgresql', 'multi-az'],
      securityScore: 95,
      efficiencyScore: 82,
      lastUpdated: '2024-01-15T10:25:00Z',
      aiInsights: [
        'Database performance optimal for current workload',
        'Storage utilization high - consider archiving old data',
        'Connection pool utilization at 70% - healthy',
        'Backup and encryption properly configured'
      ],
      recommendations: [
        'Implement read replicas for better performance',
        'Enable automated storage scaling',
        'Set up performance insights monitoring',
        'Consider reserved instances for cost savings'
      ],
      performanceMetrics: {
        responseTime: 12,
        throughput: 850,
        errorRate: 0.05,
        availability: 99.95
      }
    },
    {
      id: 'cache-cluster-01',
      name: 'cache-cluster-01',
      type: 'ElastiCache',
      region: 'us-east-1',
      status: 'running',
      instanceType: 'cache.r5.large',
      cpu: 30,
      memory: 50,
      storage: 20,
      network: 85,
      cost: 80,
      tags: ['production', 'cache', 'redis', 'session-storage'],
      securityScore: 88,
      efficiencyScore: 91,
      lastUpdated: '2024-01-15T10:20:00Z',
      aiInsights: [
        'Cache hit rate excellent at 95%',
        'Memory usage optimal with good headroom',
        'Network latency minimal for cache operations',
        'Security groups properly configured'
      ],
      recommendations: [
        'Consider implementing cache warming strategies',
        'Monitor memory usage for potential scaling',
        'Enable encryption in transit',
        'Set up cache performance alerts'
      ],
      performanceMetrics: {
        responseTime: 2,
        throughput: 5000,
        errorRate: 0.02,
        availability: 99.8
      }
    },
    {
      id: 'storage-bucket-01',
      name: 'storage-bucket-01',
      type: 'S3',
      region: 'us-east-1',
      status: 'active',
      instanceType: 'Standard',
      cpu: 0,
      memory: 0,
      storage: 65,
      network: 90,
      cost: 45,
      tags: ['production', 'storage', 'static-assets', 'cdn'],
      securityScore: 96,
      efficiencyScore: 89,
      lastUpdated: '2024-01-15T10:15:00Z',
      aiInsights: [
        'Storage utilization moderate with good lifecycle policies',
        'Access patterns show optimal CDN usage',
        'Security configuration excellent with proper IAM',
        'Cost optimization opportunities identified'
      ],
      recommendations: [
        'Implement S3 lifecycle policies for cost optimization',
        'Enable intelligent tiering for infrequently accessed data',
        'Set up access logging for security monitoring',
        'Consider S3 Transfer Acceleration for uploads'
      ],
      performanceMetrics: {
        responseTime: 150,
        throughput: 800,
        errorRate: 0.01,
        availability: 99.99
      }
    }
  ]

  // Enhanced regions with performance data
  const advancedRegions: RegionData[] = [
    { name: 'us-east-1', resources: 12, cost: 850, performance: 95, availability: 99.9, latency: 25, securityScore: 94 },
    { name: 'us-west-2', resources: 8, cost: 620, performance: 92, availability: 99.8, latency: 45, securityScore: 91 },
    { name: 'eu-west-1', resources: 6, cost: 480, performance: 88, availability: 99.7, latency: 80, securityScore: 89 },
    { name: 'ap-southeast-1', resources: 4, cost: 320, performance: 85, availability: 99.6, latency: 120, securityScore: 87 }
  ]

  // Enhanced services with AI insights
  const advancedServices: ServiceData[] = [
    { 
      name: 'EC2', 
      count: 8, 
      cost: 450, 
      status: 'healthy', 
      performance: 92, 
      efficiency: 87,
      recommendations: [
        'Implement auto-scaling for better resource utilization',
        'Consider reserved instances for predictable workloads',
        'Enable detailed monitoring for performance optimization'
      ]
    },
    { 
      name: 'RDS', 
      count: 3, 
      cost: 280, 
      status: 'healthy', 
      performance: 95, 
      efficiency: 92,
      recommendations: [
        'Set up read replicas for better performance',
        'Enable automated backups and encryption',
        'Monitor connection pool utilization'
      ]
    },
    { 
      name: 'S3', 
      count: 5, 
      cost: 120, 
      status: 'healthy', 
      performance: 98, 
      efficiency: 89,
      recommendations: [
        'Implement lifecycle policies for cost optimization',
        'Enable intelligent tiering for infrequently accessed data',
        'Set up access logging for security monitoring'
      ]
    },
    { 
      name: 'ElastiCache', 
      count: 2, 
      cost: 80, 
      status: 'warning', 
      performance: 85, 
      efficiency: 91,
      recommendations: [
        'Monitor memory usage for potential scaling',
        'Implement cache warming strategies',
        'Enable encryption in transit'
      ]
    },
    { 
      name: 'CloudFront', 
      count: 1, 
      cost: 45, 
      status: 'healthy', 
      performance: 99, 
      efficiency: 95,
      recommendations: [
        'Optimize cache hit rates for better performance',
        'Enable real-time logs for monitoring',
        'Configure security headers for enhanced security'
      ]
    },
    { 
      name: 'Lambda', 
      count: 12, 
      cost: 25, 
      status: 'healthy', 
      performance: 88, 
      efficiency: 94,
      recommendations: [
        'Optimize function execution time',
        'Implement proper error handling and retries',
        'Use provisioned concurrency for consistent performance'
      ]
    }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
      case 'active':
      case 'healthy': return 'text-green-600 bg-green-100'
      case 'stopped':
      case 'inactive': return 'text-gray-600 bg-gray-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'critical': return 'text-red-600 bg-red-100'
      case 'degraded': return 'text-orange-600 bg-orange-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getResourceIcon = (type: string) => {
    switch (type) {
      case 'EC2': return <Server className="w-4 h-4" />
      case 'RDS': return <Database className="w-4 h-4" />
      case 'S3': return <HardDrive className="w-4 h-4" />
      case 'ElastiCache': return <Memory className="w-4 h-4" />
      case 'CloudFront': return <Network className="w-4 h-4" />
      case 'Lambda': return <Cpu className="w-4 h-4" />
      default: return <Cloud className="w-4 h-4" />
    }
  }

  const getUtilizationColor = (value: number) => {
    if (value >= 80) return 'text-red-600'
    if (value >= 60) return 'text-yellow-600'
    return 'text-green-600'
  }

  const getPerformanceColor = (value: number) => {
    if (value >= 90) return 'text-green-600'
    if (value >= 80) return 'text-yellow-600'
    return 'text-red-600'
  }

  // Real-time monitoring simulation
  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        // Simulate real-time metrics updates
        setRealTimeMetrics(prev => [...prev, {
          timestamp: new Date().toISOString(),
          cpu: Math.random() * 100,
          memory: Math.random() * 100,
          network: Math.random() * 100
        }])
        
        // Update AI insights
        setAiInsights([
          "🚀 **Performance Alert**: CPU utilization trending upward on web-server-01",
          "💡 **Optimization**: Consider auto-scaling for better resource utilization",
          "📊 **Efficiency**: Overall infrastructure efficiency at 87%",
          "🔒 **Security**: All resources have excellent security posture",
          "⚡ **Performance**: Response times within optimal ranges"
        ])
      }, 30000) // Update every 30 seconds

      return () => clearInterval(interval)
    }
  }, [autoRefresh])

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Enhanced Header with AI Insights */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Infrastructure Center</h1>
            <p className="text-gray-600">AI-powered infrastructure monitoring and optimization.</p>
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
              <span>Add Resource</span>
            </button>
          </div>
        </div>

        {/* AI Infrastructure Insights Banner */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center space-x-3">
            <Brain className="w-6 h-6 text-blue-600" />
            <div className="flex-1">
              <h3 className="font-semibold text-blue-900">AI Infrastructure Insights</h3>
              <p className="text-sm text-blue-700">{aiInsights[0] || "🚀 AI monitoring active - infrastructure performing optimally"}</p>
            </div>
            <button className="text-blue-600 hover:text-blue-700">
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Enhanced Infrastructure Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Resources</p>
                <p className="text-2xl font-bold text-gray-900">{infrastructures.isLoading ? '—' : totalResourcesLive || 0}</p>
                <div className="flex items-center mt-1">
                  <Activity className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">+2 this week</span>
                </div>
                <div className="flex items-center mt-1">
                  <Brain className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">AI optimized</span>
                </div>
              </div>
              <div className="p-3 bg-blue-100 rounded-lg">
                <Globe className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Performance Score</p>
                <p className="text-2xl font-bold text-gray-900">94%</p>
                <div className="flex items-center mt-1">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">Excellent</span>
                </div>
                <div className="flex items-center mt-1">
                  <Award className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">Above average</span>
                </div>
              </div>
              <div className="p-3 bg-green-100 rounded-lg">
                <Activity className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Efficiency Score</p>
                <p className="text-2xl font-bold text-gray-900">87%</p>
                <div className="flex items-center mt-1">
                  <Target className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">Optimized</span>
                </div>
                <div className="flex items-center mt-1">
                  <Star className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">AI recommended</span>
                </div>
              </div>
              <div className="p-3 bg-purple-100 rounded-lg">
                <Target className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Security Score</p>
                <p className="text-2xl font-bold text-gray-900">93%</p>
                <div className="flex items-center mt-1">
                  <Shield className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-600">Secure</span>
                </div>
                <div className="flex items-center mt-1">
                  <Lock className="w-3 h-3 text-gray-400 mr-1" />
                  <span className="text-xs text-gray-500">All resources</span>
                </div>
              </div>
              <div className="p-3 bg-yellow-100 rounded-lg">
                <Shield className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Live Infrastructures */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Live Infrastructures</h3>
              <p className="text-sm text-gray-600">Select an infrastructure to view resources.</p>
            </div>
          </div>
          {infrastructures.isLoading ? (
            <div className="min-h-[100px] flex items-center justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400" />
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {(infrastructures.data || []).map((infra: any) => (
                <button
                  key={infra.id}
                  onClick={() => setSelectedInfraId(infra.id)}
                  className={`border rounded-lg p-3 text-left hover:shadow ${selectedInfraId === infra.id ? 'border-blue-400 ring-1 ring-blue-300' : 'border-gray-200'}`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-gray-900">{infra.name}</span>
                    <span className="text-xs text-gray-600">{infra.cloud_provider || 'Cloud'}</span>
                  </div>
                  <div className="text-xs text-gray-600 mt-1">Resources: {infra.total_resources ?? '—'}</div>
                </button>
              ))}
              {(infrastructures.data || []).length === 0 && (
                <div className="text-sm text-gray-600">No infrastructures found</div>
              )}
            </div>
          )}
        </div>

        {/* Live Resources for selected infra */}
        {selectedInfraId && (
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Resources</h3>
              <span className="text-sm text-gray-600">Infra: {selectedInfraId}</span>
            </div>
            {liveResources.isLoading ? (
              <div className="min-h-[100px] flex items-center justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400" />
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {(liveResources.data || []).map((r: any) => (
                  <button key={r.id} className="text-left border border-gray-200 rounded-lg p-4 hover:shadow" onClick={()=>setSelectedResource(r)}>
                    <div className="flex items-center justify-between mb-2">
                      <div className="font-medium text-gray-900">{r.name || r.id}</div>
                      <span className="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-700">{r.status || 'unknown'}</span>
                    </div>
                    <div className="flex items-center justify-between text-xs text-gray-600">
                      <span>{r.region || '—'}</span>
                      <span>{r.monthly_cost ? `$${Number(r.monthly_cost).toFixed(2)}/mo` : '—'}</span>
                    </div>
                  </button>
                ))}
                {(!liveResources.data || liveResources.data.length === 0) && (
                  <div className="text-sm text-gray-600">No resources found</div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Resource Details Overlay */}
        {selectedResource && (
          <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl w-full max-w-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">{selectedResource.name || selectedResource.id}</h3>
                <button className="text-gray-500 hover:text-gray-700" onClick={()=>setSelectedResource(null)}>✕</button>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div><span className="text-gray-500">Region:</span> <span className="ml-1 text-gray-900">{selectedResource.region || '—'}</span></div>
                <div><span className="text-gray-500">Status:</span> <span className="ml-1 text-gray-900">{selectedResource.status || 'unknown'}</span></div>
                <div><span className="text-gray-500">Type:</span> <span className="ml-1 text-gray-900">{selectedResource.resource_type || '—'}</span></div>
                <div><span className="text-gray-500">Instance:</span> <span className="ml-1 text-gray-900">{selectedResource.instance_type || '—'}</span></div>
                <div><span className="text-gray-500">Monthly Cost:</span> <span className="ml-1 text-gray-900">{selectedResource.monthly_cost ? `$${Number(selectedResource.monthly_cost).toFixed(2)}` : '—'}</span></div>
              </div>
              <div className="mt-4 flex items-center justify-end gap-2">
                <button className="btn-secondary text-xs px-3 py-1" onClick={()=>setSelectedResource(null)}>Close</button>
                <button className="btn-primary text-xs px-3 py-1" onClick={()=>alert('Action placeholder')}>Action</button>
              </div>
            </div>
          </div>
        )}

        {/* Enhanced Resources List/Grid */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Infrastructure Resources</h3>
              <p className="text-sm text-gray-600">AI-powered resource monitoring and optimization</p>
            </div>
            <div className="flex items-center space-x-2">
              <button 
                onClick={() => setViewMode('list')}
                className={`px-3 py-1 rounded-md text-sm font-medium ${
                  viewMode === 'list' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                List
              </button>
              <button 
                onClick={() => setViewMode('grid')}
                className={`px-3 py-1 rounded-md text-sm font-medium ${
                  viewMode === 'grid' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                Grid
              </button>
              <button 
                onClick={() => setViewMode('3d')}
                className={`px-3 py-1 rounded-md text-sm font-medium ${
                  viewMode === '3d' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                3D View
              </button>
              <button className="btn-secondary flex items-center space-x-2">
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>
            </div>
          </div>
          
          {viewMode === 'list' && (
            <div className="space-y-4">
              {advancedResources.map((resource) => (
                <div key={resource.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      {getResourceIcon(resource.type)}
                      <div>
                        <h4 className="font-medium text-gray-900">{resource.name}</h4>
                        <p className="text-sm text-gray-500">{resource.type} • {resource.instanceType}</p>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className="text-xs text-gray-500">{resource.region}</span>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(resource.status)}`}>
                            {resource.status}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-6">
                      <div className="text-center">
                        <p className="text-sm text-gray-500">CPU</p>
                        <p className={`text-sm font-medium ${getUtilizationColor(resource.cpu)}`}>
                          {resource.cpu}%
                        </p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-gray-500">Memory</p>
                        <p className={`text-sm font-medium ${getUtilizationColor(resource.memory)}`}>
                          {resource.memory}%
                        </p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-gray-500">Storage</p>
                        <p className={`text-sm font-medium ${getUtilizationColor(resource.storage)}`}>
                          {resource.storage}%
                        </p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-gray-500">Network</p>
                        <p className={`text-sm font-medium ${getUtilizationColor(resource.network)}`}>
                          {resource.network}%
                        </p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-gray-500">Cost</p>
                        <p className="text-sm font-medium text-gray-900">${resource.cost}/mo</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button className="btn-secondary text-sm px-3 py-1">
                          <Eye className="w-4 h-4 mr-1" />
                          Details
                        </button>
                        <button className="btn-primary text-sm px-3 py-1">
                          <Settings className="w-4 h-4 mr-1" />
                          Manage
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  {/* AI Insights and Performance Metrics */}
                  <div className="mt-4 grid grid-cols-1 lg:grid-cols-2 gap-4">
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <div className="flex items-center space-x-2 mb-2">
                        <Brain className="w-4 h-4 text-blue-600" />
                        <span className="text-sm font-medium text-blue-900">AI Insights</span>
                      </div>
                      <ul className="space-y-1">
                        {resource.aiInsights.slice(0, 2).map((insight, index) => (
                          <li key={index} className="text-xs text-blue-700 flex items-start space-x-2">
                            <span className="text-blue-500 mt-1">•</span>
                            <span>{insight}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className="bg-green-50 p-3 rounded-lg">
                      <div className="flex items-center space-x-2 mb-2">
                        <Activity className="w-4 h-4 text-green-600" />
                        <span className="text-sm font-medium text-green-900">Performance</span>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-500">Response:</span>
                          <span className="ml-1 font-medium text-green-600">{resource.performanceMetrics.responseTime}ms</span>
                        </div>
                        <div>
                          <span className="text-gray-500">Throughput:</span>
                          <span className="ml-1 font-medium text-green-600">{resource.performanceMetrics.throughput}/s</span>
                        </div>
                        <div>
                          <span className="text-gray-500">Error Rate:</span>
                          <span className="ml-1 font-medium text-green-600">{resource.performanceMetrics.errorRate}%</span>
                        </div>
                        <div>
                          <span className="text-gray-500">Availability:</span>
                          <span className="ml-1 font-medium text-green-600">{resource.performanceMetrics.availability}%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-3 flex items-center space-x-2">
                    {resource.tags.map((tag, index) => (
                      <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {viewMode === 'grid' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {advancedResources.map((resource) => (
                <div key={resource.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      {getResourceIcon(resource.type)}
                      <span className="text-sm font-medium text-gray-900">{resource.name}</span>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(resource.status)}`}>
                      {resource.status}
                    </span>
                  </div>
                  
                  <div className="space-y-2 mb-3">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Type:</span>
                      <span className="text-gray-900">{resource.type}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Region:</span>
                      <span className="text-gray-900">{resource.region}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Instance:</span>
                      <span className="text-gray-900">{resource.instanceType}</span>
                    </div>
                  </div>
                  
                  <div className="space-y-2 mb-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-gray-500">CPU</span>
                      <span className={`text-xs font-medium ${getUtilizationColor(resource.cpu)}`}>
                        {resource.cpu}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-1">
                      <div 
                        className={`h-1 rounded-full ${
                          resource.cpu >= 80 ? 'bg-red-500' : 
                          resource.cpu >= 60 ? 'bg-yellow-500' : 'bg-green-500'
                        }`}
                        style={{ width: `${resource.cpu}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-900">${resource.cost}/mo</span>
                    <button className="btn-primary text-xs px-2 py-1">
                      <Settings className="w-3 h-3 mr-1" />
                      Manage
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {viewMode === '3d' && (
            <div className="h-96 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <Cube className="w-16 h-16 text-blue-500 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">3D Infrastructure Visualization</h3>
                <p className="text-gray-600 mb-4">Interactive 3D visualization of your infrastructure topology</p>
                <div className="flex items-center justify-center space-x-4 mb-4">
                  <div className="text-center">
                    <div className="w-8 h-8 bg-blue-500 rounded-full mx-auto mb-2"></div>
                    <span className="text-xs text-gray-600">Web Tier</span>
                  </div>
                  <div className="text-center">
                    <div className="w-8 h-8 bg-green-500 rounded-full mx-auto mb-2"></div>
                    <span className="text-xs text-gray-600">Database</span>
                  </div>
                  <div className="text-center">
                    <div className="w-8 h-8 bg-purple-500 rounded-full mx-auto mb-2"></div>
                    <span className="text-xs text-gray-600">Cache</span>
                  </div>
                  <div className="text-center">
                    <div className="w-8 h-8 bg-yellow-500 rounded-full mx-auto mb-2"></div>
                    <span className="text-xs text-gray-600">Storage</span>
                  </div>
                </div>
                <button className="btn-primary">
                  <Cube className="w-4 h-4 mr-2" />
                  Launch 3D View
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Enhanced Service Breakdown */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Service Performance Analysis</h3>
            <div className="space-y-4">
              {advancedServices.map((service) => (
                <div key={service.name} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-center space-x-3">
                    {getResourceIcon(service.name)}
                    <div>
                      <p className="font-medium text-gray-900">{service.name}</p>
                      <p className="text-sm text-gray-500">{service.count} resources</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-gray-900">${service.cost}/mo</p>
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(service.status)}`}>
                        {service.status}
                      </span>
                      <span className={`text-xs font-medium ${getPerformanceColor(service.performance)}`}>
                        {service.performance}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Regional Performance</h3>
            <div className="space-y-4">
              {advancedRegions.map((region) => (
                <div key={region.name} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{region.name}</p>
                    <p className="text-sm text-gray-500">{region.resources} resources</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-gray-900">${region.cost}/mo</p>
                    <div className="grid grid-cols-3 gap-2 text-xs mt-1">
                      <div>
                        <span className="text-gray-500">Perf:</span>
                        <span className="ml-1 font-medium text-green-600">{region.performance}%</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Avail:</span>
                        <span className="ml-1 font-medium text-green-600">{region.availability}%</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Latency:</span>
                        <span className="ml-1 font-medium text-blue-600">{region.latency}ms</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
} 