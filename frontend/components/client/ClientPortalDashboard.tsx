'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import CountUp from 'react-countup';
import { 
  TrendingUp, 
  DollarSign, 
  Clock, 
  Target,
  CheckCircle2,
  AlertCircle,
  BarChart3,
  FileText,
  Github,
  Zap,
  Shield,
  Activity,
  Calendar,
  Download,
  ExternalLink,
  Sparkles,
  ArrowUp,
  ArrowDown
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import api, { engagementsApi } from '@/lib/api/client';

// Mock data - in real app this would come from API
const mockEngagement = {
  id: 'eng-001',
  title: 'AWS Infrastructure Optimization',
  client_name: 'TechCorp Inc.',
  status: 'in_progress',
  progress_percentage: 67,
  total_cost: 4250.00,
  projected_monthly_savings: 28500.00,
  actual_monthly_savings: 24200.00,
  roi_percentage: 678.2,
  payback_months: 1.8,
  start_date: '2024-01-15',
  estimated_completion_date: '2024-02-28',
  github_repo_url: 'https://github.com/cloudmind/techcorp-optimization',
  resources_discovered: 247,
  resources_analyzed: 165,
  optimizations_identified: 23,
  items: [
    { name: 'EC2 Instance Analysis', quantity: 89, status: 'completed', savings: 12500 },
    { name: 'RDS Database Analysis', quantity: 12, status: 'completed', savings: 8200 },
    { name: 'S3 Storage Analysis', quantity: 146, status: 'in_progress', savings: 3500 },
    { name: 'Cost Optimization Implementation', quantity: 1, status: 'pending', savings: 0 }
  ]
};

const recentActivity = [
  {
    type: 'optimization',
    title: 'RDS Instance Rightsizing Completed',
    description: 'Optimized 3 RDS instances, reducing costs by $2,400/month',
    timestamp: '2 hours ago',
    savings: 2400,
    icon: TrendingUp,
    color: 'cyber-green'
  },
  {
    type: 'scan',
    title: 'S3 Lifecycle Policies Applied',
    description: 'Implemented intelligent tiering on 47 S3 buckets',
    timestamp: '5 hours ago',
    savings: 1200,
    icon: Zap,
    color: 'cyber-cyan'
  },
  {
    type: 'report',
    title: 'Weekly Progress Report Generated',
    description: 'Comprehensive analysis with recommendations available',
    timestamp: '1 day ago',
    savings: 0,
    icon: FileText,
    color: 'cyber-purple'
  },
  {
    type: 'security',
    title: 'Security Assessment Completed',
    description: 'Identified and resolved 5 security vulnerabilities',
    timestamp: '2 days ago',
    savings: 0,
    icon: Shield,
    color: 'cyber-orange'
  }
];

export default function ClientPortalDashboard({ projectCount }: { projectCount?: number }) {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [engagement, setEngagement] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [documents, setDocuments] = useState<any[]>([]);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    let mounted = true;
    (async () => {
      setLoading(true);
      try {
        const list = await engagementsApi.list();
        if (mounted && Array.isArray(list) && list.length > 0) {
          const selected = list[0];
          setEngagement(selected);
          try {
            const [progressRes, docsRes] = await Promise.all([
              engagementsApi.getProgress(selected.id),
              engagementsApi.getDocuments(selected.id),
            ]);
            if (mounted) {
              setTimeline(Array.isArray(progressRes) ? progressRes : []);
              setDocuments(Array.isArray(docsRes) ? docsRes : []);
            }
          } catch {
            if (mounted) {
              setTimeline([
                { id: 'p1', title: 'Engagement Kickoff', date: '2024-01-15', status: 'completed', notes: 'Scope defined, access granted' },
                { id: 'p2', title: 'Discovery & Scanning', date: '2024-01-20', status: 'completed', notes: 'Initial scan completed' },
                { id: 'p3', title: 'Optimization Planning', date: '2024-01-28', status: 'in_progress', notes: 'Rightsizing plan in progress' },
                { id: 'p4', title: 'Implementation', date: '2024-02-05', status: 'pending', notes: 'Execution window scheduled' },
              ]);
              setDocuments([
                { id: 'd1', name: 'Statement of Work (SOW).pdf', type: 'SOW', date: '2024-01-15', url: '#', size: '214 KB' },
                { id: 'd2', name: 'Weekly Report - Jan 22.pdf', type: 'Report', date: '2024-01-22', url: '#', size: '512 KB' },
                { id: 'd3', name: 'Optimization Plan v1.pdf', type: 'Plan', date: '2024-01-28', url: '#', size: '390 KB' },
              ]);
            }
          }
        }
      } catch (_) {
        // fallback to mock
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => { mounted = false };
  }, []);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'cyber-green';
      case 'in_progress': return 'cyber-cyan';
      case 'pending': return 'cyber-orange';
      default: return 'cyber-cyan';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return CheckCircle2;
      case 'in_progress': return Activity;
      case 'pending': return Clock;
      default: return AlertCircle;
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
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-6">
          <div>
            <h1 className="text-cyber-title mb-2">
              <Sparkles className="inline-block w-8 h-8 mr-3" />
              {(engagement?.title) || mockEngagement.title}
            </h1>
            <p className="text-cyber-cyan/70 font-mono">
              {(engagement?.client_name || mockEngagement.client_name)} • Started {(engagement?.start_date ? new Date(engagement.start_date).toLocaleDateString() : new Date(mockEngagement.start_date).toLocaleDateString())}
            </p>
          </div>
          
          <div className="flex items-center gap-4 mt-4 lg:mt-0">
            <Badge className={`badge-cyber-${getStatusColor(engagement?.status || mockEngagement.status)}`}>
              {(engagement?.status || mockEngagement.status).replace('_', ' ').toUpperCase()}
            </Badge>
            <div className="text-cyber-cyan/60 font-mono text-sm">
              Last updated: {currentTime.toLocaleTimeString()}
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <Card className="card-cyber-glow">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-mono font-semibold text-cyber-cyan">Overall Progress</h3>
              <span className="text-2xl font-mono font-bold text-cyber-green">
                {(engagement?.progress_percentage ?? mockEngagement.progress_percentage)}%
              </span>
            </div>
            <Progress 
              value={(engagement?.progress_percentage ?? mockEngagement.progress_percentage)} 
              className="progress-cyber h-3 mb-4"
            />
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-cyber-cyan font-mono font-bold text-lg">
                  {(engagement?.resources_analyzed ?? mockEngagement.resources_analyzed)}
                </div>
                <div className="text-cyber-cyan/60 font-mono text-xs">Resources Analyzed</div>
              </div>
              <div>
                <div className="text-cyber-purple font-mono font-bold text-lg">
                  {(engagement?.optimizations_identified ?? mockEngagement.optimizations_identified)}
                </div>
                <div className="text-cyber-cyan/60 font-mono text-xs">Optimizations Found</div>
              </div>
              <div>
                <div className="text-cyber-orange font-mono font-bold text-lg">
                  {(engagement?.estimated_completion_date ? Math.ceil((new Date(engagement.estimated_completion_date).getTime() - Date.now()) / (1000 * 60 * 60 * 24)) : Math.ceil((new Date(mockEngagement.estimated_completion_date).getTime() - Date.now()) / (1000 * 60 * 60 * 24)))}
                </div>
                <div className="text-cyber-cyan/60 font-mono text-xs">Days Remaining</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Key Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
      >
        {/* Total Investment */}
        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <DollarSign className="w-8 h-8 text-cyber-cyan mx-auto mb-3" />
            <div className="cost-display-cyber text-2xl mb-2">
              <CountUp
                end={(engagement?.total_cost ?? mockEngagement.total_cost)}
                duration={2}
                prefix="$"
                separator=","
              />
            </div>
            <p className="text-cyber-cyan/70 font-mono text-sm">Total Investment</p>
          </CardContent>
        </Card>

        {/* Monthly Savings */}
        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <TrendingUp className="w-8 h-8 text-cyber-green mx-auto mb-3" />
            <div className="savings-display-cyber text-2xl mb-2">
              <CountUp
                end={(engagement?.actual_monthly_savings ?? mockEngagement.actual_monthly_savings || 0)}
                duration={2}
                prefix="$"
                suffix="/mo"
                separator=","
              />
            </div>
            <p className="text-cyber-green/70 font-mono text-sm">Monthly Savings</p>
            {(engagement?.actual_monthly_savings ?? mockEngagement.actual_monthly_savings) && (engagement?.projected_monthly_savings ?? mockEngagement.projected_monthly_savings) && (
              <div className="flex items-center justify-center gap-1 mt-2">
                <ArrowUp className="w-3 h-3 text-cyber-green" />
                <span className="text-cyber-green font-mono text-xs">
                  {((((engagement?.actual_monthly_savings ?? mockEngagement.actual_monthly_savings) / (engagement?.projected_monthly_savings ?? mockEngagement.projected_monthly_savings)) * 100) as number).toFixed(0)}% of target
                </span>
              </div>
            )}
          </CardContent>
        </Card>

        {/* ROI */}
        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <Target className="w-8 h-8 text-cyber-purple mx-auto mb-3" />
            <div className="roi-display-cyber text-2xl mb-2">
              <CountUp
                end={(engagement?.roi_percentage ?? mockEngagement.roi_percentage)}
                duration={2.5}
                suffix="%"
                decimals={0}
              />
            </div>
            <p className="text-cyber-purple/70 font-mono text-sm">Annual ROI</p>
          </CardContent>
        </Card>

        {/* Payback Period */}
        <Card className="card-cyber-glow">
          <CardContent className="p-6 text-center">
            <Clock className="w-8 h-8 text-cyber-orange mx-auto mb-3" />
            <div className="text-cyber-orange font-mono font-bold text-2xl mb-2">
              <CountUp
                end={(engagement?.payback_months ?? mockEngagement.payback_months)}
                duration={1.8}
                decimals={1}
                suffix=" mo"
              />
            </div>
            <p className="text-cyber-orange/70 font-mono text-sm">Payback Period</p>
          </CardContent>
        </Card>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Service Progress */}
        <div className="lg:col-span-2 space-y-6">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  Service Progress
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {(engagement?.items ?? mockEngagement.items).map((item: any, index: number) => {
                  const StatusIcon = getStatusIcon(item.status);
                  return (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.1 * index }}
                      className="card-cyber p-4"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <StatusIcon className={`w-5 h-5 text-${getStatusColor(item.status)}`} />
                          <div>
                            <h4 className="font-mono font-semibold text-cyber-cyan text-sm">
                              {item.name}
                            </h4>
                            <p className="font-mono text-cyber-cyan/60 text-xs">
                              {item.quantity} resources
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <Badge className={`badge-cyber-${getStatusColor(item.status)} mb-1`}>
                            {item.status.replace('_', ' ')}
                          </Badge>
                          {item.savings > 0 && (
                            <div className="text-cyber-green font-mono text-sm">
                              +{formatCurrency(item.savings)}/mo
                            </div>
                          )}
                        </div>
                      </div>
                    </motion.div>
                  );
                })}
              </CardContent>
            </Card>
          </motion.div>

          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono flex items-center gap-2">
                  <Activity className="w-5 h-5" />
                  Recent Activity
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {recentActivity.map((activity, index) => {
                  const Icon = activity.icon;
                  return (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.1 * index }}
                      className="flex items-start gap-4 p-3 bg-cyber-darker/30 rounded-lg"
                    >
                      <Icon className={`w-5 h-5 text-${activity.color} mt-1`} />
                      <div className="flex-1">
                        <h4 className="font-mono font-semibold text-cyber-cyan text-sm mb-1">
                          {activity.title}
                        </h4>
                        <p className="text-cyber-cyan/70 font-mono text-xs mb-2">
                          {activity.description}
                        </p>
                        <div className="flex items-center justify-between">
                          <span className="text-cyber-cyan/50 font-mono text-xs">
                            {activity.timestamp}
                          </span>
                          {activity.savings > 0 && (
                            <span className="text-cyber-green font-mono text-xs">
                              +{formatCurrency(activity.savings)}/mo saved
                            </span>
                          )}
                        </div>
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
          {/* Progress Timeline */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.45 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono text-sm">Engagement Timeline</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="relative pl-4">
                  <div className="absolute left-1 top-0 bottom-0 w-0.5 bg-cyber-cyan/20" />
                  <div className="space-y-4">
                    {(timeline.length ? timeline : []).map((ev: any) => (
                      <div key={ev.id} className="relative">
                        <div className={`absolute -left-2.5 top-1 w-2 h-2 rounded-full ${ev.status === 'completed' ? 'bg-cyber-green' : ev.status === 'in_progress' ? 'bg-cyber-cyan' : 'bg-cyber-orange'}`} />
                        <div className="ml-2">
                          <div className="flex items-center justify-between">
                            <h4 className="font-mono font-semibold text-cyber-cyan text-xs">{ev.title}</h4>
                            <span className="text-cyber-cyan/50 font-mono text-[10px]">{ev.date}</span>
                          </div>
                          {ev.notes && (
                            <p className="text-cyber-cyan/60 font-mono text-[11px] mt-1">{ev.notes}</p>
                          )}
                        </div>
                      </div>
                    ))}
                    {!timeline.length && (
                      <p className="text-cyber-cyan/60 font-mono text-xs">No progress events yet.</p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Documents */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.55 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono text-sm">Documents</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {(documents.length ? documents : []).map((doc: any) => (
                  <div key={doc.id} className="flex items-center justify-between p-2 bg-cyber-darker/30 rounded-lg">
                    <div className="flex items-center gap-3">
                      <FileText className="w-4 h-4 text-cyber-cyan" />
                      <div>
                        <p className="font-mono text-cyber-cyan text-xs">{doc.name}</p>
                        <p className="font-mono text-cyber-cyan/60 text-[10px]">{doc.type} • {doc.date}{doc.size ? ` • ${doc.size}` : ''}</p>
                      </div>
                    </div>
                    <a
                      className="btn-cyber-secondary text-xs px-2 py-1 rounded-md flex items-center gap-1"
                      href={doc.url || '#'}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <Download className="w-3 h-3" /> Download
                    </a>
                  </div>
                ))}
                {!documents.length && (
                  <p className="text-cyber-cyan/60 font-mono text-xs">No documents yet.</p>
                )}
              </CardContent>
            </Card>
          </motion.div>
          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono text-sm">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button className="btn-cyber-primary w-full justify-start" size="sm">
                  <FileText className="w-4 h-4 mr-2" />
                  Download Report
                </Button>
                <Button className="btn-cyber-secondary w-full justify-start" size="sm">
                  <Github className="w-4 h-4 mr-2" />
                  View Repository
                  <ExternalLink className="w-3 h-3 ml-auto" />
                </Button>
                <Button className="btn-cyber-secondary w-full justify-start" size="sm">
                  <Calendar className="w-4 h-4 mr-2" />
                  Schedule Meeting
                </Button>
              </CardContent>
            </Card>
          </motion.div>

          {/* Next Milestones */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.7 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono text-sm">Upcoming Milestones</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-cyber-cyan rounded-full" />
                    <span className="font-mono text-cyber-cyan text-xs">
                      S3 optimization completion
                    </span>
                  </div>
                  <div className="text-cyber-cyan/60 font-mono text-xs ml-4">
                    Expected: 3 days
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-cyber-purple rounded-full" />
                    <span className="font-mono text-cyber-purple text-xs">
                      Implementation phase start
                    </span>
                  </div>
                  <div className="text-cyber-cyan/60 font-mono text-xs ml-4">
                    Expected: 1 week
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-cyber-green rounded-full" />
                    <span className="font-mono text-cyber-green text-xs">
                      Final report delivery
                    </span>
                  </div>
                  <div className="text-cyber-cyan/60 font-mono text-xs ml-4">
                    Expected: 2 weeks
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Contact */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.9 }}
          >
            <Card className="card-cyber-glow">
              <CardHeader>
                <CardTitle className="text-cyber-cyan font-mono text-sm">Your Consultant</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className="w-12 h-12 bg-gradient-to-br from-cyber-cyan to-cyber-purple rounded-full mx-auto mb-3 flex items-center justify-center">
                    <span className="font-mono font-bold text-cyber-black">CM</span>
                  </div>
                  <h4 className="font-mono font-semibold text-cyber-cyan text-sm mb-1">
                    CloudMind Expert
                  </h4>
                  <p className="text-cyber-cyan/60 font-mono text-xs mb-3">
                    Senior Cloud Architect
                  </p>
                  <Button className="btn-cyber-primary w-full" size="sm">
                    Contact Consultant
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
