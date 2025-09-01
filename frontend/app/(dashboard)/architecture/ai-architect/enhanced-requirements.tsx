"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Checkbox } from '@/components/ui/checkbox'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Loader2, Sparkles, Shield, Zap, TrendingUp, Database, Globe, Lock, Download, Share } from 'lucide-react'

interface Requirement {
  id: string
  title: string
  description: string
  category: string
  priority: 'low' | 'medium' | 'high' | 'critical'
  complexity: 'simple' | 'moderate' | 'complex' | 'enterprise'
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
  real_time_insights: any[]
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
  real_time_data: any[]
}

export default function EnhancedRequirementsPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState(1)
  const [requirements, setRequirements] = useState<Requirement[]>([])
  const [architectureRecommendations, setArchitectureRecommendations] = useState<ArchitectureRecommendation[]>([])
  const [technologyRecommendations, setTechnologyRecommendations] = useState<TechnologyRecommendation[]>([])
  const [realTimeKnowledge, setRealTimeKnowledge] = useState<any>({})
  const [selectedArchitecture, setSelectedArchitecture] = useState<string>('')
  const [projectTemplate, setProjectTemplate] = useState<any>(null)

  // Form state
  const [projectDescription, setProjectDescription] = useState('')
  const [businessGoals, setBusinessGoals] = useState<string[]>([])
  const [technicalConstraints, setTechnicalConstraints] = useState<string[]>([])
  const [teamSize, setTeamSize] = useState(5)
  const [timeline, setTimeline] = useState('3-6 months')
  const [budget, setBudget] = useState('')
  const [domain, setDomain] = useState('')
  const [scale, setScale] = useState('startup')
  const [securityLevel, setSecurityLevel] = useState('standard')
  const [performanceRequirements, setPerformanceRequirements] = useState('moderate')
  const [complianceFrameworks, setComplianceFrameworks] = useState<string[]>([])

  const businessGoalOptions = [
    'Cost optimization',
    'Scalability',
    'Security compliance',
    'Performance',
    'User experience',
    'Time to market',
    'Maintainability',
    'Innovation'
  ]

  const technicalConstraintOptions = [
    'Legacy system integration',
    'Regulatory compliance',
    'Performance requirements',
    'Security requirements',
    'Budget constraints',
    'Team expertise',
    'Technology preferences',
    'Infrastructure limitations'
  ]

  const complianceFrameworkOptions = [
    'SOC2',
    'HIPAA',
    'PCI DSS',
    'ISO27001',
    'GDPR',
    'CIS',
    'NIST',
    'FedRAMP'
  ]

  const handleAnalyzeRequirements = async () => {
    setIsLoading(true)
    setProgress(0)
    setCurrentStep(1)

    try {
      // Step 1: Requirements Analysis
      setProgress(20)
      setCurrentStep(1)
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Step 2: Real-time Knowledge Gathering
      setProgress(40)
      setCurrentStep(2)
      await new Promise(resolve => setTimeout(resolve, 1500))

      // Step 3: Architecture Recommendations
      setProgress(60)
      setCurrentStep(3)
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Step 4: Technology Recommendations
      setProgress(80)
      setCurrentStep(4)
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Step 5: Project Template Generation
      setProgress(100)
      setCurrentStep(5)
      await new Promise(resolve => setTimeout(resolve, 500))

      // Simulate API call to enhanced architecture engine
      const response = await fetch('/api/v1/ai/enhanced-requirements-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          project_description: projectDescription,
          business_goals: businessGoals,
          technical_constraints: technicalConstraints,
          team_size: teamSize,
          timeline,
          budget,
          domain,
          scale,
          security_level: securityLevel,
          performance_requirements: performanceRequirements,
          compliance_frameworks: complianceFrameworks
        })
      })

      if (response.ok) {
        const data = await response.json()
        setRequirements(data.requirements || [])
        setArchitectureRecommendations(data.architecture_recommendations || [])
        setTechnologyRecommendations(data.technology_recommendations || [])
        setRealTimeKnowledge(data.real_time_knowledge || {})
        setProjectTemplate(data.project_template || null)
      }

    } catch (error) {
      console.error('Error analyzing requirements:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleBusinessGoalToggle = (goal: string) => {
    setBusinessGoals(prev => 
      prev.includes(goal) 
        ? prev.filter(g => g !== goal)
        : [...prev, goal]
    )
  }

  const handleTechnicalConstraintToggle = (constraint: string) => {
    setTechnicalConstraints(prev => 
      prev.includes(constraint) 
        ? prev.filter(c => c !== constraint)
        : [...prev, constraint]
    )
  }

  const handleComplianceFrameworkToggle = (framework: string) => {
    setComplianceFrameworks(prev => 
      prev.includes(framework) 
        ? prev.filter(f => f !== framework)
        : [...prev, framework]
    )
  }

  const getStepIcon = (step: number) => {
    switch (step) {
      case 1: return <Sparkles className="h-4 w-4" />
      case 2: return <Database className="h-4 w-4" />
      case 3: return <Globe className="h-4 w-4" />
      case 4: return <Zap className="h-4 w-4" />
      case 5: return <Shield className="h-4 w-4" />
      default: return <TrendingUp className="h-4 w-4" />
    }
  }

  const getStepDescription = (step: number) => {
    switch (step) {
      case 1: return "Analyzing requirements and constraints..."
      case 2: return "Gathering real-time knowledge from multiple sources..."
      case 3: return "Generating architecture recommendations..."
      case 4: return "Evaluating technology stack options..."
      case 5: return "Creating comprehensive project template..."
      default: return "Processing..."
    }
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Enhanced AI Architect</h1>
          <p className="text-muted-foreground">
            Get expert architecture recommendations with real-time knowledge from multiple sources
          </p>
        </div>
        <Badge variant="secondary" className="flex items-center gap-2">
          <Sparkles className="h-3 w-3" />
          Enhanced with Real-time Data
        </Badge>
      </div>

      <Tabs defaultValue="requirements" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="requirements">Requirements</TabsTrigger>
          <TabsTrigger value="analysis">Analysis</TabsTrigger>
          <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
          <TabsTrigger value="template">Project Template</TabsTrigger>
        </TabsList>

        <TabsContent value="requirements" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Project Requirements</CardTitle>
              <CardDescription>
                Provide detailed information about your project to get expert recommendations
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="project-description">Project Description</Label>
                  <Textarea
                    id="project-description"
                    placeholder="Describe your project, its purpose, and key features..."
                    value={projectDescription}
                    onChange={(e) => setProjectDescription(e.target.value)}
                    rows={4}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="domain">Domain/Industry</Label>
                  <Input
                    id="domain"
                    placeholder="e.g., E-commerce, Healthcare, FinTech"
                    value={domain}
                    onChange={(e) => setDomain(e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="team-size">Team Size</Label>
                  <Select value={teamSize.toString()} onValueChange={(value) => setTeamSize(parseInt(value))}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1">1-2 developers</SelectItem>
                      <SelectItem value="3">3-5 developers</SelectItem>
                      <SelectItem value="6">6-10 developers</SelectItem>
                      <SelectItem value="11">11-20 developers</SelectItem>
                      <SelectItem value="21">20+ developers</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="timeline">Timeline</Label>
                  <Select value={timeline} onValueChange={setTimeline}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1-3 months">1-3 months</SelectItem>
                      <SelectItem value="3-6 months">3-6 months</SelectItem>
                      <SelectItem value="6-12 months">6-12 months</SelectItem>
                      <SelectItem value="12+ months">12+ months</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="scale">Project Scale</Label>
                  <Select value={scale} onValueChange={setScale}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="startup">Startup</SelectItem>
                      <SelectItem value="small_team">Small Team</SelectItem>
                      <SelectItem value="enterprise">Enterprise</SelectItem>
                      <SelectItem value="enterprise_plus">Enterprise+</SelectItem>
                      <SelectItem value="global_scale">Global Scale</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="budget">Budget Range</Label>
                  <Input
                    id="budget"
                    placeholder="e.g., $50K-$100K, $100K-$500K"
                    value={budget}
                    onChange={(e) => setBudget(e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="security-level">Security Level</Label>
                  <Select value={securityLevel} onValueChange={setSecurityLevel}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="basic">Basic</SelectItem>
                      <SelectItem value="standard">Standard</SelectItem>
                      <SelectItem value="enhanced">Enhanced</SelectItem>
                      <SelectItem value="enterprise">Enterprise</SelectItem>
                      <SelectItem value="government">Government</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="performance">Performance Requirements</Label>
                  <Select value={performanceRequirements} onValueChange={setPerformanceRequirements}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="basic">Basic</SelectItem>
                      <SelectItem value="moderate">Moderate</SelectItem>
                      <SelectItem value="high">High</SelectItem>
                      <SelectItem value="extreme">Extreme</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <Label>Business Goals</Label>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2">
                    {businessGoalOptions.map((goal) => (
                      <div key={goal} className="flex items-center space-x-2">
                        <Checkbox
                          id={goal}
                          checked={businessGoals.includes(goal)}
                          onCheckedChange={() => handleBusinessGoalToggle(goal)}
                        />
                        <Label htmlFor={goal} className="text-sm">{goal}</Label>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <Label>Technical Constraints</Label>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2">
                    {technicalConstraintOptions.map((constraint) => (
                      <div key={constraint} className="flex items-center space-x-2">
                        <Checkbox
                          id={constraint}
                          checked={technicalConstraints.includes(constraint)}
                          onCheckedChange={() => handleTechnicalConstraintToggle(constraint)}
                        />
                        <Label htmlFor={constraint} className="text-sm">{constraint}</Label>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <Label>Compliance Frameworks</Label>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2">
                    {complianceFrameworkOptions.map((framework) => (
                      <div key={framework} className="flex items-center space-x-2">
                        <Checkbox
                          id={framework}
                          checked={complianceFrameworks.includes(framework)}
                          onCheckedChange={() => handleComplianceFrameworkToggle(framework)}
                        />
                        <Label htmlFor={framework} className="text-sm">{framework}</Label>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <Button 
                onClick={handleAnalyzeRequirements}
                disabled={isLoading || !projectDescription}
                className="w-full"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing Requirements...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Analyze Requirements with AI
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analysis" className="space-y-6">
          {isLoading ? (
            <Card>
              <CardContent className="pt-6">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Analysis Progress</span>
                    <span className="text-sm text-muted-foreground">{progress}%</span>
                  </div>
                  <Progress value={progress} className="w-full" />
                  
                  <div className="flex items-center space-x-2">
                    {getStepIcon(currentStep)}
                    <span className="text-sm">{getStepDescription(currentStep)}</span>
                  </div>

                  <Alert>
                    <AlertDescription>
                      Gathering real-time data from multiple sources including:
                      <ul className="list-disc list-inside mt-2 space-y-1">
                        <li>Security vulnerability databases (NVD, CVE)</li>
                        <li>Cloud pricing APIs (AWS, Azure, GCP)</li>
                        <li>Technology trends (Stack Overflow, GitHub)</li>
                        <li>Compliance frameworks (NIST, ISO)</li>
                        <li>Performance benchmarks</li>
                        <li>Networking standards</li>
                      </ul>
                    </AlertDescription>
                  </Alert>
                </div>
              </CardContent>
            </Card>
          ) : requirements.length > 0 ? (
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Requirements Analysis</CardTitle>
                  <CardDescription>
                    AI-analyzed requirements with real-time knowledge integration
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {requirements.map((req) => (
                      <div key={req.id} className="border rounded-lg p-4">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-semibold">{req.title}</h3>
                          <div className="flex gap-2">
                            <Badge variant={req.priority === 'critical' ? 'destructive' : 'secondary'}>
                              {req.priority}
                            </Badge>
                            <Badge variant="outline">{req.complexity}</Badge>
                          </div>
                        </div>
                        <p className="text-sm text-muted-foreground mb-3">{req.description}</p>
                        
                        {req.acceptance_criteria.length > 0 && (
                          <div className="mb-3">
                            <h4 className="text-sm font-medium mb-1">Acceptance Criteria:</h4>
                            <ul className="list-disc list-inside text-sm space-y-1">
                              {req.acceptance_criteria.map((criteria, index) => (
                                <li key={index}>{criteria}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {Object.keys(realTimeKnowledge).length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Real-time Knowledge Sources</CardTitle>
                    <CardDescription>
                      Data gathered from authoritative sources for enhanced recommendations
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {Object.entries(realTimeKnowledge).map(([category, entries]: [string, any]) => (
                        <div key={category} className="border rounded-lg p-4">
                          <h3 className="font-semibold mb-2 capitalize">{category.replace('_', ' ')}</h3>
                          <p className="text-sm text-muted-foreground mb-2">
                            {Array.isArray(entries) ? entries.length : 0} entries found
                          </p>
                          {Array.isArray(entries) && entries.slice(0, 3).map((entry: any, index: number) => (
                            <div key={index} className="text-sm mb-1">
                              • {entry.title}
                            </div>
                          ))}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          ) : (
            <Card>
              <CardContent className="pt-6">
                <div className="text-center text-muted-foreground">
                  Complete the requirements form and click "Analyze Requirements" to see the analysis
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="recommendations" className="space-y-6">
          {architectureRecommendations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Architecture Recommendations</CardTitle>
                <CardDescription>
                  AI-generated architecture recommendations with real-time insights
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {architectureRecommendations.map((arch) => (
                    <div key={arch.id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold text-lg">{arch.name}</h3>
                        <Button
                          variant={selectedArchitecture === arch.id ? "default" : "outline"}
                          size="sm"
                          onClick={() => setSelectedArchitecture(arch.id)}
                        >
                          {selectedArchitecture === arch.id ? "Selected" : "Select"}
                        </Button>
                      </div>
                      
                      <p className="text-sm text-muted-foreground mb-4">{arch.description}</p>
                      
                      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-4">
                        <div className="text-center">
                          <div className="text-2xl font-bold text-blue-600">{Math.round(arch.complexity_score * 100)}%</div>
                          <div className="text-xs text-muted-foreground">Complexity</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-green-600">{Math.round(arch.scalability_score * 100)}%</div>
                          <div className="text-xs text-muted-foreground">Scalability</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-purple-600">{Math.round(arch.maintainability_score * 100)}%</div>
                          <div className="text-xs text-muted-foreground">Maintainability</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-orange-600">{Math.round(arch.cost_score * 100)}%</div>
                          <div className="text-xs text-muted-foreground">Cost Efficiency</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-red-600">{Math.round(arch.security_score * 100)}%</div>
                          <div className="text-xs text-muted-foreground">Security</div>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <h4 className="font-medium mb-2">Pros</h4>
                          <ul className="list-disc list-inside text-sm space-y-1">
                            {arch.pros.map((pro, index) => (
                              <li key={index}>{pro}</li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <h4 className="font-medium mb-2">Cons</h4>
                          <ul className="list-disc list-inside text-sm space-y-1">
                            {arch.cons.map((con, index) => (
                              <li key={index}>{con}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {technologyRecommendations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Technology Recommendations</CardTitle>
                <CardDescription>
                  AI-recommended technology stack with real-time market data
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {technologyRecommendations.map((tech) => (
                    <div key={tech.id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold">{tech.name}</h3>
                        <Badge variant="outline">{tech.category}</Badge>
                      </div>
                      
                      <p className="text-sm text-muted-foreground mb-4">{tech.description}</p>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                        <div>
                          <div className="text-sm font-medium">Learning Curve</div>
                          <div className="text-xs text-muted-foreground">{tech.learning_curve}</div>
                        </div>
                        <div>
                          <div className="text-sm font-medium">Community Support</div>
                          <div className="text-xs text-muted-foreground">{tech.community_support}</div>
                        </div>
                        <div>
                          <div className="text-sm font-medium">Enterprise Adoption</div>
                          <div className="text-xs text-muted-foreground">{tech.enterprise_adoption}</div>
                        </div>
                        <div>
                          <div className="text-sm font-medium">Cost Considerations</div>
                          <div className="text-xs text-muted-foreground">{tech.cost_considerations}</div>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <h4 className="font-medium mb-2">Use Cases</h4>
                          <ul className="list-disc list-inside text-sm space-y-1">
                            {tech.use_cases.map((useCase, index) => (
                              <li key={index}>{useCase}</li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <h4 className="font-medium mb-2">Security Features</h4>
                          <ul className="list-disc list-inside text-sm space-y-1">
                            {tech.security_features.map((feature, index) => (
                              <li key={index}>{feature}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="template" className="space-y-6">
          {projectTemplate ? (
            <Card>
              <CardHeader>
                <CardTitle>Generated Project Template</CardTitle>
                <CardDescription>
                  Complete project structure and configuration based on your requirements
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div>
                    <h3 className="font-semibold mb-2">Project Structure</h3>
                    <div className="bg-muted p-4 rounded-lg">
                      <pre className="text-sm overflow-x-auto">
                        {JSON.stringify(projectTemplate.project_structure, null, 2)}
                      </pre>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="font-semibold mb-2">Setup Instructions</h3>
                    <ol className="list-decimal list-inside space-y-2">
                      {projectTemplate.setup_instructions?.map((instruction: string, index: number) => (
                        <li key={index} className="text-sm">{instruction}</li>
                      ))}
                    </ol>
                  </div>
                  
                  <div>
                    <h3 className="font-semibold mb-2">Configuration Files</h3>
                    <div className="space-y-2">
                      {Object.entries(projectTemplate.configuration_files || {}).map(([filename, content]: [string, any]) => (
                        <div key={filename} className="border rounded-lg p-3">
                          <div className="font-medium text-sm mb-2">{filename}</div>
                          <pre className="text-xs bg-muted p-2 rounded overflow-x-auto">
                            {content}
                          </pre>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="flex gap-2">
                    <Button>
                      <Download className="mr-2 h-4 w-4" />
                      Download Template
                    </Button>
                    <Button variant="outline">
                      <Share className="mr-2 h-4 w-4" />
                      Share Template
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="pt-6">
                <div className="text-center text-muted-foreground">
                  Select an architecture recommendation to generate the project template
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
} 