'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { DashboardSkeleton } from '@/components/ui/LoadingSkeleton';
import { getColorClass, getIconColorClass } from '@/lib/utils/colors';
import { 
  Calculator, 
  TrendingUp, 
  Zap, 
  Shield, 
  DollarSign,
  ArrowRight,
  Sparkles,
  Target,
  Clock,
  Users,
  Activity,
  CheckCircle,
  AlertTriangle,
  Wifi
} from 'lucide-react';

interface DashboardData {
  stats: Array<{
    label: string;
    value: string;
    change: string;
    icon: any;
    color: string;
    trend: 'up' | 'down' | 'stable';
  }>;
  systemStatus: Array<{
    service: string;
    status: 'online' | 'offline' | 'warning';
    metrics: string;
    uptime: string;
  }>;
  recentActivity: Array<{
    action: string;
    time: string;
    status: 'success' | 'warning' | 'error';
  }>;
}

export default function EnhancedDashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Simulate data loading
  useEffect(() => {
    const loadData = async () => {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        setData({
          stats: [
            {
              label: 'Active Engagements',
              value: '12',
              change: '+3 this month',
              icon: Users,
              color: 'cyber-cyan',
              trend: 'up'
            },
            {
              label: 'Total Savings Delivered',
              value: '$2.4M',
              change: '+15% this quarter',
              icon: TrendingUp,
              color: 'cyber-green',
              trend: 'up'
            },
            {
              label: 'Average ROI',
              value: '340%',
              change: 'Across all clients',
              icon: Target,
              color: 'cyber-purple',
              trend: 'stable'
            },
            {
              label: 'Avg. Payback Period',
              value: '2.3 months',
              change: 'Industry leading',
              icon: Clock,
              color: 'cyber-orange',
              trend: 'down'
            }
          ],
          systemStatus: [
            {
              service: 'Tokenized Pricing System',
              status: 'online',
              metrics: 'All pricing calculations operational',
              uptime: '99.9%'
            },
            {
              service: 'Infrastructure Scanner',
              status: 'online', 
              metrics: 'Cloud scanning services ready',
              uptime: '99.8%'
            },
            {
              service: 'AI Terminal',
              status: 'online',
              metrics: 'AI-powered assistance available',
              uptime: '99.7%'
            },
            {
              service: 'Cost Analysis Engine',
              status: 'warning',
              metrics: 'Minor performance degradation',
              uptime: '98.2%'
            }
          ],
          recentActivity: [
            { action: 'New client engagement started', time: '2 minutes ago', status: 'success' },
            { action: 'Cost optimization completed', time: '15 minutes ago', status: 'success' },
            { action: 'Security scan initiated', time: '1 hour ago', status: 'warning' },
            { action: 'Infrastructure analysis finished', time: '2 hours ago', status: 'success' },
          ]
        });
      } catch (err) {
        setError('Failed to load dashboard data');
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  const quickActions = [
    {
      title: 'Pricing Calculator',
      description: 'Calculate transparent, tokenized pricing for your consulting engagement',
      icon: Calculator,
      href: '/pricing',
      color: 'cyber-cyan',
      highlight: true
    },
    {
      title: 'Cost Analysis',
      description: 'Analyze and optimize your cloud infrastructure costs',
      icon: DollarSign,
      href: '/cost-analysis',
      color: 'cyber-green'
    },
    {
      title: 'Infrastructure Scan',
      description: 'Scan your cloud infrastructure for optimization opportunities',
      icon: Zap,
      href: '/infrastructure',
      color: 'cyber-purple'
    },
    {
      title: 'Security Assessment',
      description: 'Comprehensive security analysis and recommendations',
      icon: Shield,
      href: '/security',
      color: 'cyber-orange'
    }
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online': return CheckCircle;
      case 'warning': return AlertTriangle;
      case 'offline': return Wifi;
      default: return Activity;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'text-cyber-green';
      case 'warning': return 'text-cyber-orange';
      case 'offline': return 'text-gray-500';
      default: return 'text-cyber-cyan';
    }
  };

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (error) {
    return (
      <div className="min-h-screen bg-cyber-black flex items-center justify-center">
        <Card className="card-cyber-glow max-w-md">
          <CardContent className="p-8 text-center">
            <AlertTriangle className="w-12 h-12 text-cyber-orange mx-auto mb-4" />
            <h2 className="text-xl font-mono text-cyber-cyan mb-2">Error Loading Dashboard</h2>
            <p className="text-cyber-cyan/70 font-mono text-sm">{error}</p>
            <button 
              onClick={() => window.location.reload()}
              className="btn-cyber-primary mt-4"
            >
              Retry
            </button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cyber-black p-6">
      {/* Animated Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="text-center mb-8">
          <h1 className="text-cyber-title mb-4">
            <Sparkles className="inline-block w-10 h-10 mr-4" />
            CloudMind Dashboard
          </h1>
          <p className="text-cyber-cyan/70 font-mono text-lg">
            Enterprise FinOps Consulting Platform
          </p>
          <div className="flex items-center justify-center gap-2 mt-2">
            <div className="status-cyber-online" />
            <span className="text-cyber-green font-mono text-sm">All Systems Operational</span>
          </div>
        </div>
      </motion.div>

      {/* Enhanced Stats Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
      >
        <AnimatePresence>
          {data?.stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * index }}
                whileHover={{ scale: 1.02 }}
                className="group"
              >
                <Card className="card-cyber-glow cursor-pointer">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <Icon className={`w-8 h-8 ${getIconColorClass(stat.color)} group-hover:scale-110 transition-transform`} />
                      <div className="status-cyber-online" />
                    </div>
                    <div className="space-y-2">
                      <p className="font-mono text-sm text-cyber-cyan/70">
                        {stat.label}
                      </p>
                      <p className={`text-3xl font-mono font-bold ${getColorClass(stat.color)}`}>
                        {stat.value}
                      </p>
                      <div className="flex items-center gap-2">
                        <TrendingUp className={`w-4 h-4 ${stat.trend === 'up' ? 'text-cyber-green' : stat.trend === 'down' ? 'text-cyber-orange' : 'text-cyber-cyan'}`} />
                        <p className="font-mono text-xs text-cyber-cyan/50">
                          {stat.change}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="mb-8"
      >
        <h2 className="text-cyber-subtitle mb-6 text-center">
          Quick Actions
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {quickActions.map((action, index) => {
            const Icon = action.icon;
            return (
              <motion.div
                key={action.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * index }}
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
              >
                <Link href={action.href}>
                  <Card className={`card-cyber-glow cursor-pointer transition-all duration-300 hover:shadow-[0_0_30px_rgba(0,245,255,0.3)] ${action.highlight ? 'ring-2 ring-cyber-purple/50' : ''}`}>
                    <CardHeader>
                      <CardTitle className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <Icon className={`w-6 h-6 ${getIconColorClass(action.color)}`} />
                          <span className="font-mono text-cyber-cyan">
                            {action.title}
                            {action.highlight && (
                              <motion.span 
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                className="ml-2 text-xs bg-cyber-purple/20 text-cyber-purple px-2 py-1 rounded-full"
                              >
                                NEW
                              </motion.span>
                            )}
                          </span>
                        </div>
                        <ArrowRight className="w-5 h-5 text-cyber-cyan/50 group-hover:translate-x-1 transition-transform" />
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-cyber-cyan/70 font-mono text-sm">
                        {action.description}
                      </p>
                    </CardContent>
                  </Card>
                </Link>
              </motion.div>
            );
          })}
        </div>
      </motion.div>

      {/* Enhanced System Status */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
      >
        {/* System Status */}
        <Card className="card-cyber-glow">
          <CardHeader>
            <CardTitle className="text-cyber-cyan font-mono flex items-center gap-2">
              <Activity className="w-5 h-5" />
              System Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data?.systemStatus.map((system, index) => {
                const StatusIcon = getStatusIcon(system.status);
                return (
                  <motion.div
                    key={system.service}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 * index }}
                    className="flex items-center justify-between p-4 bg-cyber-darker/50 rounded-lg hover:bg-cyber-darker/70 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <StatusIcon className={`w-5 h-5 ${getStatusColor(system.status)}`} />
                      <div>
                        <p className="font-mono font-semibold text-cyber-cyan text-sm">
                          {system.service}
                        </p>
                        <p className="font-mono text-cyber-cyan/60 text-xs">
                          {system.metrics}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className={`font-mono text-sm ${getStatusColor(system.status)}`}>
                        {system.status.charAt(0).toUpperCase() + system.status.slice(1)}
                      </span>
                      <p className="font-mono text-cyber-cyan/50 text-xs">
                        {system.uptime} uptime
                      </p>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card className="card-cyber-glow">
          <CardHeader>
            <CardTitle className="text-cyber-cyan font-mono flex items-center gap-2">
              <TrendingUp className="w-5 h-5" />
              Recent Activity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data?.recentActivity.map((activity, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 * index }}
                  className="flex items-center gap-3 p-3 bg-cyber-darker/30 rounded-lg"
                >
                  <div className={`w-2 h-2 rounded-full ${
                    activity.status === 'success' ? 'bg-cyber-green' :
                    activity.status === 'warning' ? 'bg-cyber-orange' :
                    'bg-cyber-pink'
                  }`} />
                  <div className="flex-1">
                    <p className="font-mono text-cyber-cyan text-sm">
                      {activity.action}
                    </p>
                    <p className="font-mono text-cyber-cyan/50 text-xs">
                      {activity.time}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
