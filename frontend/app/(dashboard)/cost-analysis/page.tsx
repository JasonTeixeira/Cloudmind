'use client'

import { useState, useEffect } from 'react'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  AlertTriangle, 
  CheckCircle,
  BarChart3,
  PieChart,
  Calendar,
  Download,
  RefreshCw,
  Filter
} from 'lucide-react'
import { useUnitEconomics, useCostEvents, useRightsizingRecommendations, useTagHygieneAudit, useCommitmentPlan } from '@/lib/hooks/useApi'

export default function CostAnalysisPage() {
  const unitEconomics = useUnitEconomics()
  const events = useCostEvents(1, 25)
  const rightsizing = useRightsizingRecommendations()
  const tagHygiene = useTagHygieneAudit()
  const commitments = useCommitmentPlan()

  const isLoading = unitEconomics.isLoading || events.isLoading || rightsizing.isLoading || tagHygiene.isLoading || commitments.isLoading
  const costData = {
    totalCost: unitEconomics.data?.total_cost ?? 0,
    monthlyChange: unitEconomics.data?.month_over_month_change ?? 0,
    topServices: (unitEconomics.data?.by_service || []).slice(0, 4).map((s: any) => ({ name: s.service || s.name, cost: s.cost ?? 0, change: s.change ?? 0 }))
  }

  if (isLoading) {
    return (
      <div className="space-y-6 page-transition">
        <div className="text-center space-y-4">
          <div className="skeleton h-10 w-96 mx-auto" />
          <div className="skeleton h-6 w-64 mx-auto" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {Array.from({ length: 4 }).map((_, index) => (
            <div key={index} className="card-cyber p-6">
              <div className="skeleton h-6 w-32 mb-4" />
              <div className="skeleton h-8 w-24 mb-2" />
              <div className="skeleton h-4 w-20" />
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 page-transition" data-testid="cost-analysis-page">
      {/* Header */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold font-mono text-cyber-cyan">
          Cost Analysis Dashboard
        </h1>
        <p className="text-cyber-cyan/70 font-mono">
          Comprehensive cost breakdown and optimization insights
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card-cyber-glow p-6">
          <div className="flex items-center justify-between mb-4">
            <DollarSign className="w-8 h-8 text-cyber-green" />
            <div className="flex items-center text-cyber-green text-sm">
              <TrendingUp className="w-4 h-4 mr-1" />
              +{costData.monthlyChange}%
            </div>
          </div>
          <div className="space-y-2">
            <h3 className="font-mono text-cyber-cyan/70 text-sm">Total Monthly Cost</h3>
            <p className="text-3xl font-bold font-mono text-cyber-green">
              ${costData.totalCost.toLocaleString()}
            </p>
          </div>
        </div>

        <div className="card-cyber-glow p-6">
          <div className="flex items-center justify-between mb-4">
            <BarChart3 className="w-8 h-8 text-cyber-purple" />
            <CheckCircle className="w-5 h-5 text-cyber-green" />
          </div>
          <div className="space-y-2">
            <h3 className="font-mono text-cyber-cyan/70 text-sm">Optimization Score</h3>
            <p className="text-3xl font-bold font-mono text-cyber-purple">87%</p>
          </div>
        </div>

        <div className="card-cyber-glow p-6">
          <div className="flex items-center justify-between mb-4">
            <PieChart className="w-8 h-8 text-cyber-orange" />
            <div className="flex items-center text-cyber-green text-sm">
              <TrendingDown className="w-4 h-4 mr-1" />
              -8.2%
            </div>
          </div>
          <div className="space-y-2">
            <h3 className="font-mono text-cyber-cyan/70 text-sm">Potential Savings</h3>
            <p className="text-3xl font-bold font-mono text-cyber-orange">
              $2,340
            </p>
          </div>
        </div>

        <div className="card-cyber-glow p-6">
          <div className="flex items-center justify-between mb-4">
            <AlertTriangle className="w-8 h-8 text-cyber-pink" />
            <div className="cyber-badge bg-cyber-pink/20 text-cyber-pink">
              3 Issues
            </div>
          </div>
          <div className="space-y-2">
            <h3 className="font-mono text-cyber-cyan/70 text-sm">Cost Anomalies</h3>
            <p className="text-3xl font-bold font-mono text-cyber-pink">3</p>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8" data-testid="charts-container">
        <div className="card-cyber-glow p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="font-mono font-semibold text-cyber-cyan text-lg">
              Cost Breakdown by Service
            </h3>
            <div className="flex gap-2">
              <button className="btn-cyber-secondary">
                <Filter className="w-4 h-4" />
              </button>
              <button className="btn-cyber-secondary">
                <Download className="w-4 h-4" />
              </button>
            </div>
          </div>
          
          <div className="space-y-4" data-testid="bar-chart">
            {costData.topServices.map((service, index) => (
              <div key={service.name} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-cyber-cyan text-sm">{service.name}</span>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-cyber-green font-bold">
                      ${service.cost.toLocaleString()}
                    </span>
                    <div className={`flex items-center text-xs ${
                      service.change > 0 ? 'text-cyber-pink' : 'text-cyber-green'
                    }`}>
                      {service.change > 0 ? (
                        <TrendingUp className="w-3 h-3 mr-1" />
                      ) : (
                        <TrendingDown className="w-3 h-3 mr-1" />
                      )}
                      {Math.abs(service.change)}%
                    </div>
                  </div>
                </div>
                <div className="w-full bg-cyber-darker rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-cyber-cyan to-cyber-purple h-2 rounded-full transition-all duration-500"
                    style={{ width: `${(service.cost / costData.topServices[0].cost) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card-cyber-glow p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="font-mono font-semibold text-cyber-cyan text-lg">
              Cost Trends (30 Days)
            </h3>
            <div className="flex gap-2">
              <button className="btn-cyber-secondary">
                <Calendar className="w-4 h-4" />
              </button>
              <button className="btn-cyber-secondary">
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>
          </div>
          
          <div className="h-64 flex items-end justify-between gap-2" data-testid="line-chart">
            {Array.from({ length: 30 }).map((_, index) => (
              <div 
                key={index}
                className="bg-gradient-to-t from-cyber-cyan/50 to-cyber-purple/50 rounded-t transition-all duration-300 hover:from-cyber-cyan hover:to-cyber-purple"
                style={{ 
                  height: `${Math.random() * 80 + 20}%`,
                  width: '3%'
                }}
              />
            ))}
          </div>
          
          <div className="mt-4 flex items-center justify-between text-sm font-mono text-cyber-cyan/60">
            <span>30 days ago</span>
            <span>Today</span>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="card-cyber-glow p-6">
        <h3 className="font-mono font-semibold text-cyber-cyan text-lg mb-6">
          AI-Powered Optimization Recommendations
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            {
              title: "Rightsize EC2 Instances",
              description: "3 instances are over-provisioned",
              savings: "$890/month",
              priority: "High",
              color: "cyber-pink"
            },
            {
              title: "Reserved Instance Opportunities",
              description: "Convert 5 on-demand instances",
              savings: "$1,200/month", 
              priority: "Medium",
              color: "cyber-orange"
            },
            {
              title: "S3 Lifecycle Policies",
              description: "Optimize storage classes",
              savings: "$250/month",
              priority: "Low",
              color: "cyber-green"
            }
          ].map((rec, index) => (
            <div key={index} className="card-cyber p-4 hover:card-cyber-glow transition-all duration-300">
              <div className="flex items-start justify-between mb-3">
                <h4 className="font-mono font-semibold text-cyber-cyan text-sm">
                  {rec.title}
                </h4>
                <div className={`cyber-badge bg-${rec.color}/20 text-${rec.color}`}>
                  {rec.priority}
                </div>
              </div>
              <p className="font-mono text-cyber-cyan/70 text-xs mb-3">
                {rec.description}
              </p>
              <div className="flex items-center justify-between">
                <span className="font-mono font-bold text-cyber-green text-sm">
                  Save {rec.savings}
                </span>
                <button className="btn-cyber-secondary text-xs px-3 py-1">
                  Apply
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}