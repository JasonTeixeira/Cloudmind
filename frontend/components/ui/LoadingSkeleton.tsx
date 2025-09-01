import React from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';

interface LoadingSkeletonProps {
  variant?: 'card' | 'stat' | 'list' | 'chart';
  count?: number;
}

const SkeletonBox: React.FC<{ className?: string }> = ({ className = '' }) => (
  <div className={`skeleton ${className}`} />
);

export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({ 
  variant = 'card', 
  count = 1 
}) => {
  const renderSkeleton = () => {
    switch (variant) {
      case 'stat':
        return (
          <Card className="card-cyber">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <SkeletonBox className="w-8 h-8 rounded-full" />
                <SkeletonBox className="w-3 h-3 rounded-full" />
              </div>
              <div className="space-y-2">
                <SkeletonBox className="h-4 w-24" />
                <SkeletonBox className="h-8 w-16" />
                <SkeletonBox className="h-3 w-32" />
              </div>
            </CardContent>
          </Card>
        );
      
      case 'list':
        return (
          <Card className="card-cyber">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <SkeletonBox className="w-6 h-6 rounded-full" />
                <div className="flex-1 space-y-2">
                  <SkeletonBox className="h-4 w-3/4" />
                  <SkeletonBox className="h-3 w-1/2" />
                </div>
                <SkeletonBox className="h-4 w-16" />
              </div>
            </CardContent>
          </Card>
        );
      
      case 'chart':
        return (
          <Card className="card-cyber">
            <CardHeader>
              <SkeletonBox className="h-6 w-48" />
            </CardHeader>
            <CardContent>
              <SkeletonBox className="h-64 w-full rounded-lg" />
            </CardContent>
          </Card>
        );
      
      default:
        return (
          <Card className="card-cyber">
            <CardHeader>
              <SkeletonBox className="h-6 w-3/4" />
              <SkeletonBox className="h-4 w-1/2" />
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <SkeletonBox className="h-4 w-full" />
                <SkeletonBox className="h-4 w-5/6" />
                <SkeletonBox className="h-4 w-4/6" />
              </div>
            </CardContent>
          </Card>
        );
    }
  };

  return (
    <>
      {Array.from({ length: count }, (_, i) => (
        <div key={i}>
          {renderSkeleton()}
        </div>
      ))}
    </>
  );
};

export const DashboardSkeleton: React.FC = () => (
  <div className="min-h-screen bg-cyber-black p-6">
    {/* Header Skeleton */}
    <div className="text-center mb-8">
      <SkeletonBox className="h-12 w-96 mx-auto mb-4" />
      <SkeletonBox className="h-6 w-64 mx-auto" />
    </div>
    
    {/* Stats Grid Skeleton */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <LoadingSkeleton variant="stat" count={4} />
    </div>
    
    {/* Quick Actions Skeleton */}
    <div className="mb-8">
      <SkeletonBox className="h-8 w-48 mx-auto mb-6" />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <LoadingSkeleton variant="card" count={4} />
      </div>
    </div>
    
    {/* Platform Status Skeleton */}
    <LoadingSkeleton variant="chart" count={1} />
  </div>
);

export default LoadingSkeleton;



