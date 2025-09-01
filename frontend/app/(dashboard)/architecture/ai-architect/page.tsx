'use client'

import { useState, useEffect } from 'react'
import DashboardLayout from '@/components/layouts/DashboardLayout'
import { 
  Brain,
  Lightbulb,
  Code,
  Database,
  Shield,
  Cloud,
  Network,
  Server,
  Zap,
  BookOpen,
  Search,
  Compare,
  FileText,
  Settings,
  Play,
  Download,
  Share2,
  Star,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Users,
  Target,
  BarChart3,
  Layers,
  GitBranch,
  Globe,
  Lock,
  Activity,
  Cpu,
  HardDrive,
  Wifi,
  Database as DatabaseIcon,
  Code2,
  Palette,
  Rocket,
  GitCommit,
  GitPullRequest,
  GitMerge,
  GitBranch as GitBranchIcon,
  GitCommit as GitCommitIcon,
  GitPullRequest as GitPullRequestIcon,
  GitMerge as GitMergeIcon,
  GitBranch as GitBranchIcon2,
  GitCommit as GitCommitIcon2,
  GitPullRequest as GitPullRequestIcon2,
  GitMerge as GitMergeIcon2
} from 'lucide-react'

interface Requirement {
  id: string
  title: string
  description: string
  category: string
  priority: string
  complexity: string
  dependencies: string[]
  acceptance_criteria: string[]
  constraints: string[]
  assumptions: string[]
}

interface ArchitectureRecommendation {
  id: string
  name: string
  description: string
  architecture_type: string
  pros: string[]
  cons: string[]
  complexity_score: number
  scalability_score: number
  maintainability_score: number
  cost_score: number
  security_score: number
  technology_stack: Record<string, string[]>
  implementation_steps: string[]
  risks: string[]
  alternatives: string[]
}

interface TechnologyRecommendation {
  id: string
  name: string
  category: string
  description: string
  pros: string[]
  cons: string[]
  use_cases: string[]
  alternatives: string[]
  learning_curve: string
  community_support: string
  enterprise_adoption: string
  cost_considerations: string
  security_features: string[]
  performance_characteristics: Record<string, any>
}

interface ProjectTemplate {
  id: string
  name: string
  description: string
  architecture_type: string
  technology_stack: Record<string, string[]>
  project_structure: Record<string, any>
  setup_instructions: string[]
  configuration_files: Record<string, string>
  deployment_scripts: string[]
  testing_strategy: Record<string, any>
  monitoring_setup: Record<string, any>
  security_configuration: Record<string, any>
}

interface KnowledgeBaseEntry {
  category: string
  topic: string
  content: Record<string, any>
  related_topics: string[]
  best_practices: string[]
  common_pitfalls: string[]
  implementation_guide: string[]
}

export default function AIArchitectPage() {
  const [activeTab, setActiveTab] = useState('requirements')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResults, setAnalysisResults] = useState<any>(null)
  
  // Requirements Analysis State
  const [projectDescription, setProjectDescription] = useState('')
  const [businessGoals, setBusinessGoals] = useState<string[]>([''])
  const [technicalConstraints, setTechnicalConstraints] = useState<string[]>([''])
  const [teamSize, setTeamSize] = useState(5)
  const [timeline, setTimeline] = useState('3 months')
  const [budget, setBudget] = useState('')
  
  // Architecture Design State
  const [selectedArchitecture, setSelectedArchitecture] = useState<string>('')
  const [architecturePreferences, setArchitecturePreferences] = useState<Record<string, any>>({})
  
  // Technology Comparison State
  const [selectedCategory, setSelectedCategory] = useState('programming_languages')
  const [technologiesToCompare, setTechnologiesToCompare] = useState<string[]>([])
  const [comparisonResults, setComparisonResults] = useState<any>(null)
  
  // Knowledge Base State
  const [knowledgeCategory, setKnowledgeCategory] = useState('security')
  const [knowledgeTopic, setKnowledgeTopic] = useState('')
  const [knowledgeResults, setKnowledgeResults] = useState<KnowledgeBaseEntry | null>(null)
  
  // Project Templates State
  const [selectedTemplate, setSelectedTemplate] = useState<string>('')
  const [templateResults, setTemplateResults] = useState<ProjectTemplate | null>(null)

  const categories = [
    { id: 'security', name: 'Security', icon: Shield },
    { id: 'cloud', name: 'Cloud', icon: Cloud },
    { id: 'networking', name: 'Networking', icon: Network },
    { id: 'distributed_systems', name: 'Distributed Systems', icon: Server },
    { id: 'databases', name: 'Databases', icon: DatabaseIcon }
  ]

  const technologyCategories = [
    { id: 'programming_languages', name: 'Programming Languages', icon: Code },
    { id: 'frameworks', name: 'Frameworks', icon: Layers },
    { id: 'databases', name: 'Databases', icon: Database },
    { id: 'cloud_providers', name: 'Cloud Providers', icon: Cloud },
    { id: 'containers', name: 'Containers', icon: Cpu },
    { id: 'monitoring', name: 'Monitoring', icon: Activity }
  ]

  const architectureTypes = [
    { id: 'microservices', name: 'Microservices', description: 'Distributed system with loosely coupled services' },
    { id: 'monolith', name: 'Monolith', description: 'Single application with all functionality' },
    { id: 'serverless', name: 'Serverless', description: 'Event-driven, auto-scaling functions' },
    { id: 'event_driven', name: 'Event-Driven', description: 'Asynchronous communication via events' },
    { id: 'clean_architecture', name: 'Clean Architecture', description: 'Layered architecture with dependency inversion' }
  ]

  const projectTemplates = [
    { id: 'microservices_api', name: 'Microservices API', description: 'Scalable microservices architecture' },
    { id: 'serverless_app', name: 'Serverless Application', description: 'Event-driven serverless architecture' },
    { id: 'monolith_webapp', name: 'Monolithic Web App', description: 'Traditional monolithic web application' }
  ]

  const handleAnalyzeRequirements = async () => {
    setIsAnalyzing(true)
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // Mock analysis results
      const mockResults = {
        requirements: [
          {
            id: '1',
            title: 'User Authentication System',
            description: 'Secure user authentication with JWT tokens',
            category: 'Security',
            priority: 'high',
            complexity: 'medium',
            dependencies: ['Database', 'Email Service'],
            acceptance_criteria: ['Users can register', 'Users can login', 'Password reset functionality'],
            constraints: ['Must be SOC2 compliant', 'Must support OAuth'],
            assumptions: ['Users have email addresses', 'Database is PostgreSQL']
          }
        ],
        architecture_recommendations: [
          {
            id: '1',
            name: 'Microservices Architecture',
            description: 'Distributed system with loosely coupled services',
            architecture_type: 'microservices',
            pros: ['Scalable', 'Team autonomy', 'Technology diversity'],
            cons: ['Complex deployment', 'Network latency', 'Data consistency'],
            complexity_score: 0.8,
            scalability_score: 0.9,
            maintainability_score: 0.7,
            cost_score: 0.6,
            security_score: 0.8,
            technology_stack: {
              'backend': ['FastAPI', 'Django', 'Spring Boot'],
              'database': ['PostgreSQL', 'MongoDB', 'Redis'],
              'message_queue': ['RabbitMQ', 'Apache Kafka']
            },
            implementation_steps: ['Design API contracts', 'Set up service mesh', 'Implement authentication'],
            risks: ['Service discovery complexity', 'Data consistency challenges'],
            alternatives: ['Monolith', 'Serverless']
          }
        ],
        technology_recommendations: [
          {
            id: '1',
            name: 'FastAPI',
            category: 'framework',
            description: 'Modern Python web framework for building APIs',
            pros: ['Fast performance', 'Automatic documentation', 'Type hints'],
            cons: ['Python ecosystem', 'Learning curve'],
            use_cases: ['API development', 'Microservices', 'Real-time applications'],
            alternatives: ['Django', 'Flask', 'Express.js'],
            learning_curve: 'Low',
            community_support: 'High',
            enterprise_adoption: 'Medium',
            cost_considerations: 'Open source',
            security_features: ['Built-in validation', 'CORS support', 'Rate limiting'],
            performance_characteristics: {
              'requests_per_second': 50000,
              'memory_usage': 'Low',
              'startup_time': 'Fast'
            }
          }
        ],
        project_plan: {
          phases: [
            { name: 'Planning', duration: '2 weeks', tasks: ['Requirements gathering', 'Architecture design'] },
            { name: 'Development', duration: '8 weeks', tasks: ['Core development', 'Testing'] },
            { name: 'Deployment', duration: '2 weeks', tasks: ['Infrastructure setup', 'Production deployment'] }
          ],
          timeline: '12 weeks',
          budget: '$50,000',
          team_structure: {
            'backend_developers': 3,
            'frontend_developers': 2,
            'devops_engineer': 1,
            'qa_engineer': 1
          }
        },
        risk_assessment: {
          high_risks: ['Data consistency in microservices', 'Service discovery complexity'],
          medium_risks: ['Team learning curve', 'Infrastructure costs'],
          low_risks: ['Third-party dependencies', 'Documentation maintenance']
        },
        cost_estimation: {
          development: 30000,
          infrastructure: 10000,
          tools: 5000,
          maintenance: 5000,
          total: 50000
        }
      }
      
      setAnalysisResults(mockResults)
    } catch (error) {
      console.error('Analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleCompareTechnologies = async () => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      const mockComparison = {
        technologies: {
          'FastAPI': {
            description: 'Modern Python web framework',
            pros: ['Fast performance', 'Automatic documentation'],
            cons: ['Python ecosystem', 'Learning curve'],
            use_cases: ['API development', 'Microservices']
          },
          'Django': {
            description: 'Full-featured Python web framework',
            pros: ['Batteries included', 'Admin interface'],
            cons: ['Heavy', 'Less flexible'],
            use_cases: ['Full-stack applications', 'Rapid prototyping']
          },
          'Express.js': {
            description: 'Minimal Node.js web framework',
            pros: ['Lightweight', 'Flexible', 'Large ecosystem'],
            cons: ['Less opinionated', 'Security concerns'],
            use_cases: ['APIs', 'Real-time applications']
          }
        },
        comparison_matrix: {
          performance: { 'FastAPI': 9, 'Django': 7, 'Express.js': 8 },
          learning_curve: { 'FastAPI': 8, 'Django': 6, 'Express.js': 7 },
          ecosystem: { 'FastAPI': 7, 'Django': 9, 'Express.js': 9 },
          security: { 'FastAPI': 9, 'Django': 8, 'Express.js': 6 }
        },
        recommendations: [
          {
            technology: 'FastAPI',
            reason: 'Best for API-first development with high performance requirements',
            confidence: 0.9
          }
        ]
      }
      
      setComparisonResults(mockComparison)
    } catch (error) {
      console.error('Technology comparison failed:', error)
    }
  }

  const handleKnowledgeBaseSearch = async () => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const mockKnowledgeEntry: KnowledgeBaseEntry = {
        category: 'security',
        topic: 'OWASP Top 10',
        content: {
          description: 'The OWASP Top 10 is a standard awareness document for developers and web application security.',
          items: [
            'Injection',
            'Broken Authentication',
            'Sensitive Data Exposure',
            'XML External Entities (XXE)',
            'Broken Access Control',
            'Security Misconfiguration',
            'Cross-Site Scripting (XSS)',
            'Insecure Deserialization',
            'Using Components with Known Vulnerabilities',
            'Insufficient Logging & Monitoring'
          ]
        },
        related_topics: ['Authentication', 'Authorization', 'Input Validation', 'Output Encoding'],
        best_practices: [
          'Use parameterized queries',
          'Implement proper authentication',
          'Encrypt sensitive data',
          'Validate all inputs',
          'Use HTTPS everywhere'
        ],
        common_pitfalls: [
          'Storing passwords in plain text',
          'Not validating user inputs',
          'Using outdated libraries',
          'Poor error handling'
        ],
        implementation_guide: [
          'Conduct security assessment',
          'Implement security controls',
          'Regular security testing',
          'Security training for team'
        ]
      }
      
      setKnowledgeResults(mockKnowledgeEntry)
    } catch (error) {
      console.error('Knowledge base search failed:', error)
    }
  }

  const handleGenerateTemplate = async () => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      const mockTemplate: ProjectTemplate = {
        id: '1',
        name: 'Microservices API Template',
        description: 'Comprehensive template for microservices architecture',
        architecture_type: 'microservices',
        technology_stack: {
          'backend': ['FastAPI', 'Django', 'Spring Boot'],
          'database': ['PostgreSQL', 'MongoDB', 'Redis'],
          'message_queue': ['RabbitMQ', 'Apache Kafka'],
          'container': ['Docker', 'Kubernetes'],
          'monitoring': ['Prometheus', 'Grafana', 'Jaeger']
        },
        project_structure: {
          'services': ['auth-service', 'user-service', 'product-service'],
          'shared': ['common-lib', 'api-gateway', 'service-registry']
        },
        setup_instructions: [
          'Clone the template repository',
          'Install dependencies',
          'Configure environment variables',
          'Set up database connections',
          'Start development servers'
        ],
        configuration_files: {
          'docker-compose.yml': 'Docker Compose configuration',
          'kubernetes.yaml': 'Kubernetes deployment manifests',
          '.env.example': 'Environment variables template'
        },
        deployment_scripts: [
          'deploy.sh - Production deployment script',
          'setup-dev.sh - Development environment setup',
          'migrate.sh - Database migration script'
        ],
        testing_strategy: {
          'unit_tests': 'Jest/PyTest for unit testing',
          'integration_tests': 'API testing with Postman/Newman',
          'e2e_tests': 'Cypress for end-to-end testing'
        },
        monitoring_setup: {
          'metrics': 'Prometheus for metrics collection',
          'logging': 'ELK stack for log aggregation',
          'tracing': 'Jaeger for distributed tracing'
        },
        security_configuration: {
          'authentication': 'JWT-based authentication',
          'authorization': 'Role-based access control',
          'encryption': 'TLS for data in transit',
          'secrets': 'HashiCorp Vault for secrets management'
        }
      }
      
      setTemplateResults(mockTemplate)
    } catch (error) {
      console.error('Template generation failed:', error)
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">AI Architect</h1>
            <p className="text-gray-600">World-class AI-powered architecture design and engineering intelligence</p>
          </div>
          <div className="flex items-center space-x-2">
            <Brain className="w-8 h-8 text-blue-600" />
            <span className="text-sm font-medium text-blue-600">AI-Powered</span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'requirements', name: 'Requirements Analysis', icon: FileText },
              { id: 'architecture', name: 'Architecture Design', icon: Layers },
              { id: 'technology', name: 'Technology Comparison', icon: Compare },
              { id: 'knowledge', name: 'Knowledge Base', icon: BookOpen },
              { id: 'templates', name: 'Project Templates', icon: Code }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Requirements Analysis Tab */}
        {activeTab === 'requirements' && (
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Requirements</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Project Description
                  </label>
                  <textarea
                    value={projectDescription}
                    onChange={(e) => setProjectDescription(e.target.value)}
                    className="input-field h-32"
                    placeholder="Describe your project, its goals, and key features..."
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Business Goals
                    </label>
                    {businessGoals.map((goal, index) => (
                      <div key={index} className="flex space-x-2 mb-2">
                        <input
                          type="text"
                          value={goal}
                          onChange={(e) => {
                            const newGoals = [...businessGoals]
                            newGoals[index] = e.target.value
                            setBusinessGoals(newGoals)
                          }}
                          className="input-field flex-1"
                          placeholder="Enter business goal..."
                        />
                        {businessGoals.length > 1 && (
                          <button
                            onClick={() => setBusinessGoals(businessGoals.filter((_, i) => i !== index))}
                            className="btn-secondary px-2"
                          >
                            Remove
                          </button>
                        )}
                      </div>
                    ))}
                    <button
                      onClick={() => setBusinessGoals([...businessGoals, ''])}
                      className="btn-secondary text-sm"
                    >
                      Add Goal
                    </button>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Technical Constraints
                    </label>
                    {technicalConstraints.map((constraint, index) => (
                      <div key={index} className="flex space-x-2 mb-2">
                        <input
                          type="text"
                          value={constraint}
                          onChange={(e) => {
                            const newConstraints = [...technicalConstraints]
                            newConstraints[index] = e.target.value
                            setTechnicalConstraints(newConstraints)
                          }}
                          className="input-field flex-1"
                          placeholder="Enter technical constraint..."
                        />
                        {technicalConstraints.length > 1 && (
                          <button
                            onClick={() => setTechnicalConstraints(technicalConstraints.filter((_, i) => i !== index))}
                            className="btn-secondary px-2"
                          >
                            Remove
                          </button>
                        )}
                      </div>
                    ))}
                    <button
                      onClick={() => setTechnicalConstraints([...technicalConstraints, ''])}
                      className="btn-secondary text-sm"
                    >
                      Add Constraint
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Team Size
                    </label>
                    <input
                      type="number"
                      value={teamSize}
                      onChange={(e) => setTeamSize(Number(e.target.value))}
                      className="input-field"
                      min="1"
                      max="50"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Timeline
                    </label>
                    <select
                      value={timeline}
                      onChange={(e) => setTimeline(e.target.value)}
                      className="input-field"
                    >
                      <option value="1 month">1 month</option>
                      <option value="3 months">3 months</option>
                      <option value="6 months">6 months</option>
                      <option value="1 year">1 year</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Budget (Optional)
                    </label>
                    <input
                      type="text"
                      value={budget}
                      onChange={(e) => setBudget(e.target.value)}
                      className="input-field"
                      placeholder="e.g., $50,000"
                    />
                  </div>
                </div>

                <div className="flex justify-center pt-4">
                  <button
                    onClick={handleAnalyzeRequirements}
                    disabled={isAnalyzing || !projectDescription.trim()}
                    className="btn-primary flex items-center space-x-2"
                  >
                    {isAnalyzing ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        <span>Analyzing...</span>
                      </>
                    ) : (
                      <>
                        <Brain className="w-4 h-4" />
                        <span>Analyze Requirements</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Analysis Results */}
            {analysisResults && (
              <div className="space-y-6">
                {/* Requirements */}
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Requirements Analysis</h3>
                  <div className="space-y-4">
                    {analysisResults.requirements?.map((req: Requirement) => (
                      <div key={req.id} className="p-4 bg-gray-50 rounded-lg">
                        <h4 className="font-medium text-gray-900">{req.title}</h4>
                        <p className="text-sm text-gray-600 mt-1">{req.description}</p>
                        <div className="flex items-center space-x-4 mt-2 text-xs">
                          <span className={`px-2 py-1 rounded-full ${
                            req.priority === 'high' ? 'bg-red-100 text-red-800' :
                            req.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {req.priority} priority
                          </span>
                          <span className="text-gray-500">{req.category}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Architecture Recommendations */}
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Architecture Recommendations</h3>
                  <div className="space-y-4">
                    {analysisResults.architecture_recommendations?.map((arch: ArchitectureRecommendation) => (
                      <div key={arch.id} className="p-4 border rounded-lg">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-medium text-gray-900">{arch.name}</h4>
                          <div className="flex items-center space-x-2">
                            <span className="text-sm text-gray-500">Score:</span>
                            <div className="flex items-center space-x-1">
                              {[arch.complexity_score, arch.scalability_score, arch.maintainability_score, arch.cost_score, arch.security_score].map((score, index) => (
                                <div
                                  key={index}
                                  className="w-2 h-2 rounded-full"
                                  style={{
                                    backgroundColor: score > 0.8 ? '#10B981' : score > 0.6 ? '#F59E0B' : '#EF4444'
                                  }}
                                />
                              ))}
                            </div>
                          </div>
                        </div>
                        <p className="text-sm text-gray-600 mb-3">{arch.description}</p>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <h5 className="text-sm font-medium text-gray-900 mb-2">Pros</h5>
                            <ul className="text-sm text-gray-600 space-y-1">
                              {arch.pros.map((pro, index) => (
                                <li key={index} className="flex items-center space-x-2">
                                  <CheckCircle className="w-3 h-3 text-green-500" />
                                  <span>{pro}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                          <div>
                            <h5 className="text-sm font-medium text-gray-900 mb-2">Cons</h5>
                            <ul className="text-sm text-gray-600 space-y-1">
                              {arch.cons.map((con, index) => (
                                <li key={index} className="flex items-center space-x-2">
                                  <AlertTriangle className="w-3 h-3 text-red-500" />
                                  <span>{con}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Project Plan */}
                {analysisResults.project_plan && (
                  <div className="card">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Plan</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="p-4 bg-blue-50 rounded-lg">
                        <h4 className="font-medium text-blue-900">Timeline</h4>
                        <p className="text-2xl font-bold text-blue-600">{analysisResults.project_plan.timeline}</p>
                      </div>
                      <div className="p-4 bg-green-50 rounded-lg">
                        <h4 className="font-medium text-green-900">Budget</h4>
                        <p className="text-2xl font-bold text-green-600">{analysisResults.project_plan.budget}</p>
                      </div>
                      <div className="p-4 bg-purple-50 rounded-lg">
                        <h4 className="font-medium text-purple-900">Team Size</h4>
                        <p className="text-2xl font-bold text-purple-600">
                          {Object.values(analysisResults.project_plan.team_structure).reduce((a: number, b: number) => a + b, 0)} members
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Technology Comparison Tab */}
        {activeTab === 'technology' && (
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Technology Comparison</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Technology Category
                  </label>
                  <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    className="input-field"
                  >
                    {technologyCategories.map((category) => (
                      <option key={category.id} value={category.id}>
                        {category.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Technologies to Compare
                  </label>
                  <div className="space-y-2">
                    {['FastAPI', 'Django', 'Express.js'].map((tech) => (
                      <label key={tech} className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={technologiesToCompare.includes(tech)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setTechnologiesToCompare([...technologiesToCompare, tech])
                            } else {
                              setTechnologiesToCompare(technologiesToCompare.filter(t => t !== tech))
                            }
                          }}
                          className="rounded border-gray-300"
                        />
                        <span className="text-sm text-gray-700">{tech}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div className="flex justify-center pt-4">
                  <button
                    onClick={handleCompareTechnologies}
                    disabled={technologiesToCompare.length < 2}
                    className="btn-primary flex items-center space-x-2"
                  >
                    <Compare className="w-4 h-4" />
                    <span>Compare Technologies</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Comparison Results */}
            {comparisonResults && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Comparison Results</h3>
                
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Technology
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Performance
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Learning Curve
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Ecosystem
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Security
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {Object.entries(comparisonResults.comparison_matrix.performance).map(([tech, score]) => (
                        <tr key={tech}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {tech}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            <div className="flex items-center space-x-2">
                              <div className="w-16 bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-blue-600 h-2 rounded-full"
                                  style={{ width: `${(score as number) * 10}%` }}
                                />
                              </div>
                              <span>{score}/10</span>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {comparisonResults.comparison_matrix.learning_curve[tech]}/10
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {comparisonResults.comparison_matrix.ecosystem[tech]}/10
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {comparisonResults.comparison_matrix.security[tech]}/10
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {comparisonResults.recommendations && (
                  <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                    <h4 className="font-medium text-blue-900 mb-2">Recommendation</h4>
                    {comparisonResults.recommendations.map((rec: any, index: number) => (
                      <div key={index} className="text-sm text-blue-800">
                        <strong>{rec.technology}</strong>: {rec.reason}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Knowledge Base Tab */}
        {activeTab === 'knowledge' && (
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Knowledge Base</h3>
              
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Category
                    </label>
                    <select
                      value={knowledgeCategory}
                      onChange={(e) => setKnowledgeCategory(e.target.value)}
                      className="input-field"
                    >
                      {categories.map((category) => (
                        <option key={category.id} value={category.id}>
                          {category.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Topic
                    </label>
                    <input
                      type="text"
                      value={knowledgeTopic}
                      onChange={(e) => setKnowledgeTopic(e.target.value)}
                      className="input-field"
                      placeholder="e.g., OWASP Top 10, Microservices..."
                    />
                  </div>
                </div>

                <div className="flex justify-center pt-4">
                  <button
                    onClick={handleKnowledgeBaseSearch}
                    disabled={!knowledgeTopic.trim()}
                    className="btn-primary flex items-center space-x-2"
                  >
                    <Search className="w-4 h-4" />
                    <span>Search Knowledge Base</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Knowledge Results */}
            {knowledgeResults && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  {knowledgeResults.topic} - {knowledgeResults.category}
                </h3>
                
                <div className="space-y-6">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Description</h4>
                    <p className="text-sm text-gray-600">{knowledgeResults.content.description}</p>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Key Items</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      {knowledgeResults.content.items?.map((item: string, index: number) => (
                        <li key={index} className="flex items-center space-x-2">
                          <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Best Practices</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {knowledgeResults.best_practices.map((practice: string, index: number) => (
                          <li key={index} className="flex items-center space-x-2">
                            <CheckCircle className="w-3 h-3 text-green-500" />
                            <span>{practice}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Common Pitfalls</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {knowledgeResults.common_pitfalls.map((pitfall: string, index: number) => (
                          <li key={index} className="flex items-center space-x-2">
                            <AlertTriangle className="w-3 h-3 text-red-500" />
                            <span>{pitfall}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Project Templates Tab */}
        {activeTab === 'templates' && (
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Templates</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select Template
                  </label>
                  <select
                    value={selectedTemplate}
                    onChange={(e) => setSelectedTemplate(e.target.value)}
                    className="input-field"
                  >
                    <option value="">Choose a template...</option>
                    {projectTemplates.map((template) => (
                      <option key={template.id} value={template.id}>
                        {template.name} - {template.description}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="flex justify-center pt-4">
                  <button
                    onClick={handleGenerateTemplate}
                    disabled={!selectedTemplate}
                    className="btn-primary flex items-center space-x-2"
                  >
                    <Code className="w-4 h-4" />
                    <span>Generate Template</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Template Results */}
            {templateResults && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">{templateResults.name}</h3>
                
                <div className="space-y-6">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Description</h4>
                    <p className="text-sm text-gray-600">{templateResults.description}</p>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Technology Stack</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {Object.entries(templateResults.technology_stack).map(([category, technologies]) => (
                        <div key={category} className="p-3 bg-gray-50 rounded-lg">
                          <h5 className="text-sm font-medium text-gray-900 mb-2 capitalize">
                            {category.replace('_', ' ')}
                          </h5>
                          <div className="flex flex-wrap gap-1">
                            {technologies.map((tech: string) => (
                              <span key={tech} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                                {tech}
                              </span>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Setup Instructions</h4>
                    <ol className="text-sm text-gray-600 space-y-1">
                      {templateResults.setup_instructions.map((instruction: string, index: number) => (
                        <li key={index} className="flex items-start space-x-2">
                          <span className="text-blue-600 font-medium">{index + 1}.</span>
                          <span>{instruction}</span>
                        </li>
                      ))}
                    </ol>
                  </div>

                  <div className="flex space-x-4">
                    <button className="btn-secondary flex items-center space-x-2">
                      <Download className="w-4 h-4" />
                      <span>Download Template</span>
                    </button>
                    <button className="btn-secondary flex items-center space-x-2">
                      <Share2 className="w-4 h-4" />
                      <span>Share Template</span>
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  )
} 