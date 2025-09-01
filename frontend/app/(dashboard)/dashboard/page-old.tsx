'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
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
  Users
} from 'lucide-react';

export default function DashboardPage() {
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

  const stats = [
    {
      label: 'Active Engagements',
      value: '12',
      change: '+3 this month',
      icon: Users,
      color: 'cyber-cyan'
    },
    {
      label: 'Total Savings Delivered',
      value: '$2.4M',
      change: '+15% this quarter',
      icon: TrendingUp,
      color: 'cyber-green'
    },
    {
      label: 'Average ROI',
      value: '340%',
      change: 'Across all clients',
      icon: Target,
      color: 'cyber-purple'
    },
    {
      label: 'Avg. Payback Period',
      value: '2.3 months',
      change: 'Industry leading',
      icon: Clock,
      color: 'cyber-orange'
    }
  ];

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
            <Sparkles className="inline-block w-10 h-10 mr-4" />
            CloudMind Dashboard
          </h1>
          <p className="text-cyber-cyan/70 font-mono text-lg">
            Cyberpunk FinOps Consulting Platform
          </p>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
      >
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
            >
              <Card className="card-cyber-glow">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <Icon className={`w-8 h-8 ${getIconColorClass(stat.color)}`} />
                    <div className="status-cyber-online" />
                  </div>
                  <div className="space-y-2">
                    <p className="font-mono text-sm text-cyber-cyan/70">
                      {stat.label}
                    </p>
                    <p className={`text-3xl font-mono font-bold ${getColorClass(stat.color)}`}>
                      {stat.value}
                    </p>
                    <p className="font-mono text-xs text-cyber-cyan/50">
                      {stat.change}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
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
                whileHover={{ scale: 1.02 }}
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
                              <span className="ml-2 text-xs bg-cyber-purple/20 text-cyber-purple px-2 py-1 rounded-full">
                                NEW
                              </span>
                            )}
                          </span>
                        </div>
                        <ArrowRight className="w-5 h-5 text-cyber-cyan/50" />
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

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <Card className="card-cyber-glow">
          <CardHeader>
            <CardTitle className="text-cyber-cyan font-mono flex items-center gap-2">
              <TrendingUp className="w-5 h-5" />
              Platform Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-cyber-darker/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="status-cyber-online" />
                  <div>
                    <p className="font-mono font-semibold text-cyber-green text-sm">
                      Tokenized Pricing System
                    </p>
                    <p className="font-mono text-cyber-cyan/60 text-xs">
                      All pricing calculations operational
                    </p>
                  </div>
                </div>
                <span className="font-mono text-cyber-green text-sm">Online</span>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-cyber-darker/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="status-cyber-online" />
                  <div>
                    <p className="font-mono font-semibold text-cyber-cyan text-sm">
                      Infrastructure Scanner
                    </p>
                    <p className="font-mono text-cyber-cyan/60 text-xs">
                      Cloud scanning services ready
                    </p>
                  </div>
                </div>
                <span className="font-mono text-cyber-cyan text-sm">Ready</span>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-cyber-darker/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="status-cyber-online" />
                  <div>
                    <p className="font-mono font-semibold text-cyber-purple text-sm">
                      AI Terminal
                    </p>
                    <p className="font-mono text-cyber-cyan/60 text-xs">
                      AI-powered assistance available
                    </p>
                  </div>
                </div>
                <span className="font-mono text-cyber-purple text-sm">Active</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}