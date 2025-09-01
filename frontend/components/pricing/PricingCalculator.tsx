'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import CountUp from 'react-countup';
import { 
  ServiceToken, 
  ServiceCategory, 
  UnitType, 
  PricingCalculationResponse
} from '@/lib/types/pricing';
import api from '@/lib/api/client';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  Calculator, 
  Zap, 
  TrendingUp, 
  DollarSign, 
  Clock, 
  Target,
  Sparkles,
  ArrowRight,
  CheckCircle2
} from 'lucide-react';

interface ServiceSelection {
  service_token_id: string;
  quantity: number;
}

interface PricingCalculatorProps {
  onCalculationChange?: (calculation: PricingCalculationResponse) => void;
  projectedSavings?: number;
  className?: string;
}

export default function PricingCalculator({ 
  onCalculationChange, 
  projectedSavings = 0,
  className = "" 
}: PricingCalculatorProps) {
  const [selectedServices, setSelectedServices] = useState<ServiceSelection[]>([]);
  const [calculation, setCalculation] = useState<PricingCalculationResponse | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);

  // Group services by category
  const [serviceTokens, setServiceTokens] = useState<ServiceToken[]>([])
  useEffect(() => {
    let mounted = true
    api.get('/pricing/tokens')
      .then((res: any) => {
        const data = res.data ?? res
        if (mounted && Array.isArray(data)) setServiceTokens(data)
      })
      .catch(() => {})
    return () => { mounted = false }
  }, [])

  const servicesByCategory = useMemo(() => {
    return serviceTokens.reduce((acc, service) => {
      if (!acc[service.category]) {
        acc[service.category] = [];
      }
      acc[service.category].push(service);
      return acc;
    }, {} as Record<ServiceCategory, ServiceToken[]>);
  }, []);

  // Calculate pricing whenever selections change
  useEffect(() => {
    if (selectedServices.length > 0) {
      calculatePricing();
    } else {
      setCalculation(null);
      onCalculationChange?.(null as any);
    }
  }, [selectedServices, projectedSavings]);

  const calculatePricing = async () => {
    setIsCalculating(true);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    let totalCost = 0;
    let subtotal = 0;
    let totalDiscount = 0;
    const items: any[] = [];
    const breakdownByCategory: Record<string, number> = {};
    const appliedRules: string[] = [];
    let estimatedDuration = 0;

    for (const selection of selectedServices) {
      const token = serviceTokens.find(t => t.id === selection.service_token_id);
      if (!token) continue;

      let unitPrice = token.base_price;
      let totalPrice = unitPrice * selection.quantity;

      // Handle percentage-based pricing
      if (token.unit_type === UnitType.PERCENTAGE_SAVINGS && projectedSavings > 0) {
        unitPrice = (projectedSavings * token.base_price) / 100;
        totalPrice = unitPrice * selection.quantity;
      }

      // Apply volume discounts
      let discount = 0;
      if (token.volume_discount_threshold && 
          selection.quantity >= token.volume_discount_threshold && 
          token.volume_discount_rate) {
        discount = totalPrice * token.volume_discount_rate;
        appliedRules.push(`Volume discount (${(token.volume_discount_rate * 100).toFixed(0)}%) on ${token.name}`);
      }

      const finalPrice = totalPrice - discount;

      // Add to category breakdown
      if (!breakdownByCategory[token.category]) {
        breakdownByCategory[token.category] = 0;
      }
      breakdownByCategory[token.category] += finalPrice;

      // Add estimated duration
      if (token.estimated_duration_hours) {
        estimatedDuration += token.estimated_duration_hours * selection.quantity;
      }

      items.push({
        service_token_id: token.id,
        service_name: token.name,
        quantity: selection.quantity,
        unit_price: unitPrice,
        total_price: totalPrice,
        discount: discount,
        final_price: finalPrice,
        category: token.category,
        unit_type: token.unit_type
      });

      subtotal += totalPrice;
      totalDiscount += discount;
      totalCost += finalPrice;
    }

    // Calculate ROI if projected savings provided
    let roiPercentage: number | undefined;
    let paybackMonths: number | undefined;
    if (projectedSavings > 0) {
      const annualSavings = projectedSavings * 12;
      roiPercentage = ((annualSavings - totalCost) / totalCost) * 100;
      paybackMonths = totalCost / projectedSavings;
    }

    // Try real backend calculation; fallback to local
    try {
      const response: any = await api.post('/pricing/calculate', {
        client_id: 'demo-client',
        items: selectedServices.map(s => ({ token_id: s.service_token_id, quantity: s.quantity })),
        volume_discount_pct: undefined
      })
      const data: PricingCalculationResponse = response.data ?? response
      setCalculation(data)
      onCalculationChange?.(data)
    } catch {
      const result: PricingCalculationResponse = {
        total_cost: totalCost,
        subtotal: subtotal,
        total_discount: totalDiscount,
        discount_percentage: subtotal > 0 ? (totalDiscount / subtotal) * 100 : 0,
        estimated_duration_hours: estimatedDuration > 0 ? estimatedDuration : undefined,
        breakdown_by_category: breakdownByCategory,
        items: items,
        applied_rules: appliedRules,
        projected_monthly_savings: projectedSavings > 0 ? projectedSavings : undefined,
        roi_percentage: roiPercentage,
        payback_months: paybackMonths
      };
      setCalculation(result);
      onCalculationChange?.(result);
    } finally {
      setIsCalculating(false);
    }
  };

  const addService = (serviceId: string) => {
    const existing = selectedServices.find(s => s.service_token_id === serviceId);
    if (existing) {
      setSelectedServices(prev => 
        prev.map(s => 
          s.service_token_id === serviceId 
            ? { ...s, quantity: s.quantity + 1 }
            : s
        )
      );
    } else {
      setSelectedServices(prev => [...prev, { service_token_id: serviceId, quantity: 1 }]);
    }
  };

  const updateQuantity = (serviceId: string, quantity: number) => {
    if (quantity <= 0) {
      setSelectedServices(prev => prev.filter(s => s.service_token_id !== serviceId));
    } else {
      setSelectedServices(prev => 
        prev.map(s => 
          s.service_token_id === serviceId 
            ? { ...s, quantity }
            : s
        )
      );
    }
  };

  const getCategoryIcon = (category: ServiceCategory) => {
    switch (category) {
      case ServiceCategory.SCANNING: return <Zap className="w-4 h-4" />;
      case ServiceCategory.OPTIMIZATION: return <TrendingUp className="w-4 h-4" />;
      case ServiceCategory.DOCUMENTATION: return <CheckCircle2 className="w-4 h-4" />;
      case ServiceCategory.IMPLEMENTATION: return <Target className="w-4 h-4" />;
      case ServiceCategory.CONSULTING: return <Sparkles className="w-4 h-4" />;
      default: return <Calculator className="w-4 h-4" />;
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  };

  const formatUnitType = (unitType: UnitType) => {
    switch (unitType) {
      case UnitType.PER_RESOURCE: return 'per resource';
      case UnitType.PER_HOUR: return 'per hour';
      case UnitType.FLAT_RATE: return 'flat rate';
      case UnitType.PERCENTAGE_SAVINGS: return '% of savings';
      case UnitType.PER_GB: return 'per GB';
      case UnitType.PER_API_CALL: return 'per API call';
      default: return unitType;
    }
  };

  return (
    <div className={`pricing-calculator-cyber ${className}`}>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Service Selection */}
        <div className="lg:col-span-2 space-y-6">
          <div className="text-center mb-8">
            <h2 className="text-cyber-title mb-4">
              <Calculator className="inline-block w-8 h-8 mr-3" />
              Tokenized Pricing Calculator
            </h2>
            <p className="text-cyber-cyan/70 font-mono">
              Select services to see transparent, real-time pricing with volume discounts and ROI calculations
            </p>
          </div>

          {Object.entries(servicesByCategory).map(([category, services]) => (
            <motion.div
              key={category}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-4"
            >
              <div className="flex items-center gap-3 mb-4">
                {getCategoryIcon(category as ServiceCategory)}
                <h3 className="text-cyber-subtitle capitalize">
                  {category.replace('_', ' ')}
                </h3>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {services.map((service) => {
                  const selection = selectedServices.find(s => s.service_token_id === service.id);
                  const isSelected = !!selection;

                  return (
                    <motion.div
                      key={service.id}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      className={`service-token-cyber ${isSelected ? 'ring-2 ring-cyber-cyan' : ''}`}
                    >
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h4 className="font-mono font-semibold text-cyber-cyan text-sm mb-1">
                            {service.name}
                          </h4>
                          <p className="text-cyber-cyan/60 text-xs leading-relaxed">
                            {service.description}
                          </p>
                        </div>
                        {service.requires_approval && (
                          <Badge className="badge-cyber-warning ml-2">
                            Approval Required
                          </Badge>
                        )}
                      </div>

                      <div className="flex items-center justify-between mb-3">
                        <div className="text-cyber-green font-mono font-bold">
                          {formatCurrency(service.base_price)}
                          <span className="text-cyber-cyan/60 text-xs ml-1">
                            {formatUnitType(service.unit_type)}
                          </span>
                        </div>
                        {service.volume_discount_threshold && (
                          <Badge className="badge-cyber-info text-xs">
                            {(service.volume_discount_rate! * 100).toFixed(0)}% off at {service.volume_discount_threshold}+
                          </Badge>
                        )}
                      </div>

                      <div className="flex items-center gap-2">
                        {isSelected ? (
                          <div className="flex items-center gap-2 flex-1">
                            <Button
                              size="sm"
                              variant="outline"
                              className="btn-cyber-secondary h-8 w-8 p-0"
                              onClick={() => updateQuantity(service.id, selection.quantity - 1)}
                            >
                              -
                            </Button>
                            <Input
                              type="number"
                              min="1"
                              value={selection.quantity}
                              onChange={(e) => updateQuantity(service.id, parseInt(e.target.value) || 0)}
                              className="input-cyber text-center h-8 w-16"
                            />
                            <Button
                              size="sm"
                              variant="outline"
                              className="btn-cyber-secondary h-8 w-8 p-0"
                              onClick={() => updateQuantity(service.id, selection.quantity + 1)}
                            >
                              +
                            </Button>
                          </div>
                        ) : (
                          <Button
                            onClick={() => addService(service.id)}
                            className="btn-cyber-primary flex-1 h-8"
                            size="sm"
                          >
                            Add Service
                          </Button>
                        )}
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Pricing Summary */}
        <div className="space-y-6">
          <Card className="card-cyber-glow sticky top-6">
            <CardHeader>
              <CardTitle className="text-cyber-cyan font-mono flex items-center gap-2">
                <DollarSign className="w-5 h-5" />
                Pricing Summary
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {isCalculating ? (
                <div className="text-center py-8">
                  <div className="loading-cyber mx-auto mb-4" />
                  <p className="text-cyber-cyan/70 font-mono text-sm">Calculating...</p>
                </div>
              ) : calculation ? (
                <AnimatePresence mode="wait">
                  <motion.div
                    key="calculation"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="space-y-6"
                  >
                    {/* Total Cost */}
                    <div className="text-center">
                      <div className="cost-display-cyber">
                        $<CountUp
                          end={calculation.total_cost}
                          duration={1}
                          decimals={2}
                          decimal="."
                          separator=","
                        />
                      </div>
                      <p className="text-cyber-cyan/70 font-mono text-sm">Total Cost</p>
                    </div>

                    {/* Discount Info */}
                    {calculation.total_discount > 0 && (
                      <div className="text-center">
                        <div className="text-cyber-green font-mono font-bold text-xl">
                          -{formatCurrency(calculation.total_discount)}
                        </div>
                        <p className="text-cyber-green/70 font-mono text-sm">
                          {calculation.discount_percentage.toFixed(1)}% Discount Applied
                        </p>
                      </div>
                    )}

                    <Separator className="bg-cyber-cyan/20" />

                    {/* ROI Information */}
                    {calculation.projected_monthly_savings && (
                      <div className="space-y-4">
                        <div className="text-center">
                          <div className="savings-display-cyber">
                            {formatCurrency(calculation.projected_monthly_savings)}/mo
                          </div>
                          <p className="text-cyber-cyan/70 font-mono text-sm">Projected Savings</p>
                        </div>

                        {calculation.roi_percentage && (
                          <div className="text-center">
                            <div className="roi-display-cyber">
                              <CountUp
                                end={calculation.roi_percentage}
                                duration={1.5}
                                decimals={0}
                                suffix="%"
                              /> ROI
                            </div>
                            <p className="text-cyber-purple/70 font-mono text-sm">Annual Return</p>
                          </div>
                        )}

                        {calculation.payback_months && (
                          <div className="text-center">
                            <div className="text-cyber-orange font-mono font-semibold text-lg">
                              <CountUp
                                end={calculation.payback_months}
                                duration={1.2}
                                decimals={1}
                              /> months
                            </div>
                            <p className="text-cyber-orange/70 font-mono text-sm">Payback Period</p>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Duration */}
                    {calculation.estimated_duration_hours && (
                      <>
                        <Separator className="bg-cyber-cyan/20" />
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <Clock className="w-4 h-4 text-cyber-cyan" />
                            <span className="font-mono text-sm text-cyber-cyan/70">Duration</span>
                          </div>
                          <span className="font-mono font-semibold text-cyber-cyan">
                            {calculation.estimated_duration_hours.toFixed(1)}h
                          </span>
                        </div>
                      </>
                    )}

                    {/* Applied Rules */}
                    {calculation.applied_rules.length > 0 && (
                      <>
                        <Separator className="bg-cyber-cyan/20" />
                        <div className="space-y-2">
                          <p className="font-mono text-sm text-cyber-cyan/70">Applied Discounts:</p>
                          {calculation.applied_rules.map((rule, index) => (
                            <div key={index} className="flex items-center gap-2">
                              <CheckCircle2 className="w-3 h-3 text-cyber-green" />
                              <span className="font-mono text-xs text-cyber-green">{rule}</span>
                            </div>
                          ))}
                        </div>
                      </>
                    )}

                    {/* Category Breakdown */}
                    {Object.keys(calculation.breakdown_by_category).length > 0 && (
                      <>
                        <Separator className="bg-cyber-cyan/20" />
                        <div className="space-y-2">
                          <p className="font-mono text-sm text-cyber-cyan/70">Breakdown:</p>
                          {Object.entries(calculation.breakdown_by_category).map(([category, amount]) => (
                            <div key={category} className="flex items-center justify-between">
                              <div className="flex items-center gap-2">
                                {getCategoryIcon(category as ServiceCategory)}
                                <span className="font-mono text-xs text-cyber-cyan/80 capitalize">
                                  {category.replace('_', ' ')}
                                </span>
                              </div>
                              <span className="font-mono text-sm text-cyber-cyan">
                                {formatCurrency(amount)}
                              </span>
                            </div>
                          ))}
                        </div>
                      </>
                    )}
                  </motion.div>
                </AnimatePresence>
              ) : (
                <div className="text-center py-8">
                  <Calculator className="w-12 h-12 text-cyber-cyan/30 mx-auto mb-4" />
                  <p className="text-cyber-cyan/50 font-mono text-sm">
                    Select services to see pricing
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
