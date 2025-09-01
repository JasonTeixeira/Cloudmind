import React from 'react'
import { cn } from '@/lib/utils'

interface AlertProps {
  variant?: 'default' | 'destructive' | 'warning' | 'success'
  children: React.ReactNode
  className?: string
}

interface AlertDescriptionProps {
  children: React.ReactNode
  className?: string
}

interface AlertTitleProps {
  children: React.ReactNode
  className?: string
}

const alertVariants = {
  default: 'border-cyber-cyan/30 bg-cyber-cyan/10 text-cyber-cyan',
  destructive: 'border-cyber-pink/30 bg-cyber-pink/10 text-cyber-pink',
  warning: 'border-yellow-500/30 bg-yellow-500/10 text-yellow-400',
  success: 'border-green-500/30 bg-green-500/10 text-green-400'
}

export const Alert: React.FC<AlertProps> = ({ 
  variant = 'default', 
  children, 
  className 
}) => {
  return (
    <div className={cn(
      'relative w-full rounded-lg border px-4 py-3 text-sm cyber-card',
      alertVariants[variant],
      className
    )}>
      {children}
    </div>
  )
}

export const AlertTitle: React.FC<AlertTitleProps> = ({ children, className }) => {
  return (
    <h5 className={cn('mb-1 font-medium leading-none tracking-tight font-mono', className)}>
      {children}
    </h5>
  )
}

export const AlertDescription: React.FC<AlertDescriptionProps> = ({ children, className }) => {
  return (
    <div className={cn('text-sm opacity-90 font-mono', className)}>
      {children}
    </div>
  )
}
