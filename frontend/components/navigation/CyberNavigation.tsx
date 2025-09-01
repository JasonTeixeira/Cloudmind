'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Calculator, 
  BarChart3, 
  Shield, 
  Zap, 
  Settings, 
  Menu, 
  X,
  Home,
  DollarSign,
  TrendingUp,
  Users,
  FileText,
  Terminal,
  Sparkles
} from 'lucide-react';
import { Button } from '@/components/ui/button';

const navigationItems = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: Home,
    description: 'Overview and metrics'
  },
  {
    name: 'Pricing Calculator',
    href: '/pricing',
    icon: Calculator,
    description: 'Tokenized pricing system',
    highlight: true
  },
  {
    name: 'Client Portal',
    href: '/client-portal',
    icon: Users,
    description: 'Real-time engagement tracking'
  },
  {
    name: 'Cost Analysis',
    href: '/cost-analysis',
    icon: DollarSign,
    description: 'Cost optimization insights'
  },
  {
    name: 'Infrastructure',
    href: '/infrastructure',
    icon: Zap,
    description: 'Cloud infrastructure management'
  },
  {
    name: 'Security',
    href: '/security',
    icon: Shield,
    description: 'Security monitoring'
  },
  {
    name: 'Reports',
    href: '/reports',
    icon: FileText,
    description: 'Analytics and reports'
  },
  {
    name: 'AI Terminal',
    href: '/terminal',
    icon: Terminal,
    description: 'AI-powered terminal'
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Settings,
    description: 'Platform configuration'
  }
];

export default function CyberNavigation() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  const isActive = (href: string) => {
    if (href === '/dashboard') {
      return pathname === '/dashboard' || pathname === '/';
    }
    return pathname.startsWith(href);
  };

  return (
    <>
      {/* Mobile Menu Button */}
      <Button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-50 lg:hidden btn-cyber-primary"
        size="sm"
      >
        {isOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
      </Button>

      {/* Sidebar */}
      <AnimatePresence>
        <motion.nav
          initial={{ x: -300 }}
          animate={{ x: isOpen || (typeof window !== 'undefined' && window.innerWidth >= 1024) ? 0 : -300 }}
          exit={{ x: -300 }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
          className="sidebar-cyber"
        >
          {/* Logo */}
          <div className="p-6 border-b border-cyber-cyan/30">
            <Link href="/dashboard" className="flex items-center gap-3">
              <div className="w-8 h-8 bg-gradient-to-br from-cyber-cyan to-cyber-purple rounded-lg flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-cyber-black" />
              </div>
              <div>
                <h1 className="font-mono font-bold text-cyber-cyan text-lg">
                  CloudMind
                </h1>
                <p className="font-mono text-cyber-cyan/60 text-xs">
                  Cyberpunk FinOps
                </p>
              </div>
            </Link>
          </div>

          {/* Navigation Items */}
          <div className="flex-1 p-4 space-y-2">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.href);
              
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className={`
                    relative flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200
                    ${active 
                      ? 'bg-cyber-cyan/10 border border-cyber-cyan/50 text-cyber-cyan shadow-[0_0_15px_rgba(0,245,255,0.2)]' 
                      : 'text-cyber-cyan/70 hover:text-cyber-cyan hover:bg-cyber-cyan/5'
                    }
                    ${item.highlight ? 'ring-1 ring-cyber-purple/50' : ''}
                  `}
                >
                  {active && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute inset-0 bg-cyber-cyan/5 rounded-lg border border-cyber-cyan/30"
                      initial={false}
                      transition={{ type: "spring", stiffness: 500, damping: 30 }}
                    />
                  )}
                  
                  <Icon className={`w-5 h-5 relative z-10 ${active ? 'text-cyber-cyan' : ''}`} />
                  
                  <div className="relative z-10">
                    <div className={`font-mono font-medium text-sm ${active ? 'text-cyber-cyan' : ''}`}>
                      {item.name}
                      {item.highlight && (
                        <span className="ml-2 text-xs bg-cyber-purple/20 text-cyber-purple px-2 py-0.5 rounded-full">
                          NEW
                        </span>
                      )}
                    </div>
                    <div className="font-mono text-xs text-cyber-cyan/50">
                      {item.description}
                    </div>
                  </div>
                  
                  {active && (
                    <div className="absolute right-2 w-2 h-2 bg-cyber-cyan rounded-full animate-pulse" />
                  )}
                </Link>
              );
            })}
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-cyber-cyan/30">
            <div className="text-center">
              <div className="text-cyber-cyan/50 font-mono text-xs mb-2">
                System Status
              </div>
              <div className="flex items-center justify-center gap-2">
                <div className="status-cyber-online" />
                <span className="font-mono text-cyber-green text-xs">
                  All Systems Operational
                </span>
              </div>
            </div>
          </div>
        </motion.nav>
      </AnimatePresence>

      {/* Mobile Overlay */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 bg-cyber-black/80 backdrop-blur-sm z-40 lg:hidden"
        />
      )}
    </>
  );
}
