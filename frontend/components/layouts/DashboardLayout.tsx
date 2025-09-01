'use client';

import React from 'react';
import CyberNavigation from '@/components/navigation/CyberNavigation';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-cyber-black">
      <CyberNavigation />
      
      {/* Main content */}
      <div className="lg:pl-64">
        <main className="min-h-screen">
          {children}
        </main>
      </div>
    </div>
  );
}