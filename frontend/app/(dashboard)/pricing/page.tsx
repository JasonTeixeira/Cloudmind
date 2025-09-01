'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import PricingCalculator from '@/components/pricing/PricingCalculator';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  DollarSign, 
  TrendingUp, 
  Calculator, 
  Zap,
  Target,
  Clock,
  Users,
  Building,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { PricingCalculationResponse } from '@/lib/types/pricing';

export default function PricingPage() {
  const [projectedSavings, setProjectedSavings] = useState<number>(25000);
  const [currentCalculation, setCurrentCalculation] = useState<PricingCalculationResponse | null>(null);

  const handleCalculationChange = (calculation: PricingCalculationResponse) => {
    setCurrentCalculation(calculation);
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
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
            <Sparkles className="inline-block w-10 h-10 mr-4" />
            CloudMind Tokenized Pricing
          </h1>
          <p className="text-cyber-cyan/70 font-mono text-lg max-w-3xl mx-auto">
            Revolutionary transparent pricing for cloud infrastructure optimization consulting. 
            See exactly what you pay for, when you pay for it, and the ROI in real-time.
          </p>
        </div>

        {/* Key Features */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card className="card-cyber text-center">
            <CardContent className="p-4">
              <Calculator className="w-8 h-8 text-cyber-cyan mx-auto mb-2" />
              <h3 className="font-mono font-semibold text-cyber-cyan text-sm mb-1">
                Tokenized Services
              </h3>
              <p className="text-cyber-cyan/60 text-xs">
                Every service is a billable token with transparent pricing
              </p>
            </CardContent>
          </Card>

          <Card className="card-cyber text-center">
            <CardContent className="p-4">
              <TrendingUp className="w-8 h-8 text-cyber-green mx-auto mb-2" />
              <h3 className="font-mono font-semibold text-cyber-green text-sm mb-1">
                Volume Discounts
              </h3>
              <p className="text-cyber-cyan/60 text-xs">
                Automatic discounts for large engagements
              </p>
            </CardContent>
          </Card>

          <Card className="card-cyber text-center">
            <CardContent className="p-4">
              <Target className="w-8 h-8 text-cyber-purple mx-auto mb-2" />
              <h3 className="font-mono font-semibold text-cyber-purple text-sm mb-1">
                ROI Calculations
              </h3>
              <p className="text-cyber-cyan/60 text-xs">
                Real-time ROI and payback period calculations
              </p>
            </CardContent>
          </Card>

          <Card className="card-cyber text-center">
            <CardContent className="p-4">
              <Zap className="w-8 h-8 text-cyber-orange mx-auto mb-2" />
              <h3 className="font-mono font-semibold text-cyber-orange text-sm mb-1">
                Live Progress
              </h3>
              <p className="text-cyber-cyan/60 text-xs">
                Real-time cost and savings tracking
              </p>
            </CardContent>
          </Card>
        </div>
      </motion.div>

      {/* Projected Savings Input */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="mb-8"
      >
        <Card className="card-cyber-glow max-w-md mx-auto">
          <CardHeader>
            <CardTitle className="text-cyber-cyan font-mono text-center flex items-center justify-center gap-2">
              <DollarSign className="w-5 h-5" />
              Projected Monthly Savings
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <Label className="form-label-cyber">
                  Enter your estimated monthly cloud savings
                </Label>
                <Input
                  type="number"
                  value={projectedSavings}
                  onChange={(e) => setProjectedSavings(Number(e.target.value) || 0)}
                  className="input-cyber text-center text-xl"
                  placeholder="25000"
                />
              </div>
              <div className="text-center">
                <p className="text-cyber-cyan/70 font-mono text-sm">
                  This affects percentage-based pricing and ROI calculations
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Main Pricing Calculator */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="mb-8"
      >
        <PricingCalculator
          onCalculationChange={handleCalculationChange}
          projectedSavings={projectedSavings}
        />
      </motion.div>

      {/* Results Summary */}
      {currentCalculation && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-8"
        >
          <Card className="card-cyber-glow">
            <CardHeader>
              <CardTitle className="text-cyber-cyan font-mono text-center flex items-center justify-center gap-2">
                <CheckCircle2 className="w-5 h-5" />
                Engagement Summary
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Financial Summary */}
                <div className="text-center">
                  <div className="cost-display-cyber mb-2">
                    {formatCurrency(currentCalculation.total_cost)}
                  </div>
                  <p className="text-cyber-cyan/70 font-mono text-sm mb-4">Total Investment</p>
                  
                  {currentCalculation.total_discount > 0 && (
                    <div className="space-y-2">
                      <Badge className="badge-cyber-success">
                        {formatCurrency(currentCalculation.total_discount)} saved
                      </Badge>
                      <p className="text-cyber-green/70 font-mono text-xs">
                        {currentCalculation.discount_percentage.toFixed(1)}% discount applied
                      </p>
                    </div>
                  )}
                </div>

                {/* ROI Summary */}
                {currentCalculation.projected_monthly_savings && (
                  <div className="text-center">
                    <div className="savings-display-cyber mb-2">
                      {formatCurrency(currentCalculation.projected_monthly_savings * 12)}
                    </div>
                    <p className="text-cyber-cyan/70 font-mono text-sm mb-4">Annual Savings</p>
                    
                    {currentCalculation.roi_percentage && (
                      <div className="space-y-2">
                        <Badge className="badge-cyber-info">
                          {currentCalculation.roi_percentage.toFixed(0)}% ROI
                        </Badge>
                        {currentCalculation.payback_months && (
                          <p className="text-cyber-purple/70 font-mono text-xs">
                            {currentCalculation.payback_months.toFixed(1)} month payback
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {/* Service Summary */}
                <div className="text-center">
                  <div className="text-3xl font-mono font-bold text-cyber-purple mb-2">
                    {currentCalculation.items.length}
                  </div>
                  <p className="text-cyber-cyan/70 font-mono text-sm mb-4">Services Selected</p>
                  
                  {currentCalculation.estimated_duration_hours && (
                    <div className="space-y-2">
                      <Badge className="badge-cyber-warning">
                        <Clock className="w-3 h-3 mr-1" />
                        {currentCalculation.estimated_duration_hours.toFixed(1)}h
                      </Badge>
                      <p className="text-cyber-orange/70 font-mono text-xs">
                        Estimated duration
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* Service Breakdown */}
              <Separator className="bg-cyber-cyan/20 my-6" />
              
              <div className="space-y-4">
                <h4 className="text-cyber-cyan font-mono font-semibold text-center">
                  Selected Services
                </h4>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {currentCalculation.items.map((item, index) => (
                    <div key={index} className="card-cyber p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h5 className="font-mono font-semibold text-cyber-cyan text-sm">
                          {item.service_name}
                        </h5>
                        <Badge className="badge-cyber-info text-xs">
                          {item.category.replace('_', ' ')}
                        </Badge>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="font-mono text-cyber-cyan/70 text-sm">
                          {item.quantity}x {formatCurrency(item.unit_price)}
                        </span>
                        <div className="text-right">
                          {item.discount > 0 && (
                            <div className="text-cyber-green font-mono text-xs line-through">
                              {formatCurrency(item.total_price)}
                            </div>
                          )}
                          <div className="font-mono font-bold text-cyber-green">
                            {formatCurrency(item.final_price)}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Call to Action */}
              <div className="text-center mt-8">
                <Button className="btn-cyber-primary text-lg px-8 py-3">
                  Create Engagement
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
                <p className="text-cyber-cyan/50 font-mono text-sm mt-2">
                  Ready to start your optimization journey?
                </p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Value Proposition */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="text-center"
      >
        <Card className="card-cyber max-w-4xl mx-auto">
          <CardContent className="p-8">
            <h3 className="text-cyber-subtitle mb-6">
              Why CloudMind's Tokenized Pricing is Revolutionary
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <AlertCircle className="w-8 h-8 text-cyber-cyan mx-auto mb-3" />
                <h4 className="font-mono font-semibold text-cyber-cyan mb-2">
                  Complete Transparency
                </h4>
                <p className="text-cyber-cyan/70 text-sm">
                  See exactly what you're paying for with itemized, real-time pricing
                </p>
              </div>
              
              <div className="text-center">
                <Users className="w-8 h-8 text-cyber-green mx-auto mb-3" />
                <h4 className="font-mono font-semibold text-cyber-green mb-2">
                  Client Portal Access
                </h4>
                <p className="text-cyber-cyan/70 text-sm">
                  Track progress, costs, and savings in real-time through your dedicated portal
                </p>
              </div>
              
              <div className="text-center">
                <Building className="w-8 h-8 text-cyber-purple mx-auto mb-3" />
                <h4 className="font-mono font-semibold text-cyber-purple mb-2">
                  Enterprise Grade
                </h4>
                <p className="text-cyber-cyan/70 text-sm">
                  Professional documentation, GitHub integration, and automated reporting
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
