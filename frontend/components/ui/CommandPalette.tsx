'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { 
  Search, 
  Calculator, 
  BarChart3, 
  Zap, 
  Shield, 
  FileText, 
  Users, 
  Settings,
  Home,
  DollarSign,
  Terminal,
  Command,
  ArrowRight,
  Clock,
  TrendingUp
} from 'lucide-react';

interface Command {
  id: string;
  title: string;
  subtitle?: string;
  icon: React.ComponentType<any>;
  action: () => void;
  category: string;
  keywords: string[];
}

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function CommandPalette({ isOpen, onClose }: CommandPaletteProps) {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const commands: Command[] = [
    // Navigation
    {
      id: 'nav-dashboard',
      title: 'Dashboard',
      subtitle: 'Go to main dashboard',
      icon: Home,
      action: () => router.push('/dashboard'),
      category: 'Navigation',
      keywords: ['dashboard', 'home', 'overview']
    },
    {
      id: 'nav-pricing',
      title: 'Pricing Calculator',
      subtitle: 'Calculate tokenized pricing',
      icon: Calculator,
      action: () => router.push('/pricing'),
      category: 'Navigation',
      keywords: ['pricing', 'calculator', 'cost', 'tokenized']
    },
    {
      id: 'nav-client-portal',
      title: 'Client Portal',
      subtitle: 'View client engagement tracking',
      icon: Users,
      action: () => router.push('/client-portal'),
      category: 'Navigation',
      keywords: ['client', 'portal', 'engagement', 'tracking']
    },
    {
      id: 'nav-infrastructure',
      title: 'Infrastructure Scanner',
      subtitle: 'Scan and analyze infrastructure',
      icon: Zap,
      action: () => router.push('/infrastructure'),
      category: 'Navigation',
      keywords: ['infrastructure', 'scanner', 'resources', 'cloud']
    },
    {
      id: 'nav-cost-analysis',
      title: 'Cost Analysis',
      subtitle: 'Analyze cost breakdown and trends',
      icon: BarChart3,
      action: () => router.push('/cost-analysis'),
      category: 'Navigation',
      keywords: ['cost', 'analysis', 'breakdown', 'trends', 'optimization']
    },
    {
      id: 'nav-security',
      title: 'Security Assessment',
      subtitle: 'View security analysis',
      icon: Shield,
      action: () => router.push('/security'),
      category: 'Navigation',
      keywords: ['security', 'assessment', 'vulnerabilities', 'scan']
    },
    {
      id: 'nav-reports',
      title: 'Reports',
      subtitle: 'Generate and view reports',
      icon: FileText,
      action: () => router.push('/reports'),
      category: 'Navigation',
      keywords: ['reports', 'analytics', 'documentation']
    },
    {
      id: 'nav-terminal',
      title: 'AI Terminal',
      subtitle: 'AI-powered command interface',
      icon: Terminal,
      action: () => router.push('/terminal'),
      category: 'Navigation',
      keywords: ['terminal', 'ai', 'command', 'assistant']
    },
    {
      id: 'nav-settings',
      title: 'Settings',
      subtitle: 'Configure platform settings',
      icon: Settings,
      action: () => router.push('/settings'),
      category: 'Navigation',
      keywords: ['settings', 'configuration', 'preferences']
    },

    // Quick Actions
    {
      id: 'action-new-engagement',
      title: 'Create New Engagement',
      subtitle: 'Start a new client engagement',
      icon: Users,
      action: () => {
        router.push('/pricing');
        // Could open a modal or form
      },
      category: 'Actions',
      keywords: ['create', 'new', 'engagement', 'client', 'project']
    },
    {
      id: 'action-run-scan',
      title: 'Run Infrastructure Scan',
      subtitle: 'Start scanning cloud resources',
      icon: Zap,
      action: () => {
        router.push('/infrastructure');
        // Could trigger scan
      },
      category: 'Actions',
      keywords: ['run', 'scan', 'infrastructure', 'resources', 'analyze']
    },
    {
      id: 'action-generate-report',
      title: 'Generate Cost Report',
      subtitle: 'Create comprehensive cost analysis report',
      icon: FileText,
      action: () => {
        router.push('/cost-analysis');
        // Could trigger report generation
      },
      category: 'Actions',
      keywords: ['generate', 'report', 'cost', 'analysis', 'export']
    },

    // Recent Items (could be dynamic)
    {
      id: 'recent-techcorp',
      title: 'TechCorp Engagement',
      subtitle: 'AWS Infrastructure Optimization - 67% complete',
      icon: TrendingUp,
      action: () => router.push('/client-portal'),
      category: 'Recent',
      keywords: ['techcorp', 'engagement', 'aws', 'optimization']
    }
  ];

  const filteredCommands = commands.filter(command => {
    if (!query) return true;
    const searchQuery = query.toLowerCase();
    return (
      command.title.toLowerCase().includes(searchQuery) ||
      command.subtitle?.toLowerCase().includes(searchQuery) ||
      command.keywords.some(keyword => keyword.toLowerCase().includes(searchQuery))
    );
  });

  const groupedCommands = filteredCommands.reduce((acc, command) => {
    if (!acc[command.category]) {
      acc[command.category] = [];
    }
    acc[command.category].push(command);
    return acc;
  }, {} as Record<string, Command[]>);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(prev => Math.min(prev + 1, filteredCommands.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(prev => Math.max(prev - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredCommands[selectedIndex]) {
        filteredCommands[selectedIndex].action();
        onClose();
      }
    } else if (e.key === 'Escape') {
      onClose();
    }
  };

  const handleCommandClick = (command: Command) => {
    command.action();
    onClose();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-cyber-black/80 backdrop-blur-sm z-50 flex items-start justify-center pt-[20vh]"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: -20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: -20 }}
          transition={{ type: "spring", duration: 0.3 }}
          className="w-full max-w-2xl mx-4"
          onClick={(e) => e.stopPropagation()}
          role="dialog"
          aria-modal="true"
          aria-labelledby="command-palette-title"
        >
          <div className="glass-morphism rounded-lg shadow-[0_0_50px_rgba(0,245,255,0.3)] overflow-hidden">
            {/* Search Input */}
            <div className="flex items-center gap-3 p-4 border-b border-cyber-cyan/20">
              <Search className="w-5 h-5 text-cyber-cyan/60" />
              <h2 id="command-palette-title" className="sr-only">Command Palette</h2>
              <input
                ref={inputRef}
                type="text"
                placeholder="Search commands..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                className="flex-1 bg-transparent text-cyber-cyan placeholder-cyber-cyan/50 font-mono text-lg outline-none"
                aria-label="Search commands"
              />
              <div className="flex items-center gap-1 text-cyber-cyan/40 font-mono text-xs">
                <Command className="w-3 h-3" />
                <span>K</span>
              </div>
            </div>

            {/* Commands List */}
            <div className="max-h-96 overflow-y-auto">
              {Object.keys(groupedCommands).length === 0 ? (
                <div className="p-8 text-center">
                  <Search className="w-12 h-12 text-cyber-cyan/30 mx-auto mb-4" />
                  <p className="text-cyber-cyan/60 font-mono">No commands found</p>
                  <p className="text-cyber-cyan/40 font-mono text-sm mt-2">
                    Try searching for "dashboard", "pricing", or "scan"
                  </p>
                </div>
              ) : (
                Object.entries(groupedCommands).map(([category, categoryCommands]) => (
                  <div key={category}>
                    <div className="px-4 py-2 text-cyber-cyan/60 font-mono text-xs font-semibold uppercase tracking-wider border-b border-cyber-cyan/10">
                      {category}
                    </div>
                    {categoryCommands.map((command, index) => {
                      const globalIndex = filteredCommands.indexOf(command);
                      const isSelected = globalIndex === selectedIndex;
                      const Icon = command.icon;
                      
                      return (
                        <motion.div
                          key={command.id}
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.05 }}
                          className={`
                            flex items-center gap-3 p-3 cursor-pointer transition-all duration-150
                            ${isSelected 
                              ? 'bg-cyber-cyan/10 border-r-2 border-cyber-cyan' 
                              : 'hover:bg-cyber-cyan/5'
                            }
                          `}
                          onClick={() => handleCommandClick(command)}
                        >
                          <Icon className={`w-5 h-5 ${isSelected ? 'text-cyber-cyan' : 'text-cyber-cyan/60'}`} />
                          <div className="flex-1">
                            <div className={`font-mono font-medium ${isSelected ? 'text-cyber-cyan' : 'text-cyber-cyan/80'}`}>
                              {command.title}
                            </div>
                            {command.subtitle && (
                              <div className="font-mono text-xs text-cyber-cyan/50">
                                {command.subtitle}
                              </div>
                            )}
                          </div>
                          <ArrowRight className={`w-4 h-4 ${isSelected ? 'text-cyber-cyan' : 'text-cyber-cyan/30'}`} />
                        </motion.div>
                      );
                    })}
                  </div>
                ))
              )}
            </div>

            {/* Footer */}
            <div className="px-4 py-3 border-t border-cyber-cyan/20 bg-cyber-darker/30">
              <div className="flex items-center justify-between text-cyber-cyan/40 font-mono text-xs">
                <div className="flex items-center gap-4">
                  <span>↑↓ Navigate</span>
                  <span>↵ Select</span>
                  <span>Esc Close</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  <span>{filteredCommands.length} results</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

// Hook for global command palette
export function useCommandPalette() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(prev => !prev);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return {
    isOpen,
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
    toggle: () => setIsOpen(prev => !prev)
  };
}
