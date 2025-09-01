'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface SkeletonProps {
  className?: string;
  width?: string | number;
  height?: string | number;
  variant?: 'text' | 'circular' | 'rectangular' | 'card';
  lines?: number;
  animate?: boolean;
}

export function Skeleton({ 
  className = '', 
  width, 
  height, 
  variant = 'rectangular',
  lines = 1,
  animate = true
}: SkeletonProps) {
  const baseClasses = 'skeleton';
  
  const getVariantClasses = () => {
    switch (variant) {
      case 'text':
        return 'h-4 w-full rounded';
      case 'circular':
        return 'rounded-full';
      case 'card':
        return 'h-48 w-full rounded-lg';
      default:
        return 'rounded';
    }
  };

  const style = {
    width: typeof width === 'number' ? `${width}px` : width,
    height: typeof height === 'number' ? `${height}px` : height,
  };

  if (variant === 'text' && lines > 1) {
    return (
      <div className="space-y-2">
        {Array.from({ length: lines }).map((_, index) => (
          <motion.div
            key={index}
            initial={animate ? { opacity: 0 } : {}}
            animate={animate ? { opacity: 1 } : {}}
            transition={{ delay: index * 0.1 }}
            className={`${baseClasses} ${getVariantClasses()} ${className}`}
            style={{
              ...style,
              width: index === lines - 1 ? '75%' : '100%'
            }}
          />
        ))}
      </div>
    );
  }

  return (
    <motion.div
      initial={animate ? { opacity: 0 } : {}}
      animate={animate ? { opacity: 1 } : {}}
      className={`${baseClasses} ${getVariantClasses()} ${className}`}
      style={style}
    />
  );
}

// Pre-built skeleton components for common use cases
export function CardSkeleton({ className = '' }: { className?: string }) {
  return (
    <div className={`card-cyber p-6 ${className}`}>
      <div className="flex items-center space-x-4 mb-4">
        <Skeleton variant="circular" width={40} height={40} />
        <div className="space-y-2 flex-1">
          <Skeleton variant="text" width="60%" />
          <Skeleton variant="text" width="40%" />
        </div>
      </div>
      <Skeleton variant="rectangular" height={120} className="mb-4" />
      <div className="space-y-2">
        <Skeleton variant="text" lines={3} />
      </div>
    </div>
  );
}

export function TableSkeleton({ rows = 5, columns = 4 }: { rows?: number; columns?: number }) {
  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="grid gap-4" style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}>
        {Array.from({ length: columns }).map((_, index) => (
          <Skeleton key={`header-${index}`} variant="text" height={20} />
        ))}
      </div>
      
      {/* Rows */}
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <div key={`row-${rowIndex}`} className="grid gap-4" style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}>
          {Array.from({ length: columns }).map((_, colIndex) => (
            <Skeleton key={`cell-${rowIndex}-${colIndex}`} variant="text" height={16} />
          ))}
        </div>
      ))}
    </div>
  );
}

export function ChartSkeleton({ className = '' }: { className?: string }) {
  return (
    <div className={`card-cyber p-6 ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <Skeleton variant="text" width="40%" height={24} />
        <Skeleton variant="rectangular" width={80} height={32} />
      </div>
      
      <div className="space-y-4">
        {/* Chart bars */}
        {Array.from({ length: 6 }).map((_, index) => (
          <div key={index} className="flex items-end space-x-2">
            <Skeleton variant="text" width="20%" height={16} />
            <Skeleton 
              variant="rectangular" 
              width="70%" 
              height={Math.random() * 60 + 20}
              className="rounded-r"
            />
            <Skeleton variant="text" width="10%" height={16} />
          </div>
        ))}
      </div>
    </div>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="space-y-8 page-transition">
      {/* Header */}
      <div className="text-center space-y-4">
        <Skeleton variant="text" width="60%" height={40} className="mx-auto" />
        <Skeleton variant="text" width="80%" height={20} className="mx-auto" />
      </div>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {Array.from({ length: 4 }).map((_, index) => (
          <CardSkeleton key={index} />
        ))}
      </div>
      
      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <ChartSkeleton />
        </div>
        <div className="space-y-6">
          <CardSkeleton />
          <CardSkeleton />
        </div>
      </div>
    </div>
  );
}
