'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Zap, 
  Cloud, 
  Database, 
  Shield, 
  Server,
  HardDrive,
  Network,
  Cpu,
  MemoryStick,
  Activity,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Play,
  Pause,
  RotateCcw,
  Settings,
  Filter,
  Search,
  Download,
  Eye,
  TrendingUp,
  DollarSign,
  Layers,
  Globe
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';

// Mock data for infrastructure resources
const mockResources = [
  {
    id: 'i-0123456789abcdef0',
    name: 'web-server-prod-01',
    type: 'EC2 Instance',
    region: 'us-east-1',
    status: 'running',
    cost_monthly: 245.60,
    optimization_potential: 'high',
    recommendations: ['Rightsize to t3.medium', 'Enable detailed monitoring'],
    utilization: { cpu: 23, memory: 45, network: 12 },
    tags: { Environment: 'Production', Team: 'Frontend' }
  },
  {
    id: 'db-cluster-main',
    name: 'main-database-cluster',
    type: 'RDS MySQL',
    region: 'us-east-1',
    status: 'available',
    cost_monthly: 892.40,
    optimization_potential: 'medium',
    recommendations: ['Consider Aurora Serverless', 'Optimize storage'],
    utilization: { cpu: 67, memory: 78, connections: 34 },
    tags: { Environment: 'Production', Team: 'Backend' }
  },
  {
    id: 's3-bucket-assets',
    name: 'company-assets-bucket',
    type: 'S3 Bucket',
    region: 'us-east-1',
    status: 'active',
    cost_monthly: 156.20,
    optimization_potential: 'high',
    recommendations: ['Implement lifecycle policies', 'Use Intelligent Tiering'],
    utilization: { storage: 2.4, requests: 125000 },
    tags: { Environment: 'Production', Team: 'DevOps' }
  },
  {
    id: 'lb-main-prod',
    name: 'main-load-balancer',
    type: 'Application Load Balancer',
    region: 'us-east-1',
    status: 'active',
    cost_monthly: 67.80,
    optimization_potential: 'low',
    recommendations: ['Monitor unused target groups'],
    utilization: { requests: 45000, targets: 3 },
    tags: { Environment: 'Production', Team: 'Infrastructure' }
  },
  {
    id: 'cache-redis-01',
    name: 'session-cache-cluster',
    type: 'ElastiCache Redis',
    region: 'us-east-1',
    status: 'available',
    cost_monthly: 234.50,
    optimization_potential: 'medium',
    recommendations: ['Consider reserved instances', 'Optimize memory usage'],
    utilization: { memory: 56, connections: 89 },
    tags: { Environment: 'Production', Team: 'Backend' }
  }
];

const scanProgress = {
  total_resources: 247,
  scanned_resources: 165,
  progress_percentage: 67,
  estimated_completion: '4 minutes',
  current_phase: 'Analyzing cost optimization opportunities'
};

export default function InfrastructureScanner() {
  const [isScanning, setIsScanning] = useState(true);
  const [scanProgress, setScanProgress] = useState(67);
  const [selectedResource, setSelectedResource] = useState<any>(null);
  const [filterType, setFilterType] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Simulate scanning progress
  useEffect(() => {
    if (isScanning && scanProgress < 100) {
      const timer = setTimeout(() => {
        setScanProgress(prev => Math.min(prev + 1, 100));
      }, 200);
      return () => clearTimeout(timer);
    } else if (scanProgress >= 100) {
      setIsScanning(false);
    }
  }, [isScanning, scanProgress]);

  const getResourceIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'ec2 instance': return Server;
      case 'rds mysql': return Database;
      case 's3 bucket': return HardDrive;
      case 'application load balancer': return Network;
      case 'elasticache redis': return MemoryStick;
      default: return Cloud;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'running':
      case 'available':
      case 'active': return 'cyber-green';
      case 'stopped':
      case 'pending': return 'cyber-orange';
      case 'error':
      case 'failed': return 'cyber-pink';
      default: return 'cyber-cyan';
    }
  };

  const getOptimizationColor = (potential: string) => {
    switch (potential.toLowerCase()) {
      case 'high': return 'cyber-pink';
      case 'medium': return 'cyber-orange';
      case 'low': return 'cyber-green';
      default: return 'cyber-cyan';
    }
  };

  const filteredResources = mockResources.filter(resource => {
    const matchesType = filterType === 'all' || resource.type.toLowerCase().includes(filterType.toLowerCase());
    const matchesSearch = resource.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         resource.type.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesType && matchesSearch;
  });

  const totalMonthlyCost = mockResources.reduce((sum, resource) => sum + resource.cost_monthly, 0);
  const highOptimizationCount = mockResources.filter(r => r.optimization_potential === 'high').length;

  return (
    <div className="min-h-screen bg-cyber-black p-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="text-center mb-8">
          <h1 className="text-cyber-title mb-4">
            <Zap className="inline-block w-10 h-10 mr-4" />
            Infrastructure Scanner
          </h1>
          <p className="text-cyber-cyan/70 font-mono text-lg">
            Deep analysis of your cloud infrastructure for cost optimization opportunities
          </p>
        </div>
      </motion.div>

      {/* Scan Status */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="mb-8"
      >
        <Card className="card-cyber-glow">
          <CardHeader>
            <CardTitle className="text-cyber-cyan font-mono flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Activity className="w-5 h-5" />
                Scan Status
              </div>
              <div className="flex items-center gap-2">
                {isScanning ? (
                  <Button 
                    onClick={() => setIsScanning(false)}
                    className="btn-cyber-secondary"
                    size="sm"
                  >
                    <Pause className="w-4 h-4 mr-2" />
                    Pause
                  </Button>
                ) : (
                  <Button 
                    onClick={() => setIsScanning(true)}
                    className="btn-cyber-primary"
                    size="sm"
                  >
                    <Play className="w-4 h-4 mr-2" />
                    Resume
                  </Button>
                )}
                <Button className="btn-cyber-secondary" size="sm">
                  <RotateCcw className="w-4 h-4 mr-2" />
                  Restart
                </Button>
              </div>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-cyber-cyan text-sm">
                  {scanProgress.current_phase}
                </span>
                <span className="font-mono text-cyber-green text-sm">
                  {scanProgress.scanned_resources} / {scanProgress.total_resources} resources
                </span>
              </div>
              
              <Progress value={scanProgress} className="progress-cyber h-3" />
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-2xl font-mono font-bold text-cyber-cyan">
                    {scanProgress}%
                  </div>
                  <div className="text-cyber-cyan/60 font-mono text-xs">Complete</div>
                </div>
                <div>
                  <div className="text-2xl font-mono font-bold text-cyber-green">
                    {scanProgress.scanned_resources}
                  </div>
                  <div className="text-cyber-cyan/60 font-mono text-xs">Resources Scanned</div>
                </div>
                <div>
                  <div className="text-2xl font-mono font-bold text-cyber-orange">
                    {scanProgress.estimated_completion}
                  </div>
                  <div className="text-cyber-cyan/60 font-mono text-xs">Est. Remaining</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Summary Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
      >
        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <Cloud className="w-8 h-8 text-cyber-cyan mx-auto mb-3" />
            <div className="text-2xl font-mono font-bold text-cyber-cyan">
              {mockResources.length}
            </div>
            <p className="text-cyber-cyan/70 font-mono text-sm">Total Resources</p>
          </CardContent>
        </Card>

        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <DollarSign className="w-8 h-8 text-cyber-green mx-auto mb-3" />
            <div className="text-2xl font-mono font-bold text-cyber-green">
              ${totalMonthlyCost.toLocaleString()}
            </div>
            <p className="text-cyber-green/70 font-mono text-sm">Monthly Cost</p>
          </CardContent>
        </Card>

        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <TrendingUp className="w-8 h-8 text-cyber-orange mx-auto mb-3" />
            <div className="text-2xl font-mono font-bold text-cyber-orange">
              {highOptimizationCount}
            </div>
            <p className="text-cyber-orange/70 font-mono text-sm">High Priority</p>
          </CardContent>
        </Card>

        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <CheckCircle2 className="w-8 h-8 text-cyber-purple mx-auto mb-3" />
            <div className="text-2xl font-mono font-bold text-cyber-purple">
              {Math.round((scanProgress.scanned_resources / scanProgress.total_resources) * 100)}%
            </div>
            <p className="text-cyber-purple/70 font-mono text-sm">Analyzed</p>
          </CardContent>
        </Card>
      </motion.div>

      {/* Filters and Search */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="mb-6"
      >
        <Card className="card-cyber">
          <CardContent className="p-4">
            <div className="flex flex-col md:flex-row gap-4 items-center">
              <div className="flex items-center gap-2">
                <Search className="w-4 h-4 text-cyber-cyan" />
                <Input
                  placeholder="Search resources..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="input-cyber w-64"
                />
              </div>
              
              <div className="flex items-center gap-2">
                <Filter className="w-4 h-4 text-cyber-cyan" />
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="input-cyber"
                >
                  <option value="all">All Types</option>
                  <option value="ec2">EC2 Instances</option>
                  <option value="rds">RDS Databases</option>
                  <option value="s3">S3 Storage</option>
                  <option value="load balancer">Load Balancers</option>
                  <option value="cache">Cache Clusters</option>
                </select>
              </div>

              <div className="flex items-center gap-2 ml-auto">
                <Button className="btn-cyber-secondary" size="sm">
                  <Download className="w-4 h-4 mr-2" />
                  Export
                </Button>
                <Button className="btn-cyber-primary" size="sm">
                  <Settings className="w-4 h-4 mr-2" />
                  Configure Scan
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Resources Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6"
      >
        {filteredResources.map((resource, index) => {
          const ResourceIcon = getResourceIcon(resource.type);
          return (
            <motion.div
              key={resource.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
              whileHover={{ scale: 1.02 }}
              className="cursor-pointer"
              onClick={() => setSelectedResource(resource)}
            >
              <Card className="card-cyber-glow h-full">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <ResourceIcon className="w-6 h-6 text-cyber-cyan" />
                      <div>
                        <h3 className="font-mono font-semibold text-cyber-cyan text-sm">
                          {resource.name}
                        </h3>
                        <p className="font-mono text-cyber-cyan/60 text-xs">
                          {resource.type}
                        </p>
                      </div>
                    </div>
                    <Badge className={`badge-cyber-${getStatusColor(resource.status)}`}>
                      {resource.status}
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-cyber-cyan/70 text-sm">Monthly Cost</span>
                    <span className="font-mono font-bold text-cyber-green">
                      ${resource.cost_monthly.toFixed(2)}
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="font-mono text-cyber-cyan/70 text-sm">Optimization</span>
                    <Badge className={`badge-cyber-${getOptimizationColor(resource.optimization_potential)}`}>
                      {resource.optimization_potential} priority
                    </Badge>
                  </div>

                  <Separator className="bg-cyber-cyan/20" />

                  <div className="space-y-2">
                    <h4 className="font-mono font-semibold text-cyber-cyan text-xs">
                      Recommendations ({resource.recommendations.length})
                    </h4>
                    {resource.recommendations.slice(0, 2).map((rec, idx) => (
                      <div key={idx} className="flex items-center gap-2">
                        <div className="w-1 h-1 bg-cyber-cyan rounded-full" />
                        <span className="font-mono text-cyber-cyan/70 text-xs">{rec}</span>
                      </div>
                    ))}
                  </div>

                  <div className="flex items-center justify-between pt-2">
                    <span className="font-mono text-cyber-cyan/50 text-xs">
                      {resource.region}
                    </span>
                    <Button className="btn-cyber-primary" size="sm">
                      <Eye className="w-3 h-3 mr-1" />
                      Details
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </motion.div>

      {/* Resource Detail Modal */}
      <AnimatePresence>
        {selectedResource && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-cyber-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4"
            onClick={() => setSelectedResource(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="card-cyber-glow max-w-2xl w-full max-h-[90vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {React.createElement(getResourceIcon(selectedResource.type), { 
                      className: "w-6 h-6 text-cyber-cyan" 
                    })}
                    {selectedResource.name}
                  </div>
                  <Button 
                    onClick={() => setSelectedResource(null)}
                    className="btn-cyber-secondary"
                    size="sm"
                  >
                    ✕
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-mono font-semibold text-cyber-cyan text-sm mb-2">
                      Resource Details
                    </h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-cyber-cyan/70">Type:</span>
                        <span className="text-cyber-cyan">{selectedResource.type}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-cyber-cyan/70">Region:</span>
                        <span className="text-cyber-cyan">{selectedResource.region}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-cyber-cyan/70">Status:</span>
                        <Badge className={`badge-cyber-${getStatusColor(selectedResource.status)}`}>
                          {selectedResource.status}
                        </Badge>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-mono font-semibold text-cyber-cyan text-sm mb-2">
                      Cost Analysis
                    </h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-cyber-cyan/70">Monthly Cost:</span>
                        <span className="text-cyber-green font-bold">
                          ${selectedResource.cost_monthly.toFixed(2)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-cyber-cyan/70">Optimization:</span>
                        <Badge className={`badge-cyber-${getOptimizationColor(selectedResource.optimization_potential)}`}>
                          {selectedResource.optimization_potential}
                        </Badge>
                      </div>
                    </div>
                  </div>
                </div>

                <Separator className="bg-cyber-cyan/20" />

                <div>
                  <h4 className="font-mono font-semibold text-cyber-cyan text-sm mb-4">
                    Optimization Recommendations
                  </h4>
                  <div className="space-y-3">
                    {selectedResource.recommendations.map((rec: string, idx: number) => (
                      <div key={idx} className="card-cyber p-3">
                        <div className="flex items-start gap-3">
                          <CheckCircle2 className="w-4 h-4 text-cyber-green mt-0.5" />
                          <span className="font-mono text-cyber-cyan text-sm">{rec}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex gap-3">
                  <Button className="btn-cyber-primary flex-1">
                    Apply Recommendations
                  </Button>
                  <Button className="btn-cyber-secondary">
                    Schedule Implementation
                  </Button>
                </div>
              </CardContent>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
