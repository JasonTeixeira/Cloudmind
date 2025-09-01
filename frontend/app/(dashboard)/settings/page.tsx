'use client'

import { useState } from 'react'
import { Settings, User, Shield, Bell, Database, Key, Globe, Palette } from 'lucide-react'

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('profile')

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'security', label: 'Security', icon: Shield },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'api-keys', label: 'API Keys', icon: Key },
    { id: 'integrations', label: 'Integrations', icon: Database },
    { id: 'appearance', label: 'Appearance', icon: Palette },
    { id: 'preferences', label: 'Preferences', icon: Settings }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600 mt-2">Manage your account settings and preferences</p>
        </div>

        <div className="bg-white rounded-lg shadow">
          {/* Tab Navigation */}
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                      activeTab === tab.id
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'profile' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">Profile Information</h2>
                <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Full Name</label>
                    <input
                      type="text"
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Enter your full name"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Email</label>
                    <input
                      type="email"
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Enter your email"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Company</label>
                    <input
                      type="text"
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Enter your company"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Role</label>
                    <select className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                      <option>Select your role</option>
                      <option>Developer</option>
                      <option>DevOps Engineer</option>
                      <option>System Administrator</option>
                      <option>Cloud Architect</option>
                      <option>Manager</option>
                    </select>
                  </div>
                </div>
                <div className="flex justify-end">
                  <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                    Save Changes
                  </button>
                </div>
              </div>
            )}

            {activeTab === 'security' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">Security Settings</h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Two-Factor Authentication</h3>
                      <p className="text-sm text-gray-600">Add an extra layer of security to your account</p>
                    </div>
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                      Enable 2FA
                    </button>
                  </div>
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Change Password</h3>
                      <p className="text-sm text-gray-600">Update your account password</p>
                    </div>
                    <button className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700">
                      Change Password
                    </button>
                  </div>
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Session Management</h3>
                      <p className="text-sm text-gray-600">View and manage active sessions</p>
                    </div>
                    <button className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700">
                      Manage Sessions
                    </button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'notifications' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">Notification Preferences</h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Email Notifications</h3>
                      <p className="text-sm text-gray-600">Receive notifications via email</p>
                    </div>
                    <input type="checkbox" className="h-4 w-4 text-blue-600" defaultChecked />
                  </div>
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Security Alerts</h3>
                      <p className="text-sm text-gray-600">Get notified about security events</p>
                    </div>
                    <input type="checkbox" className="h-4 w-4 text-blue-600" defaultChecked />
                  </div>
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Cost Alerts</h3>
                      <p className="text-sm text-gray-600">Receive cost optimization alerts</p>
                    </div>
                    <input type="checkbox" className="h-4 w-4 text-blue-600" />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'api-keys' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">API Keys</h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">CloudMind API Key</h3>
                      <p className="text-sm text-gray-600">Main API key for CloudMind services</p>
                    </div>
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                      Generate New Key
                    </button>
                  </div>
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">External Integrations</h3>
                      <p className="text-sm text-gray-600">Manage API keys for external services</p>
                    </div>
                    <button className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700">
                      Manage Keys
                    </button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'integrations' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">Integrations</h2>
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  <div className="p-4 border border-gray-200 rounded-lg">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                        <Database className="h-4 w-4 text-blue-600" />
                      </div>
                      <h3 className="font-medium text-gray-900">AWS</h3>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">Connect your AWS account for cost analysis</p>
                    <button className="w-full bg-blue-600 text-white px-3 py-2 rounded-md text-sm hover:bg-blue-700">
                      Connect
                    </button>
                  </div>
                  <div className="p-4 border border-gray-200 rounded-lg">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                        <Database className="h-4 w-4 text-blue-600" />
                      </div>
                      <h3 className="font-medium text-gray-900">Azure</h3>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">Connect your Azure account for monitoring</p>
                    <button className="w-full bg-blue-600 text-white px-3 py-2 rounded-md text-sm hover:bg-blue-700">
                      Connect
                    </button>
                  </div>
                  <div className="p-4 border border-gray-200 rounded-lg">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                        <Database className="h-4 w-4 text-blue-600" />
                      </div>
                      <h3 className="font-medium text-gray-900">Google Cloud</h3>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">Connect your GCP account for infrastructure</p>
                    <button className="w-full bg-blue-600 text-white px-3 py-2 rounded-md text-sm hover:bg-blue-700">
                      Connect
                    </button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'appearance' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">Appearance</h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Theme</label>
                    <select className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                      <option>Light</option>
                      <option>Dark</option>
                      <option>System</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Color Scheme</label>
                    <div className="flex space-x-3">
                      <button className="w-8 h-8 bg-blue-600 rounded-full border-2 border-blue-600"></button>
                      <button className="w-8 h-8 bg-purple-600 rounded-full border-2 border-gray-300"></button>
                      <button className="w-8 h-8 bg-green-600 rounded-full border-2 border-gray-300"></button>
                      <button className="w-8 h-8 bg-red-600 rounded-full border-2 border-gray-300"></button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'preferences' && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900">Preferences</h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Auto-save</h3>
                      <p className="text-sm text-gray-600">Automatically save your work</p>
                    </div>
                    <input type="checkbox" className="h-4 w-4 text-blue-600" defaultChecked />
                  </div>
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Analytics</h3>
                      <p className="text-sm text-gray-600">Help improve CloudMind with usage analytics</p>
                    </div>
                    <input type="checkbox" className="h-4 w-4 text-blue-600" defaultChecked />
                  </div>
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Beta Features</h3>
                      <p className="text-sm text-gray-600">Access to experimental features</p>
                    </div>
                    <input type="checkbox" className="h-4 w-4 text-blue-600" />
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
} 