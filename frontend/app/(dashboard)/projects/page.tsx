'use client'

import { useState, useEffect } from 'react'
import DashboardLayout from '@/components/layouts/DashboardLayout'
import { 
  Folder, 
  Plus, 
  Search, 
  Filter,
  Settings,
  Users,
  Activity,
  BarChart3,
  DollarSign,
  Shield,
  Clock,
  Star,
  MoreVertical,
  Eye,
  Edit,
  Trash2,
  Download,
  Share2
} from 'lucide-react'

export default function ProjectsPage() {
  const [selectedStatus, setSelectedStatus] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [viewMode, setViewMode] = useState('grid')

  const projects = [
    {
      id: 1,
      name: "Production Environment",
      description: "Main production infrastructure for web application",
      status: "active",
      owner: "John Doe",
      team: ["Alice Smith", "Bob Johnson", "Carol Davis"],
      cost: 2450,
      resources: 28,
      securityScore: 92,
      lastUpdated: "2 hours ago",
      tags: ["production", "web", "critical"],
      cloudProvider: "AWS",
      regions: ["us-east-1", "us-west-2"]
    },
    {
      id: 2,
      name: "Development Environment",
      description: "Development and testing infrastructure",
      status: "active",
      owner: "Alice Smith",
      team: ["Bob Johnson", "David Wilson"],
      cost: 850,
      resources: 12,
      securityScore: 88,
      lastUpdated: "1 day ago",
      tags: ["development", "testing"],
      cloudProvider: "AWS",
      regions: ["us-east-1"]
    },
    {
      id: 3,
      name: "Staging Environment",
      description: "Staging environment for pre-production testing",
      status: "active",
      owner: "Bob Johnson",
      team: ["Alice Smith", "Carol Davis"],
      cost: 1200,
      resources: 18,
      securityScore: 90,
      lastUpdated: "3 hours ago",
      tags: ["staging", "testing"],
      cloudProvider: "AWS",
      regions: ["us-east-1"]
    },
    {
      id: 4,
      name: "Analytics Platform",
      description: "Data analytics and reporting infrastructure",
      status: "archived",
      owner: "Carol Davis",
      team: ["John Doe", "Alice Smith"],
      cost: 1800,
      resources: 22,
      securityScore: 85,
      lastUpdated: "1 week ago",
      tags: ["analytics", "data"],
      cloudProvider: "AWS",
      regions: ["us-east-1", "eu-west-1"]
    }
  ]

  const projectStats = [
    { name: "Total Projects", value: "4", change: "+1", changeType: "increase" },
    { name: "Active Projects", value: "3", change: "0", changeType: "neutral" },
    { name: "Total Cost", value: "$6,300", change: "+12%", changeType: "increase" },
    { name: "Avg Security Score", value: "89%", change: "+3%", changeType: "increase" }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100'
      case 'inactive': return 'text-gray-600 bg-gray-100'
      case 'archived': return 'text-yellow-600 bg-yellow-100'
      case 'suspended': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getSecurityScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600'
    if (score >= 80) return 'text-yellow-600'
    return 'text-red-600'
  }

  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         project.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = selectedStatus === 'all' || project.status === selectedStatus
    return matchesSearch && matchesStatus
  })

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
            <p className="text-gray-600">Manage your cloud projects and team collaboration.</p>
          </div>
          <div className="flex items-center space-x-3">
            <button className="btn-secondary flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Export</span>
            </button>
            <button className="btn-primary flex items-center space-x-2">
              <Plus className="w-4 h-4" />
              <span>New Project</span>
            </button>
          </div>
        </div>

        {/* Project Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {projectStats.map((stat) => (
            <div key={stat.name} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  <div className="flex items-center mt-1">
                    <span className={`text-sm ${
                      stat.changeType === 'increase' ? 'text-green-600' : 
                      stat.changeType === 'decrease' ? 'text-red-600' : 'text-gray-600'
                    }`}>
                      {stat.change}
                    </span>
                  </div>
                </div>
                <div className="p-3 bg-blue-100 rounded-lg">
                  <Folder className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Filters */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
            <div className="flex items-center space-x-2">
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
                onClick={() => setViewMode('list')}
                className={`px-3 py-1 rounded-md text-sm font-medium ${
                  viewMode === 'list' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                List
              </button>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="form-label">Status</label>
              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="input-field"
              >
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="archived">Archived</option>
                <option value="suspended">Suspended</option>
              </select>
            </div>
            <div>
              <label className="form-label">Cloud Provider</label>
              <select className="input-field">
                <option value="all">All Providers</option>
                <option value="aws">AWS</option>
                <option value="azure">Azure</option>
                <option value="gcp">Google Cloud</option>
              </select>
            </div>
            <div>
              <label className="form-label">Search</label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search projects..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="input-field pl-10"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Projects Grid/List */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Projects ({filteredProjects.length})</h3>
            <button className="btn-secondary flex items-center space-x-2">
              <Filter className="w-4 h-4" />
              <span>Advanced Filter</span>
            </button>
          </div>
          
          {viewMode === 'grid' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredProjects.map((project) => (
                <div key={project.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <Folder className="w-5 h-5 text-blue-500" />
                        <h4 className="text-lg font-medium text-gray-900">{project.name}</h4>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                          {project.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">{project.description}</p>
                      <div className="flex items-center space-x-2 text-xs text-gray-500 mb-3">
                        <span>{project.cloudProvider}</span>
                        <span>•</span>
                        <span>{project.regions.length} regions</span>
                      </div>
                    </div>
                    <button className="p-1 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100">
                      <MoreVertical className="w-4 h-4" />
                    </button>
                  </div>
                  
                  <div className="space-y-3 mb-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-500">Owner:</span>
                      <span className="text-gray-900">{project.owner}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-500">Team:</span>
                      <span className="text-gray-900">{project.team.length} members</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-500">Resources:</span>
                      <span className="text-gray-900">{project.resources}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-500">Cost:</span>
                      <span className="text-gray-900">${project.cost}/mo</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-500">Security:</span>
                      <span className={`font-medium ${getSecurityScoreColor(project.securityScore)}`}>
                        {project.securityScore}%
                      </span>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2 mb-3">
                    {project.tags.map((tag, index) => (
                      <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">Updated {project.lastUpdated}</span>
                    <div className="flex items-center space-x-2">
                      <button className="btn-secondary text-xs px-2 py-1">
                        <Eye className="w-3 h-3" />
                      </button>
                      <button className="btn-secondary text-xs px-2 py-1">
                        <Edit className="w-3 h-3" />
                      </button>
                      <button className="btn-secondary text-xs px-2 py-1">
                        <Share2 className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {viewMode === 'list' && (
            <div className="space-y-4">
              {filteredProjects.map((project) => (
                <div key={project.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <Folder className="w-8 h-8 text-blue-500" />
                      <div>
                        <div className="flex items-center space-x-3 mb-1">
                          <h4 className="text-lg font-medium text-gray-900">{project.name}</h4>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                            {project.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{project.description}</p>
                        <div className="flex items-center space-x-4 text-xs text-gray-500">
                          <span>Owner: {project.owner}</span>
                          <span>•</span>
                          <span>{project.team.length} team members</span>
                          <span>•</span>
                          <span>{project.cloudProvider}</span>
                          <span>•</span>
                          <span>{project.regions.length} regions</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-6">
                      <div className="text-center">
                        <p className="text-sm text-gray-500">Resources</p>
                        <p className="text-lg font-medium text-gray-900">{project.resources}</p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-gray-500">Cost</p>
                        <p className="text-lg font-medium text-gray-900">${project.cost}/mo</p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-gray-500">Security</p>
                        <p className={`text-lg font-medium ${getSecurityScoreColor(project.securityScore)}`}>
                          {project.securityScore}%
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button className="btn-secondary text-sm px-3 py-1">
                          View
                        </button>
                        <button className="btn-primary text-sm px-3 py-1">
                          Manage
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-3 flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      {project.tags.map((tag, index) => (
                        <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                    <span className="text-xs text-gray-500">Updated {project.lastUpdated}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button className="flex items-center space-x-3 p-4 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors duration-200">
              <Plus className="w-5 h-5 text-blue-600" />
              <span className="text-sm font-medium text-blue-900">Create Project</span>
            </button>
            <button className="flex items-center space-x-3 p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors duration-200">
              <Users className="w-5 h-5 text-green-600" />
              <span className="text-sm font-medium text-green-900">Invite Team</span>
            </button>
            <button className="flex items-center space-x-3 p-4 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors duration-200">
              <BarChart3 className="w-5 h-5 text-purple-600" />
              <span className="text-sm font-medium text-purple-900">View Analytics</span>
            </button>
            <button className="flex items-center space-x-3 p-4 bg-yellow-50 hover:bg-yellow-100 rounded-lg transition-colors duration-200">
              <Settings className="w-5 h-5 text-yellow-600" />
              <span className="text-sm font-medium text-yellow-900">Project Settings</span>
            </button>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
} 