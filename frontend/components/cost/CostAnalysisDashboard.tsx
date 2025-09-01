'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  DollarSign, 
  TrendingUp, 
  TrendingDown,
  BarChart3, 
  PieChart,
  Calendar,
  Filter,
  Download,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Target,
  Zap,
  Cloud,
  Database,
  Server
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import CountUp from 'react-countup';

// Mock data for cost analysis
const costData = {
  current_month: 12450,
  last_month: 11200,
  projected_next_month: 8950,
  ytd_total: 142300,
  savings_identified: 3500,
  savings_implemented: 2100,
  optimization_opportunities: 15
};

const serviceBreakdown = [
  { name: 'EC2 Instances', cost: 4200, percentage: 33.7, trend: 'up', change: 12 },
  { name: 'RDS Databases', cost: 2800, percentage: 22.5, trend: 'down', change: -8 },
  { name: 'S3 Storage', cost: 1850, percentage: 14.9, trend: 'stable', change: 2 },
  { name: 'Load Balancers', cost: 1200, percentage: 9.6, trend: 'up', change: 15 },
  { name: 'CloudFront CDN', cost: 980, percentage: 7.9, trend: 'down', change: -5 },
  { name: 'ElastiCache', cost: 720, percentage: 5.8, trend: 'stable', change: 1 },
  { name: 'Other Services', cost: 700, percentage: 5.6, trend: 'up', change: 8 }
];

const optimizationOpportunities = [
  {
    id: 1,
    title: 'Rightsize EC2 Instances',
    description: '23 instances are over-provisioned and can be downsized',
    potential_savings: 1200,
    effort: 'low',
    impact: 'high',
    category: 'compute'
  },
  {
    id: 2,
    title: 'Implement S3 Lifecycle Policies',
    description: 'Move infrequently accessed data to cheaper storage classes',
    potential_savings: 850,
    effort: 'medium',
    impact: 'medium',
    category: 'storage'
  },
  {
    id: 3,
    title: 'Reserved Instance Optimization',
    description: 'Purchase RIs for predictable workloads to save 30-60%',
    potential_savings: 2100,
    effort: 'low',
    impact: 'high',
    category: 'pricing'
  },
  {
    id: 4,
    title: 'Unused EBS Volumes',
    description: '12 unattached EBS volumes consuming unnecessary costs',
    potential_savings: 340,
    effort: 'low',
    impact: 'low',
    category: 'storage'
  },
  {
    id: 5,
    title: 'Database Connection Pooling',
    description: 'Optimize RDS connections to reduce instance requirements',
    potential_savings: 680,
    effort: 'high',
    impact: 'medium',
    category: 'database'
  }
];

const monthlyTrend = [
  { month: 'Jan', cost: 9800, savings: 0 },
  { month: 'Feb', cost: 10200, savings: 200 },
  { month: 'Mar', cost: 11500, savings: 450 },
  { month: 'Apr', cost: 12100, savings: 680 },
  { month: 'May', cost: 11800, savings: 920 },
  { month: 'Jun', cost: 11200, savings: 1200 },
  { month: 'Jul', cost: 12450, savings: 1500 }
];

export default function CostAnalysisDashboard() {
  const [selectedTimeframe, setSelectedTimeframe] = useState('month');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const getEffortColor = (effort: string) => {
    switch (effort) {
      case 'low': return 'cyber-green';
      case 'medium': return 'cyber-orange';
      case 'high': return 'cyber-pink';
      default: return 'cyber-cyan';
    }
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'cyber-green';
      case 'medium': return 'cyber-orange';
      case 'low': return 'cyber-cyan';
      default: return 'cyber-cyan';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'compute': return Server;
      case 'storage': return Database;
      case 'database': return Database;
      case 'pricing': return DollarSign;
      default: return Cloud;
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return TrendingUp;
      case 'down': return TrendingDown;
      default: return Target;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up': return 'cyber-pink';
      case 'down': return 'cyber-green';
      default: return 'cyber-cyan';
    }
  };

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
            <BarChart3 className="inline-block w-10 h-10 mr-4" />
            Cost Analysis Dashboard
          </h1>
          <p className="text-cyber-cyan/70 font-mono text-lg">
            Comprehensive analysis and optimization of your cloud infrastructure costs
          </p>
        </div>

        {/* Controls */}
        <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-cyber-cyan" />
              <select
                value={selectedTimeframe}
                onChange={(e) => setSelectedTimeframe(e.target.value)}
                className="input-cyber"
              >
                <option value="week">This Week</option>
                <option value="month">This Month</option>
                <option value="quarter">This Quarter</option>
                <option value="year">This Year</option>
              </select>
            </div>
            
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-cyber-cyan" />
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="input-cyber"
              >
                <option value="all">All Services</option>
                <option value="compute">Compute</option>
                <option value="storage">Storage</option>
                <option value="database">Database</option>
                <option value="networking">Networking</option>
              </select>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Button className="btn-cyber-secondary" size="sm">
              <Download className="w-4 h-4 mr-2" />
              Export Report
            </Button>
          </div>
        </div>
      </motion.div>

      {/* Key Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
      >
        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <DollarSign className="w-8 h-8 text-cyber-cyan mx-auto mb-3" />
            <div className="cost-display-cyber text-2xl mb-2">
              <CountUp
                end={costData.current_month}
                duration={2}
                prefix="$"
                separator=","
              />
            </div>
            <p className="text-cyber-cyan/70 font-mono text-sm mb-2">Current Month</p>
            <div className="flex items-center justify-center gap-1">
              <TrendingUp className="w-3 h-3 text-cyber-pink" />
              <span className="text-cyber-pink font-mono text-xs">
                +{((costData.current_month - costData.last_month) / costData.last_month * 100).toFixed(1)}%
              </span>
            </div>
          </CardContent>
        </Card>

        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <TrendingDown className="w-8 h-8 text-cyber-green mx-auto mb-3" />
            <div className="savings-display-cyber text-2xl mb-2">
              <CountUp
                end={costData.projected_next_month}
                duration={2}
                prefix="$"
                separator=","
              />
            </div>
            <p className="text-cyber-green/70 font-mono text-sm mb-2">Projected Next Month</p>
            <div className="flex items-center justify-center gap-1">
              <TrendingDown className="w-3 h-3 text-cyber-green" />
              <span className="text-cyber-green font-mono text-xs">
                -{((costData.current_month - costData.projected_next_month) / costData.current_month * 100).toFixed(1)}%
              </span>
            </div>
          </CardContent>
        </Card>

        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <Target className="w-8 h-8 text-cyber-purple mx-auto mb-3" />
            <div className="roi-display-cyber text-2xl mb-2">
              <CountUp
                end={costData.savings_identified}
                duration={2}
                prefix="$"
                separator=","
              />
            </div>
            <p className="text-cyber-purple/70 font-mono text-sm mb-2">Savings Identified</p>
            <div className="text-cyber-purple/60 font-mono text-xs">
              ${costData.savings_implemented.toLocaleString()} implemented
            </div>
          </CardContent>
        </Card>

        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <Zap className="w-8 h-8 text-cyber-orange mx-auto mb-3" />
            <div className="text-cyber-orange font-mono font-bold text-2xl mb-2">
              <CountUp
                end={costData.optimization_opportunities}
                duration={1.5}
              />
            </div>
            <p className="text-cyber-orange/70 font-mono text-sm">Opportunities</p>
          </CardContent>
        </Card>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Service Breakdown */}
        <div className="lg:col-span-2 space-y-6">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono flex items-center gap-2">
                  <PieChart className="w-5 h-5" />
                  Service Cost Breakdown
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {serviceBreakdown.map((service, index) => {
                  const TrendIcon = getTrendIcon(service.trend);
                  return (
                    <motion.div
                      key={service.name}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.1 * index }}
                      className="card-cyber p-4"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <div>
                          <h4 className="font-mono font-semibold text-cyber-cyan text-sm">
                            {service.name}
                          </h4>
                          <p className="font-mono text-cyber-cyan/60 text-xs">
                            {service.percentage}% of total spend
                          </p>
                        </div>
                        <div className="text-right">
                          <div className="font-mono font-bold text-cyber-green text-lg">
                            {formatCurrency(service.cost)}
                          </div>
                          <div className="flex items-center gap-1">
                            <TrendIcon className={`w-3 h-3 text-${getTrendColor(service.trend)}`} />
                            <span className={`font-mono text-xs text-${getTrendColor(service.trend)}`}>
                              {service.change > 0 ? '+' : ''}{service.change}%
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="w-full bg-cyber-darker rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-cyber-cyan to-cyber-green h-2 rounded-full"
                          style={{ width: `${service.percentage}%` }}
                        />
                      </div>
                    </motion.div>
                  );
                })}
              </CardContent>
            </Card>
          </motion.div>

          {/* Optimization Opportunities */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono flex items-center gap-2">
                  <Target className="w-5 h-5" />
                  Optimization Opportunities
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {optimizationOpportunities.slice(0, 5).map((opportunity, index) => {
                  const CategoryIcon = getCategoryIcon(opportunity.category);
                  return (
                    <motion.div
                      key={opportunity.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.1 * index }}
                      className="card-cyber p-4"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-start gap-3">
                          <CategoryIcon className="w-5 h-5 text-cyber-cyan mt-0.5" />
                          <div>
                            <h4 className="font-mono font-semibold text-cyber-cyan text-sm mb-1">
                              {opportunity.title}
                            </h4>
                            <p className="font-mono text-cyber-cyan/70 text-xs leading-relaxed">
                              {opportunity.description}
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="font-mono font-bold text-cyber-green text-sm">
                            {formatCurrency(opportunity.potential_savings)}/mo
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Badge className={`badge-cyber-${getEffortColor(opportunity.effort)} text-xs`}>
                            {opportunity.effort} effort
                          </Badge>
                          <Badge className={`badge-cyber-${getImpactColor(opportunity.impact)} text-xs`}>
                            {opportunity.impact} impact
                          </Badge>
                        </div>
                        <Button className="btn-cyber-primary" size="sm">
                          Implement
                        </Button>
                      </div>
                    </motion.div>
                  );
                })}
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Monthly Trend */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono text-sm">Monthly Trend</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {monthlyTrend.slice(-6).map((month, index) => (
                    <div key={month.month} className="flex items-center justify-between">
                      <span className="font-mono text-cyber-cyan/70 text-xs">
                        {month.month}
                      </span>
                      <div className="text-right">
                        <div className="font-mono text-cyber-cyan text-sm">
                          {formatCurrency(month.cost)}
                        </div>
                        {month.savings > 0 && (
                          <div className="font-mono text-cyber-green text-xs">
                            -{formatCurrency(month.savings)}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.7 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono text-sm">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button className="btn-cyber-primary w-full justify-start" size="sm">
                  <Zap className="w-4 h-4 mr-2" />
                  Run Cost Optimization
                </Button>
                <Button className="btn-cyber-secondary w-full justify-start" size="sm">
                  <AlertTriangle className="w-4 h-4 mr-2" />
                  Set Budget Alerts
                </Button>
                <Button className="btn-cyber-secondary w-full justify-start" size="sm">
                  <Clock className="w-4 h-4 mr-2" />
                  Schedule Analysis
                </Button>
              </CardContent>
            </Card>
          </motion.div>

          {/* Cost Alerts */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.9 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono text-sm">Cost Alerts</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-cyber-orange mt-0.5" />
                  <div>
                    <p className="font-mono text-cyber-orange text-xs font-semibold">
                      Budget Alert
                    </p>
                    <p className="font-mono text-cyber-cyan/70 text-xs">
                      85% of monthly budget used
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-cyber-green mt-0.5" />
                  <div>
                    <p className="font-mono text-cyber-green text-xs font-semibold">
                      Optimization Applied
                    </p>
                    <p className="font-mono text-cyber-cyan/70 text-xs">
                      EC2 rightsizing saved $1,200
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
