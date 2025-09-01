'use client'

import { Users, Award, Globe, Shield, Zap, Target, CheckCircle } from 'lucide-react'

export default function AboutPage() {
  const features = [
    {
      icon: Shield,
      title: 'World-Class Security',
      description: 'Enterprise-grade security with AI-powered threat detection and compliance monitoring.'
    },
    {
      icon: Zap,
      title: 'AI-Powered Insights',
      description: 'Advanced AI algorithms provide intelligent recommendations for architecture and optimization.'
    },
    {
      icon: Globe,
      title: 'Global Knowledge Base',
      description: 'Access to 67+ authoritative sources for real-time, up-to-date information.'
    },
    {
      icon: Target,
      title: 'Cost Optimization',
      description: 'Intelligent cost analysis and optimization recommendations across all cloud providers.'
    },
    {
      icon: Users,
      title: 'Team Collaboration',
      description: 'Advanced project management and team collaboration features for seamless workflows.'
    },
    {
      icon: Award,
      title: 'Industry Excellence',
      description: 'Built by experts for experts, delivering world-class cloud engineering solutions.'
    }
  ]

  const stats = [
    { label: 'Knowledge Sources', value: '67+' },
    { label: 'API Integrations', value: '50+' },
    { label: 'Security Features', value: '100+' },
    { label: 'Uptime Guarantee', value: '99.9%' }
  ]

  const team = [
    {
      name: 'CloudMind Team',
      role: 'Core Development',
      description: 'Expert engineers and architects with decades of combined experience in cloud computing, security, and AI.'
    },
    {
      name: 'Security Experts',
      role: 'Security & Compliance',
      description: 'Certified security professionals specializing in enterprise security, compliance, and threat detection.'
    },
    {
      name: 'AI Specialists',
      role: 'AI & Machine Learning',
      description: 'AI researchers and engineers focused on developing intelligent systems for cloud optimization.'
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-md border-b border-gray-200/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
                <Globe className="h-6 w-6 text-white" />
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                CloudMind
              </span>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="/" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 font-medium">
                Home
              </a>
              <a href="#features" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 font-medium">
                Features
              </a>
              <a href="#team" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 font-medium">
                Team
              </a>
            </nav>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              About
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600">
                {' '}CloudMind
              </span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
              The world's most advanced cloud engineering platform, combining AI-powered insights with encyclopedic knowledge to deliver unparalleled cloud solutions.
            </p>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Mission</h2>
            <p className="text-xl text-gray-600 max-w-4xl mx-auto">
              To revolutionize cloud engineering by providing the most comprehensive, intelligent, and secure platform that empowers organizations to build, optimize, and secure their cloud infrastructure with confidence.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Why CloudMind?</h3>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-6 w-6 text-green-500 mt-1" />
                  <div>
                    <h4 className="font-semibold text-gray-900">Encyclopedic Knowledge</h4>
                    <p className="text-gray-600">Access to 67+ authoritative sources for real-time, accurate information.</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-6 w-6 text-green-500 mt-1" />
                  <div>
                    <h4 className="font-semibold text-gray-900">AI-Powered Intelligence</h4>
                    <p className="text-gray-600">Advanced AI algorithms provide intelligent recommendations and insights.</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-6 w-6 text-green-500 mt-1" />
                  <div>
                    <h4 className="font-semibold text-gray-900">World-Class Security</h4>
                    <p className="text-gray-600">Enterprise-grade security with comprehensive threat detection.</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-6 w-6 text-green-500 mt-1" />
                  <div>
                    <h4 className="font-semibold text-gray-900">Cost Optimization</h4>
                    <p className="text-gray-600">Intelligent cost analysis and optimization across all cloud providers.</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
              <h3 className="text-2xl font-bold mb-4">The Best Tool on Planet Earth</h3>
              <p className="text-blue-100 mb-6">
                CloudMind represents the pinnacle of cloud engineering technology, combining decades of expertise with cutting-edge AI to deliver solutions that were previously impossible.
              </p>
              <div className="grid grid-cols-2 gap-4">
                {stats.map((stat, index) => (
                  <div key={index} className="text-center">
                    <div className="text-2xl font-bold">{stat.value}</div>
                    <div className="text-sm text-blue-100">{stat.label}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">World-Class Features</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Every feature in CloudMind is designed to provide the highest level of functionality, security, and intelligence.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <div key={index} className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow duration-300">
                  <div className="p-3 bg-blue-100 rounded-lg w-fit mb-4">
                    <Icon className="h-6 w-6 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                  <p className="text-gray-600">{feature.description}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section id="team" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Expert Team</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our team of experts brings decades of combined experience in cloud computing, security, and AI.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {team.map((member, index) => (
              <div key={index} className="bg-gray-50 rounded-xl p-6 text-center">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <Users className="h-10 w-10 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{member.name}</h3>
                <p className="text-blue-600 font-medium mb-3">{member.role}</p>
                <p className="text-gray-600">{member.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Technology Stack</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built with the most advanced technologies to ensure performance, security, and scalability.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white rounded-lg p-6 text-center">
              <h3 className="font-semibold text-gray-900 mb-2">Backend</h3>
              <p className="text-gray-600 text-sm">FastAPI, Python, PostgreSQL, Redis</p>
            </div>
            <div className="bg-white rounded-lg p-6 text-center">
              <h3 className="font-semibold text-gray-900 mb-2">Frontend</h3>
              <p className="text-gray-600 text-sm">Next.js, React, TypeScript, Tailwind CSS</p>
            </div>
            <div className="bg-white rounded-lg p-6 text-center">
              <h3 className="font-semibold text-gray-900 mb-2">AI & ML</h3>
              <p className="text-gray-600 text-sm">OpenAI, Anthropic, LangChain, Custom Models</p>
            </div>
            <div className="bg-white rounded-lg p-6 text-center">
              <h3 className="font-semibold text-gray-900 mb-2">Infrastructure</h3>
              <p className="text-gray-600 text-sm">Docker, Kubernetes, AWS, Azure, GCP</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-4">Ready to Experience the Future?</h2>
          <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
            Join thousands of organizations that trust CloudMind for their cloud engineering needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/register"
              className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200"
            >
              Start Free Trial
            </a>
            <a
              href="/login"
              className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors duration-200"
            >
              Sign In
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-blue-600 rounded-lg">
                  <Globe className="h-6 w-6 text-white" />
                </div>
                <span className="text-xl font-bold">CloudMind</span>
              </div>
              <p className="text-gray-400">
                The world's most advanced cloud engineering platform.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Features</a></li>
                <li><a href="#" className="hover:text-white">Pricing</a></li>
                <li><a href="#" className="hover:text-white">Documentation</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">About</a></li>
                <li><a href="#" className="hover:text-white">Contact</a></li>
                <li><a href="#" className="hover:text-white">Careers</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Help Center</a></li>
                <li><a href="#" className="hover:text-white">API Docs</a></li>
                <li><a href="#" className="hover:text-white">Status</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 CloudMind. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
} 