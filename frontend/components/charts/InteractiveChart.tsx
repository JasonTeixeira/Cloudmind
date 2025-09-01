'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Area,
  AreaChart
} from 'recharts';

interface ChartData {
  name: string;
  value: number;
  color?: string;
  trend?: number;
  [key: string]: any;
}

interface InteractiveChartProps {
  data: ChartData[];
  type: 'bar' | 'line' | 'area' | 'pie';
  title: string;
  subtitle?: string;
  height?: number;
  showTooltip?: boolean;
  showGrid?: boolean;
  animate?: boolean;
  colors?: string[];
  onDataPointClick?: (data: ChartData) => void;
}

const CYBER_COLORS = [
  '#00f5ff', // cyber-cyan
  '#8b5cf6', // cyber-purple  
  '#00ff88', // cyber-green
  '#ff6b35', // cyber-orange
  '#ff0080', // cyber-pink
  '#0066ff'  // cyber-blue
];

// Custom Tooltip Component
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-morphism p-3 rounded-lg shadow-[0_0_20px_rgba(0,245,255,0.3)]"
      >
        <p className="font-mono text-cyber-cyan text-sm font-semibold mb-2">
          {label}
        </p>
        {payload.map((entry: any, index: number) => (
          <div key={index} className="flex items-center gap-2">
            <div 
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: entry.color }}
            />
            <span className="font-mono text-cyber-cyan/80 text-sm">
              {entry.name}: 
            </span>
            <span className="font-mono text-cyber-green text-sm font-bold">
              {typeof entry.value === 'number' 
                ? entry.value.toLocaleString() 
                : entry.value
              }
            </span>
          </div>
        ))}
      </motion.div>
    );
  }
  return null;
};

// Custom Bar Component with Hover Effects
const CustomBar = (props: any) => {
  const [isHovered, setIsHovered] = useState(false);
  
  return (
    <motion.rect
      {...props}
      fill={isHovered ? props.fill : `${props.fill}CC`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      whileHover={{ scale: 1.05 }}
      transition={{ duration: 0.2 }}
      style={{ 
        filter: isHovered ? 'drop-shadow(0 0 10px currentColor)' : 'none',
        cursor: 'pointer'
      }}
    />
  );
};

// Animated Number Component
const AnimatedNumber = ({ value, duration = 2000 }: { value: number; duration?: number }) => {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    // Handle NaN or invalid values
    if (value === undefined || value === null || isNaN(value)) {
      setDisplayValue(0);
      return;
    }

    // For tests, show the value immediately
    if (process.env.NODE_ENV === 'test') {
      setDisplayValue(value);
      return;
    }

    let startTime: number;
    let animationFrame: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      
      setDisplayValue(Math.floor(value * progress));
      
      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, [value, duration]);

  return <span>{displayValue.toLocaleString()}</span>;
};

export default function InteractiveChart({
  data,
  type,
  title,
  subtitle,
  height = 300,
  showTooltip = true,
  showGrid = true,
  animate = true,
  colors = CYBER_COLORS,
  onDataPointClick
}: InteractiveChartProps) {
  const [selectedDataPoint, setSelectedDataPoint] = useState<ChartData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => setIsLoading(false), 500);
    return () => clearTimeout(timer);
  }, []);

  const handleDataPointClick = (data: ChartData) => {
    setSelectedDataPoint(data);
    onDataPointClick?.(data);
  };

  if (isLoading) {
    return (
      <div className="card-cyber p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="skeleton h-6 w-48" />
          <div className="skeleton h-8 w-20" />
        </div>
        <div className="space-y-4">
          {Array.from({ length: 6 }).map((_, index) => (
            <div key={index} className="flex items-end space-x-2">
              <div className="skeleton h-4 w-16" />
              <div 
                className="skeleton rounded-r w-full"
                style={{ height: Math.random() * 60 + 20 }}
              />
              <div className="skeleton h-4 w-12" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  const renderChart = () => {
    const commonProps = {
      data,
      width: '100%',
      height,
    };

    switch (type) {
      case 'bar':
        return (
          <ResponsiveContainer {...commonProps}>
            <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              {showGrid && (
                <CartesianGrid 
                  strokeDasharray="3 3" 
                  stroke="rgba(0, 245, 255, 0.1)" 
                />
              )}
              <XAxis 
                dataKey="name" 
                stroke="#00f5ff" 
                fontSize={12}
                fontFamily="JetBrains Mono"
              />
              <YAxis 
                stroke="#00f5ff" 
                fontSize={12}
                fontFamily="JetBrains Mono"
              />
              {showTooltip && <Tooltip content={<CustomTooltip />} />}
              <Bar 
                dataKey="value" 
                fill={colors[0]}
                shape={<CustomBar />}
                onClick={handleDataPointClick}
              />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'line':
        return (
          <ResponsiveContainer {...commonProps}>
            <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              {showGrid && (
                <CartesianGrid 
                  strokeDasharray="3 3" 
                  stroke="rgba(0, 245, 255, 0.1)" 
                />
              )}
              <XAxis 
                dataKey="name" 
                stroke="#00f5ff" 
                fontSize={12}
                fontFamily="JetBrains Mono"
              />
              <YAxis 
                stroke="#00f5ff" 
                fontSize={12}
                fontFamily="JetBrains Mono"
              />
              {showTooltip && <Tooltip content={<CustomTooltip />} />}
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke={colors[0]}
                strokeWidth={3}
                dot={{ fill: colors[0], strokeWidth: 2, r: 6 }}
                activeDot={{ r: 8, stroke: colors[0], strokeWidth: 2, fill: '#0a0a0f' }}
                style={{ filter: 'drop-shadow(0 0 10px currentColor)' }}
              />
            </LineChart>
          </ResponsiveContainer>
        );

      case 'area':
        return (
          <ResponsiveContainer {...commonProps}>
            <AreaChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              {showGrid && (
                <CartesianGrid 
                  strokeDasharray="3 3" 
                  stroke="rgba(0, 245, 255, 0.1)" 
                />
              )}
              <XAxis 
                dataKey="name" 
                stroke="#00f5ff" 
                fontSize={12}
                fontFamily="JetBrains Mono"
              />
              <YAxis 
                stroke="#00f5ff" 
                fontSize={12}
                fontFamily="JetBrains Mono"
              />
              {showTooltip && <Tooltip content={<CustomTooltip />} />}
              <Area 
                type="monotone" 
                dataKey="value" 
                stroke={colors[0]}
                fill={`${colors[0]}33`}
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        );

      case 'pie':
        return (
          <ResponsiveContainer {...commonProps}>
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                outerRadius={height / 3}
                fill="#8884d8"
                dataKey="value"
                onClick={handleDataPointClick}
              >
                {data.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={colors[index % colors.length]}
                    style={{ 
                      filter: 'drop-shadow(0 0 5px currentColor)',
                      cursor: 'pointer'
                    }}
                  />
                ))}
              </Pie>
              {showTooltip && <Tooltip content={<CustomTooltip />} />}
            </PieChart>
          </ResponsiveContainer>
        );

      default:
        return null;
    }
  };

  return (
    <motion.div
      initial={animate ? { opacity: 0, y: 20 } : {}}
      animate={animate ? { opacity: 1, y: 0 } : {}}
      className="card-cyber-glow"
    >
      {/* Header */}
      <div className="flex items-center justify-between p-6 pb-4">
        <div>
          <h3 className="font-mono font-semibold text-cyber-cyan text-lg">
            {title}
          </h3>
          {subtitle && (
            <p className="font-mono text-cyber-cyan/60 text-sm mt-1">
              {subtitle}
            </p>
          )}
        </div>
        
        {/* Chart Stats */}
        <div className="text-right">
          <div className="font-mono font-bold text-cyber-green text-xl">
            <AnimatedNumber value={data.reduce((sum, item) => {
              const val = typeof item.value === 'number' && !isNaN(item.value) ? item.value : 0;
              return sum + val;
            }, 0)} />
          </div>
          <div className="font-mono text-cyber-cyan/60 text-xs">
            Total Value
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="px-6 pb-6">
        {renderChart()}
      </div>

      {/* Selected Data Point Details */}
      <AnimatePresence>
        {selectedDataPoint && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="border-t border-cyber-cyan/20 p-4 bg-cyber-darker/30"
          >
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-mono font-semibold text-cyber-cyan text-sm">
                  {selectedDataPoint.name}
                </h4>
                <p className="font-mono text-cyber-cyan/60 text-xs">
                  Selected data point
                </p>
              </div>
              <div className="text-right">
                <div className="font-mono font-bold text-cyber-green">
                  {selectedDataPoint.value.toLocaleString()}
                </div>
                {selectedDataPoint.trend && (
                  <div className={`font-mono text-xs ${
                    selectedDataPoint.trend > 0 ? 'text-cyber-green' : 'text-cyber-pink'
                  }`}>
                    {selectedDataPoint.trend > 0 ? '+' : ''}{selectedDataPoint.trend}%
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
