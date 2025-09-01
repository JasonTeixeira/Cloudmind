'use client'

import { useState } from 'react'
import { Shield, AlertTriangle, CheckCircle, Clock, Activity, Zap, Settings, BarChart3 } from 'lucide-react'

export default function AutoHealingPage() {
  const [activeTab, setActiveTab] = useState('overview')

  const healthChecks = [
    {
      id: 1,
      service: 'API Gateway',
      status: 'healthy',
      lastCheck: '2 minutes ago',
      responseTime: '45ms',
      uptime: '99.9%'
    },
    {
      id: 2,
      service: 'Database',
      status: 'healthy',
      lastCheck: '1 minute ago',
      responseTime: '120ms',
      uptime: '99.8%'
    },
    {
      id: 3,
      service: 'Redis Cache',
      status: 'warning',
      lastCheck: '30 seconds ago',
      responseTime: '200ms',
      uptime: '99.5%'
    },
    {
      id: 4,
      service: 'File Storage',
      status: 'healthy',
      lastCheck: '45 seconds ago',
      responseTime: '85ms',
      uptime: '99.9%'
    }
  ]

  const recoveryActions = [
    {
      id: 1,
      service: 'Redis Cache',
      action: 'Restart Service',
      status: 'completed',
      timestamp: '2 minutes ago',
      duration: '30 seconds'
    },
    {
      id: 2,
      service: 'API Gateway',
      action: 'Scale Up',
      status: 'in-progress',
      timestamp: '5 minutes ago',
      duration: '2 minutes'
    },
    {
      id: 3,
      service: 'Database',
      action: 'Optimize Queries',
      status: 'scheduled',
      timestamp: '10 minutes ago',
      duration: '5 minutes'
    }
  ]

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

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-4 w-4" />
      case 'warning':
        return <AlertTriangle className="h-4 w-4" />
      case 'critical':
        return <AlertTriangle className="h-4 w-4" />
      default:
        return <Clock className="h-4 w-4" />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Shield className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Auto-Healing</h1>
              <p className="text-gray-600 mt-1">Intelligent system recovery and health monitoring</p>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <CheckCircle className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Healthy Services</p>
                <p className="text-2xl font-bold text-gray-900">12</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <AlertTriangle className="h-6 w-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Warnings</p>
                <p className="text-2xl font-bold text-gray-900">1</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Zap className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Recovery Actions</p>
                <p className="text-2xl font-bold text-gray-900">3</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Activity className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Uptime</p>
                <p className="text-2xl font-bold text-gray-900">99.9%</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Health Checks */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Service Health Checks</h2>
                <p className="text-sm text-gray-600">Real-time monitoring of all system services</p>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {healthChecks.map((check) => (
                    <div key={check.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className={`p-2 rounded-lg ${getStatusColor(check.status)}`}>
                          {getStatusIcon(check.status)}
                        </div>
                        <div>
                          <h3 className="font-medium text-gray-900">{check.service}</h3>
                          <p className="text-sm text-gray-600">Last check: {check.lastCheck}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-900">{check.responseTime}</p>
                        <p className="text-sm text-gray-600">Uptime: {check.uptime}</p>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-6">
                  <button className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                    Run Health Check
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Recovery Actions */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Recovery Actions</h2>
                <p className="text-sm text-gray-600">Recent auto-healing activities</p>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {recoveryActions.map((action) => (
                    <div key={action.id} className="p-4 border border-gray-200 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-medium text-gray-900">{action.service}</h3>
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          action.status === 'completed' ? 'bg-green-100 text-green-800' :
                          action.status === 'in-progress' ? 'bg-blue-100 text-blue-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
                          {action.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{action.action}</p>
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>{action.timestamp}</span>
                        <span>{action.duration}</span>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-6">
                  <button className="w-full bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700">
                    View All Actions
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Configuration */}
        <div className="mt-8">
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Auto-Healing Configuration</h2>
              <p className="text-sm text-gray-600">Configure intelligent recovery settings</p>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Health Check Interval</label>
                  <select className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    <option>30 seconds</option>
                    <option>1 minute</option>
                    <option>5 minutes</option>
                    <option>10 minutes</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Recovery Strategy</label>
                  <select className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    <option>Automatic</option>
                    <option>Manual Approval</option>
                    <option>Rollback on Failure</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Alert Threshold</label>
                  <select className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    <option>Immediate</option>
                    <option>After 3 failures</option>
                    <option>After 5 failures</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Circuit Breaker</label>
                  <select className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    <option>Enabled</option>
                    <option>Disabled</option>
                  </select>
                </div>
              </div>
              <div className="mt-6 flex justify-end space-x-3">
                <button className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700">
                  Reset to Defaults
                </button>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                  Save Configuration
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 