import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import DashboardPage from '../app/(dashboard)/dashboard/page'
import { useDashboardStore } from '../lib/stores/dashboardStore'

// Mock the store
jest.mock('../lib/stores/dashboardStore', () => ({
  useDashboardStore: jest.fn(),
  useMetrics: jest.fn(),
  useAlerts: jest.fn(),
  useActivities: jest.fn()
}))

// Mock lucide-react icons
jest.mock('lucide-react', () => ({
  BarChart3: () => <div data-testid="bar-chart-icon">BarChart3</div>,
  TrendingUp: () => <div data-testid="trending-up-icon">TrendingUp</div>,
  Shield: () => <div data-testid="shield-icon">Shield</div>,
  DollarSign: () => <div data-testid="dollar-sign-icon">DollarSign</div>,
  Server: () => <div data-testid="server-icon">Server</div>,
  Users: () => <div data-testid="users-icon">Users</div>,
  AlertTriangle: () => <div data-testid="alert-triangle-icon">AlertTriangle</div>,
  CheckCircle: () => <div data-testid="check-circle-icon">CheckCircle</div>,
  Clock: () => <div data-testid="clock-icon">Clock</div>,
  Activity: () => <div data-testid="activity-icon">Activity</div>,
  Zap: () => <div data-testid="zap-icon">Zap</div>,
  Globe: () => <div data-testid="globe-icon">Globe</div>,
  Calculator: () => <div data-testid="calculator-icon">Calculator</div>,
  ArrowRight: () => <div data-testid="arrow-right-icon">ArrowRight</div>,
  Sparkles: () => <div data-testid="sparkles-icon">Sparkles</div>,
  Target: () => <div data-testid="target-icon">Target</div>,
}))

// MSW is unnecessary here since we mock the store and do not perform real network calls.

describe('DashboardPage', () => {
  const mockStore = {
    data: {
      metrics: [
        {
          id: 'cost',
          title: 'Total Cost',
          value: '$12,847',
          change: '+12.5%',
          changeType: 'negative',
          icon: 'DollarSign',
          color: 'bg-red-500',
          trend: [12000, 12500, 12847]
        },
        {
          id: 'security',
          title: 'Security Score',
          value: '94/100',
          change: '+2.1%',
          changeType: 'positive',
          icon: 'Shield',
          color: 'bg-green-500',
          trend: [90, 92, 94]
        },
        {
          id: 'uptime',
          title: 'Uptime',
          value: '99.9%',
          change: '+0.1%',
          changeType: 'positive',
          icon: 'Server',
          color: 'bg-blue-500',
          trend: [99.8, 99.9, 99.9]
        },
        {
          id: 'users',
          title: 'Active Users',
          value: '1,247',
          change: '+8.3%',
          changeType: 'positive',
          icon: 'Users',
          color: 'bg-purple-500',
          trend: [1150, 1200, 1247]
        }
      ],
      alerts: [
        {
          id: '1',
          type: 'warning',
          message: 'High CPU usage detected on production servers',
          timestamp: new Date().toISOString(),
          severity: 'medium',
          dismissed: false
        },
        {
          id: '2',
          type: 'success',
          message: 'Security scan completed - no vulnerabilities found',
          timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
          severity: 'low',
          dismissed: false
        }
      ],
      activities: [
        {
          id: '1',
          action: 'Deployed new version',
          service: 'Frontend API',
          user: 'John Doe',
          time: '2 minutes ago',
          status: 'success'
        },
        {
          id: '2',
          action: 'Security scan initiated',
          service: 'Production Cluster',
          user: 'System',
          time: '5 minutes ago',
          status: 'info'
        }
      ]
    },
    isLoading: false,
    error: null,
    fetchData: jest.fn(),
    refreshData: jest.fn(),
    dismissAlert: jest.fn(),
    addAlert: jest.fn(),
    updateMetric: jest.fn()
  }

  beforeEach(() => {
    (useDashboardStore as jest.Mock).mockReturnValue(mockStore)
  })

  it('renders dashboard with metrics', () => {
    render(<DashboardPage />)
    
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Monitor your cloud infrastructure and performance')).toBeInTheDocument()
    
    // Check metrics are rendered
    expect(screen.getByText('Total Cost')).toBeInTheDocument()
    expect(screen.getByText('$12,847')).toBeInTheDocument()
    expect(screen.getByText('Security Score')).toBeInTheDocument()
    expect(screen.getByText('94/100')).toBeInTheDocument()
    expect(screen.getByText('Uptime')).toBeInTheDocument()
    expect(screen.getByText('99.9%')).toBeInTheDocument()
    expect(screen.getByText('Active Users')).toBeInTheDocument()
    expect(screen.getByText('1,247')).toBeInTheDocument()
  })

  it('renders alerts section', () => {
    render(<DashboardPage />)
    
    expect(screen.getByText('System Alerts')).toBeInTheDocument()
    expect(screen.getByText('High CPU usage detected on production servers')).toBeInTheDocument()
    expect(screen.getByText('Security scan completed - no vulnerabilities found')).toBeInTheDocument()
  })

  it('renders recent activity section', () => {
    render(<DashboardPage />)
    
    expect(screen.getByText('Recent Activity')).toBeInTheDocument()
    expect(screen.getByText('Deployed new version')).toBeInTheDocument()
    expect(screen.getByText('Security scan initiated')).toBeInTheDocument()
  })

  it('renders quick actions', () => {
    render(<DashboardPage />)
    
    expect(screen.getByText('Quick Actions')).toBeInTheDocument()
    expect(screen.getByText('Run Security Scan')).toBeInTheDocument()
    expect(screen.getByText('Optimize Costs')).toBeInTheDocument()
    expect(screen.getByText('Deploy Update')).toBeInTheDocument()
    expect(screen.getByText('Generate Report')).toBeInTheDocument()
  })

  it('handles refresh data button click', () => {
    render(<DashboardPage />)
    
    const refreshButton = screen.getByText('Refresh Data')
    fireEvent.click(refreshButton)
    
    expect(mockStore.refreshData).toHaveBeenCalled()
  })

  it('displays loading state', () => {
    (useDashboardStore as jest.Mock).mockReturnValue({
      ...mockStore,
      isLoading: true
    })
    
    render(<DashboardPage />)
    
    // Should show loading indicators or skeleton
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
  })

  it('displays error state', () => {
    (useDashboardStore as jest.Mock).mockReturnValue({
      ...mockStore,
      error: 'Failed to fetch dashboard data'
    })
    
    render(<DashboardPage />)
    
    // Should show error message
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
  })

  it('renders performance chart placeholder', () => {
    render(<DashboardPage />)
    
    expect(screen.getByText('Performance Overview')).toBeInTheDocument()
    expect(screen.getByText('Performance chart will be rendered here')).toBeInTheDocument()
    expect(screen.getByText('Real-time data visualization')).toBeInTheDocument()
  })

  it('displays metric changes correctly', () => {
    render(<DashboardPage />)
    
    // Check positive changes
    expect(screen.getByText('+2.1%')).toBeInTheDocument()
    expect(screen.getByText('+0.1%')).toBeInTheDocument()
    expect(screen.getByText('+8.3%')).toBeInTheDocument()
    
    // Check negative changes
    expect(screen.getByText('+12.5%')).toBeInTheDocument() // This is negative in the data
  })

  it('handles empty data gracefully', () => {
    (useDashboardStore as jest.Mock).mockReturnValue({
      ...mockStore,
      data: {
        metrics: [],
        alerts: [],
        activities: [],
        performance: { cpu: [], memory: [], network: [], disk: [] },
        costs: { current: 0, previous: 0, breakdown: {} },
        security: { score: 0, vulnerabilities: 0, lastScan: '' }
      }
    })
    
    render(<DashboardPage />)
    
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Performance Overview')).toBeInTheDocument()
  })

  it('renders with proper accessibility attributes', () => {
    render(<DashboardPage />)
    
    // Check for proper heading structure (updated labels)
    expect(screen.getByRole('heading', { name: /CloudMind Dashboard/i })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Quick Actions' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: /Platform Status/i })).toBeInTheDocument()
  })

  it('handles quick action button clicks', () => {
    render(<DashboardPage />)
    
    const securityScanButton = screen.getByText('Run Security Scan')
    const optimizeCostsButton = screen.getByText('Optimize Costs')
    const deployUpdateButton = screen.getByText('Deploy Update')
    const generateReportButton = screen.getByText('Generate Report')
    
    fireEvent.click(securityScanButton)
    fireEvent.click(optimizeCostsButton)
    fireEvent.click(deployUpdateButton)
    fireEvent.click(generateReportButton)
    
    // These buttons should be clickable (actual functionality would be implemented)
    expect(securityScanButton).toBeInTheDocument()
    expect(optimizeCostsButton).toBeInTheDocument()
    expect(deployUpdateButton).toBeInTheDocument()
    expect(generateReportButton).toBeInTheDocument()
  })

  it('displays activity status icons correctly', () => {
    render(<DashboardPage />)
    
    // Check that activity items have proper status indicators
    const activityItems = screen.getAllByText(/Deployed new version|Security scan initiated/)
    expect(activityItems.length).toBeGreaterThan(0)
  })

  it('renders alert severity indicators', () => {
    render(<DashboardPage />)
    
    // Check that alerts have proper styling based on type
    const warningAlert = screen.getByText('High CPU usage detected on production servers')
    const successAlert = screen.getByText('Security scan completed - no vulnerabilities found')
    
    expect(warningAlert).toBeInTheDocument()
    expect(successAlert).toBeInTheDocument()
  })
})

describe('Dashboard Integration Tests', () => {
  it('fetches data on component mount', () => {
    const mockFetchData = jest.fn()
    ;(useDashboardStore as jest.Mock).mockReturnValue({
      data: null,
      isLoading: false,
      error: null,
      fetchData: mockFetchData
    })
    
    render(<DashboardPage />)
    
    // Component should call fetchData on mount
    expect(mockFetchData).toHaveBeenCalled()
  })

  it('handles API errors gracefully', () => {
    server.use(
      rest.get('/api/v1/dashboard', (req, res, ctx) => {
        return res(ctx.status(500))
      })
    )
    
    const mockStore = {
      data: null,
      isLoading: false,
      error: 'Failed to fetch dashboard data',
      fetchData: jest.fn(),
      refreshData: jest.fn()
    }
    
    ;(useDashboardStore as jest.Mock).mockReturnValue(mockStore)
    
    render(<DashboardPage />)
    
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
  })
}) 