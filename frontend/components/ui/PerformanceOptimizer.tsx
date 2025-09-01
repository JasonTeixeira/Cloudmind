'use client'

import React, { Suspense, lazy, useEffect, useState } from 'react'
import { Loader2 } from 'lucide-react'

// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'))
const DataTable = lazy(() => import('./DataTable'))
const AnalyticsDashboard = lazy(() => import('./AnalyticsDashboard'))

interface PerformanceOptimizerProps {
  children: React.ReactNode
  fallback?: React.ReactNode
  preload?: boolean
  threshold?: number
}

// Intersection Observer for lazy loading
const useIntersectionObserver = (threshold = 0.1) => {
  const [isIntersecting, setIsIntersecting] = useState(false)
  const [ref, setRef] = useState<HTMLElement | null>(null)

  useEffect(() => {
    if (!ref) return

    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsIntersecting(entry.isIntersecting)
      },
      { threshold }
    )

    observer.observe(ref)

    return () => {
      observer.disconnect()
    }
  }, [ref, threshold])

  return [setRef, isIntersecting] as const
}

// Loading fallback component
const LoadingFallback: React.FC<{ message?: string }> = ({ message = 'Loading...' }) => (
  <div className="flex items-center justify-center p-8">
    <div className="flex items-center space-x-2">
      <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
      <span className="text-gray-600">{message}</span>
    </div>
  </div>
)

// Performance optimized component wrapper
export const PerformanceOptimizer: React.FC<PerformanceOptimizerProps> = ({
  children,
  fallback = <LoadingFallback />,
  preload = false,
  threshold = 0.1
}) => {
  const [ref, isIntersecting] = useIntersectionObserver(threshold)
  const [shouldLoad, setShouldLoad] = useState(preload)

  useEffect(() => {
    if (isIntersecting && !shouldLoad) {
      setShouldLoad(true)
    }
  }, [isIntersecting, shouldLoad])

  if (!shouldLoad) {
    return <div ref={ref} className="min-h-[200px]" />
  }

  return (
    <Suspense fallback={fallback}>
      <div ref={ref}>
        {children}
      </div>
    </Suspense>
  )
}

// Lazy loaded chart component
export const LazyChart: React.FC<{ data: any[]; type: string }> = ({ data, type }) => (
  <PerformanceOptimizer>
    <HeavyChart data={data} type={type} />
  </PerformanceOptimizer>
)

// Lazy loaded data table
export const LazyDataTable: React.FC<{ data: any[]; columns: string[] }> = ({ data, columns }) => (
  <PerformanceOptimizer>
    <DataTable data={data} columns={columns} />
  </PerformanceOptimizer>
)

// Lazy loaded analytics dashboard
export const LazyAnalyticsDashboard: React.FC<{ metrics: any[] }> = ({ metrics }) => (
  <PerformanceOptimizer>
    <AnalyticsDashboard metrics={metrics} />
  </PerformanceOptimizer>
)

// Bundle size analyzer
export const useBundleAnalyzer = () => {
  const [bundleSize, setBundleSize] = useState<number>(0)
  const [loadTime, setLoadTime] = useState<number>(0)

  useEffect(() => {
    // Measure initial load time
    const startTime = performance.now()
    
    window.addEventListener('load', () => {
      const endTime = performance.now()
      setLoadTime(endTime - startTime)
    })

    // Estimate bundle size (in production, you'd get this from webpack stats)
    if (process.env.NODE_ENV === 'development') {
      // Simulate bundle size measurement
      setBundleSize(Math.random() * 1000 + 500) // 500-1500KB
    }
  }, [])

  return { bundleSize, loadTime }
}

// Performance monitoring hook
export const usePerformanceMonitor = () => {
  const [metrics, setMetrics] = useState({
    fps: 0,
    memory: 0,
    cpu: 0
  })

  useEffect(() => {
    let frameCount = 0
    let lastTime = performance.now()

    const measurePerformance = () => {
      const currentTime = performance.now()
      frameCount++

      if (currentTime - lastTime >= 1000) {
        const fps = Math.round((frameCount * 1000) / (currentTime - lastTime))
        
        setMetrics(prev => ({
          ...prev,
          fps,
          memory: (performance as any).memory?.usedJSHeapSize / 1024 / 1024 || 0,
          cpu: Math.random() * 100 // Simulated CPU usage
        }))

        frameCount = 0
        lastTime = currentTime
      }

      requestAnimationFrame(measurePerformance)
    }

    requestAnimationFrame(measurePerformance)
  }, [])

  return metrics
}

// Code splitting utility
export const withCodeSplitting = <P extends object>(
  Component: React.ComponentType<P>,
  chunkName?: string
) => {
  const LazyComponent = lazy(() => 
    import(`../${Component.name}`).then(module => ({
      default: module.default || module[Component.name]
    }))
  )

  const WrappedComponent = (props: P) => (
    <Suspense fallback={<LoadingFallback message={`Loading ${Component.name}...`} />}>
      <LazyComponent {...props} />
    </Suspense>
  )

  WrappedComponent.displayName = `withCodeSplitting(${Component.displayName || Component.name})`

  return WrappedComponent
}

// Virtual scrolling for large lists
export const VirtualList: React.FC<{
  items: any[]
  itemHeight: number
  containerHeight: number
  renderItem: (item: any, index: number) => React.ReactNode
}> = ({ items, itemHeight, containerHeight, renderItem }) => {
  const [scrollTop, setScrollTop] = useState(0)
  const [containerRef, setContainerRef] = useState<HTMLDivElement | null>(null)

  const visibleItemCount = Math.ceil(containerHeight / itemHeight)
  const startIndex = Math.floor(scrollTop / itemHeight)
  const endIndex = Math.min(startIndex + visibleItemCount + 1, items.length)

  const visibleItems = items.slice(startIndex, endIndex)
  const totalHeight = items.length * itemHeight
  const offsetY = startIndex * itemHeight

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop)
  }

  return (
    <div
      ref={setContainerRef}
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={handleScroll}
    >
      <div style={{ height: totalHeight, position: 'relative' }}>
        <div style={{ transform: `translateY(${offsetY}px)` }}>
          {visibleItems.map((item, index) => 
            renderItem(item, startIndex + index)
          )}
        </div>
      </div>
    </div>
  )
}

// Image optimization component
export const OptimizedImage: React.FC<{
  src: string
  alt: string
  width?: number
  height?: number
  priority?: boolean
}> = ({ src, alt, width, height, priority = false }) => {
  const [isLoaded, setIsLoaded] = useState(false)
  const [error, setError] = useState(false)

  const handleLoad = () => setIsLoaded(true)
  const handleError = () => setError(true)

  if (error) {
    return (
      <div className="bg-gray-200 flex items-center justify-center">
        <span className="text-gray-500 text-sm">Failed to load image</span>
      </div>
    )
  }

  return (
    <div className="relative">
      {!isLoaded && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse" />
      )}
      <img
        src={src}
        alt={alt}
        width={width}
        height={height}
        loading={priority ? 'eager' : 'lazy'}
        onLoad={handleLoad}
        onError={handleError}
        className={`transition-opacity duration-300 ${
          isLoaded ? 'opacity-100' : 'opacity-0'
        }`}
      />
    </div>
  )
}

// Debounced search hook
export const useDebouncedSearch = (delay: number = 300) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState('')

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearchTerm(searchTerm)
    }, delay)

    return () => clearTimeout(timer)
  }, [searchTerm, delay])

  return { searchTerm, setSearchTerm, debouncedSearchTerm }
}

// Memoized component wrapper
export const withMemo = <P extends object>(
  Component: React.ComponentType<P>,
  propsAreEqual?: (prevProps: P, nextProps: P) => boolean
) => {
  return React.memo(Component, propsAreEqual)
}

// Performance context
interface PerformanceContextType {
  isLowEndDevice: boolean
  shouldReduceMotion: boolean
  enableOptimizations: boolean
}

const PerformanceContext = React.createContext<PerformanceContextType>({
  isLowEndDevice: false,
  shouldReduceMotion: false,
  enableOptimizations: true
})

export const PerformanceProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [performanceConfig, setPerformanceConfig] = useState<PerformanceContextType>({
    isLowEndDevice: false,
    shouldReduceMotion: false,
    enableOptimizations: true
  })

  useEffect(() => {
    // Detect device capabilities
    const isLowEndDevice = navigator.hardwareConcurrency <= 4
    const shouldReduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    setPerformanceConfig({
      isLowEndDevice,
      shouldReduceMotion,
      enableOptimizations: true
    })
  }, [])

  return (
    <PerformanceContext.Provider value={performanceConfig}>
      {children}
    </PerformanceContext.Provider>
  )
}

export const usePerformance = () => React.useContext(PerformanceContext) 