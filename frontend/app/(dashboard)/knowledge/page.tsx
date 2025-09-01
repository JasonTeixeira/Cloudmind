'use client'

import { useState } from 'react'
import { BookOpen, Search, Database, Globe, Shield, Cloud, Network, Code, TrendingUp, Filter } from 'lucide-react'

export default function KnowledgePage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [activeTab, setActiveTab] = useState('search')

  const categories = [
    { id: 'all', name: 'All Knowledge', icon: BookOpen, count: 1250 },
    { id: 'security', name: 'Security', icon: Shield, count: 320 },
    { id: 'cloud', name: 'Cloud Services', icon: Cloud, count: 280 },
    { id: 'networking', name: 'Networking', icon: Network, count: 190 },
    { id: 'architecture', name: 'Architecture', icon: Code, count: 210 },
    { id: 'trends', name: 'Technology Trends', icon: TrendingUp, count: 150 },
    { id: 'compliance', name: 'Compliance', icon: Database, count: 100 }
  ]

  const knowledgeSources = [
    {
      id: 1,
      name: 'NVD Database',
      description: 'National Vulnerability Database',
      category: 'Security',
      lastUpdated: '2 hours ago',
      status: 'active',
      records: '185,420'
    },
    {
      id: 2,
      name: 'AWS Architecture Center',
      description: 'AWS best practices and patterns',
      category: 'Cloud',
      lastUpdated: '1 hour ago',
      status: 'active',
      records: '2,450'
    },
    {
      id: 3,
      name: 'MITRE ATT&CK',
      description: 'Adversarial tactics and techniques',
      category: 'Security',
      lastUpdated: '30 minutes ago',
      status: 'active',
      records: '12,800'
    },
    {
      id: 4,
      name: 'NIST Cybersecurity',
      description: 'NIST cybersecurity framework',
      category: 'Compliance',
      lastUpdated: '1 day ago',
      status: 'active',
      records: '5,200'
    },
    {
      id: 5,
      name: 'GitHub Security Advisories',
      description: 'Open source security advisories',
      category: 'Security',
      lastUpdated: '15 minutes ago',
      status: 'active',
      records: '8,900'
    },
    {
      id: 6,
      name: 'Stack Overflow',
      description: 'Developer community knowledge',
      category: 'Architecture',
      lastUpdated: '5 minutes ago',
      status: 'active',
      records: '45,200'
    }
  ]

  const recentSearches = [
    'AWS Lambda best practices',
    'Kubernetes security vulnerabilities',
    'Docker container optimization',
    'Microservices architecture patterns',
    'CI/CD pipeline security'
  ]

  const trendingTopics = [
    'Zero Trust Architecture',
    'Serverless Security',
    'Container Orchestration',
    'Cloud Cost Optimization',
    'DevSecOps Practices'
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <BookOpen className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Knowledge Base</h1>
              <p className="text-gray-600 mt-1">Access encyclopedic knowledge from 67+ authoritative sources</p>
            </div>
          </div>
        </div>

        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Search across 67+ knowledge sources..."
            />
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
              <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                Search
              </button>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Database className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Knowledge Sources</p>
                <p className="text-2xl font-bold text-gray-900">67+</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <BookOpen className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Records</p>
                <p className="text-2xl font-bold text-gray-900">258K+</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Globe className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Real-time Updates</p>
                <p className="text-2xl font-bold text-gray-900">Live</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <TrendingUp className="h-6 w-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Search Accuracy</p>
                <p className="text-2xl font-bold text-gray-900">99.9%</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Categories */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Categories</h2>
                <p className="text-sm text-gray-600">Browse by knowledge domain</p>
              </div>
              <div className="p-6">
                <div className="space-y-2">
                  {categories.map((category) => {
                    const Icon = category.icon
                    return (
                      <button
                        key={category.id}
                        onClick={() => setSelectedCategory(category.id)}
                        className={`w-full flex items-center justify-between p-3 rounded-lg text-left transition-all duration-200 ${
                          selectedCategory === category.id
                            ? 'bg-blue-50 border border-blue-200'
                            : 'hover:bg-gray-50'
                        }`}
                      >
                        <div className="flex items-center space-x-3">
                          <Icon className="h-5 w-5 text-gray-500" />
                          <span className="font-medium text-gray-900">{category.name}</span>
                        </div>
                        <span className="text-sm text-gray-500">{category.count}</span>
                      </button>
                    )
                  })}
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold text-gray-900">Knowledge Sources</h2>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setActiveTab('search')}
                      className={`px-3 py-1 rounded text-sm ${
                        activeTab === 'search'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      Search Results
                    </button>
                    <button
                      onClick={() => setActiveTab('sources')}
                      className={`px-3 py-1 rounded text-sm ${
                        activeTab === 'sources'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      All Sources
                    </button>
                  </div>
                </div>
              </div>
              <div className="p-6">
                {activeTab === 'search' && (
                  <div className="space-y-6">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Searches</h3>
                      <div className="flex flex-wrap gap-2">
                        {recentSearches.map((search, index) => (
                          <button
                            key={index}
                            className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200"
                          >
                            {search}
                          </button>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Trending Topics</h3>
                      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        {trendingTopics.map((topic, index) => (
                          <div key={index} className="p-4 border border-gray-200 rounded-lg">
                            <h4 className="font-medium text-gray-900">{topic}</h4>
                            <p className="text-sm text-gray-600 mt-1">High interest topic</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'sources' && (
                  <div className="space-y-4">
                    {knowledgeSources.map((source) => (
                      <div key={source.id} className="p-4 border border-gray-200 rounded-lg">
                        <div className="flex items-center justify-between mb-3">
                          <div>
                            <h3 className="font-medium text-gray-900">{source.name}</h3>
                            <p className="text-sm text-gray-600">{source.description}</p>
                          </div>
                          <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">
                            {source.status}
                          </span>
                        </div>
                        <div className="flex items-center justify-between text-sm text-gray-500">
                          <span>Category: {source.category}</span>
                          <span>Records: {source.records}</span>
                          <span>Updated: {source.lastUpdated}</span>
                        </div>
                        <div className="mt-3 flex space-x-2">
                          <button className="bg-blue-600 text-white px-3 py-1 rounded text-xs hover:bg-blue-700">
                            View Data
                          </button>
                          <button className="bg-gray-600 text-white px-3 py-1 rounded text-xs hover:bg-gray-700">
                            Configure
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Knowledge Configuration */}
        <div className="mt-8">
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Knowledge Base Configuration</h2>
              <p className="text-sm text-gray-600">Manage knowledge sources and update frequency</p>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Update Frequency</label>
                  <select className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    <option>Real-time</option>
                    <option>Every 5 minutes</option>
                    <option>Every hour</option>
                    <option>Daily</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Cache Duration</label>
                  <select className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    <option>5 minutes</option>
                    <option>15 minutes</option>
                    <option>1 hour</option>
                    <option>No cache</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Search Algorithm</label>
                  <select className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    <option>Semantic Search</option>
                    <option>Keyword Search</option>
                    <option>Hybrid Search</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Result Limit</label>
                  <select className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    <option>10 results</option>
                    <option>25 results</option>
                    <option>50 results</option>
                    <option>100 results</option>
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