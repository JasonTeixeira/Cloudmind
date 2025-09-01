import React from 'react'
import { cn } from '@/lib/utils'

interface ProgressProps {
  value?: number
  max?: number
  className?: string
}

export const Progress: React.FC<ProgressProps> = ({ 
  value = 0, 
  max = 100, 
  className 
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100)

  return (
    <div className={cn(
      'relative h-2 w-full overflow-hidden rounded-full bg-cyber-dark/50 border border-cyber-cyan/20',
      className
    )}>
      <div
        className="h-full w-full flex-1 bg-gradient-to-r from-cyber-cyan to-cyber-purple transition-all duration-500 ease-out shadow-[0_0_10px_rgba(0,245,255,0.3)]"
        style={{
          transform: `translateX(-${100 - percentage}%)`
        }}
      />
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-pulse" />
    </div>
  )
}
