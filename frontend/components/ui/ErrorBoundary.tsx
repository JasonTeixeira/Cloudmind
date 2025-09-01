'use client'

import React, { Component, ErrorInfo, ReactNode } from 'react'
import { AlertTriangle, RefreshCw, Home, ArrowLeft } from 'lucide-react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
  onError?: (error: Error, errorInfo: ErrorInfo) => void
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
  errorId: string | null
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
      errorId: null
    }
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
      errorId: Date.now().toString()
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({
      error,
      errorInfo
    })

    // Log error to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('Error caught by boundary:', error, errorInfo)
    }

    // Call onError callback if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo)
    }

    // In production, you would send this to your error reporting service
    // Example: Sentry.captureException(error, { extra: errorInfo })
  }

  handleRetry = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
      errorId: null
    })
  }

  handleGoHome = () => {
    window.location.href = '/'
  }

  handleGoBack = () => {
    window.history.back()
  }

  render() {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback
      }

      // Default error UI
      return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center p-4">
          <div className="max-w-md w-full">
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
              {/* Error Icon */}
              <div className="flex justify-center mb-6">
                <div className="p-4 bg-red-100 rounded-full">
                  <AlertTriangle className="h-8 w-8 text-red-600" />
                </div>
              </div>

              {/* Error Message */}
              <div className="text-center mb-6">
                <h1 className="text-2xl font-bold text-gray-900 mb-2">
                  Something went wrong
                </h1>
                <p className="text-gray-600 mb-4">
                  We encountered an unexpected error. Our team has been notified and is working to fix it.
                </p>
                
                {process.env.NODE_ENV === 'development' && this.state.error && (
                  <details className="text-left bg-gray-50 rounded-lg p-4 mb-4">
                    <summary className="cursor-pointer font-medium text-gray-700 mb-2">
                      Error Details (Development)
                    </summary>
                    <div className="text-sm text-gray-600 space-y-2">
                      <div>
                        <strong>Error:</strong> {this.state.error.message}
                      </div>
                      {this.state.errorInfo && (
                        <div>
                          <strong>Component Stack:</strong>
                          <pre className="mt-1 text-xs bg-gray-100 p-2 rounded overflow-auto">
                            {this.state.errorInfo.componentStack}
                          </pre>
                        </div>
                      )}
                      <div>
                        <strong>Error ID:</strong> {this.state.errorId}
                      </div>
                    </div>
                  </details>
                )}
              </div>

              {/* Action Buttons */}
              <div className="space-y-3">
                <button
                  onClick={this.handleRetry}
                  className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200 flex items-center justify-center"
                >
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Try Again
                </button>
                
                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={this.handleGoBack}
                    className="bg-gray-100 text-gray-700 py-3 px-4 rounded-lg font-medium hover:bg-gray-200 transition-colors duration-200 flex items-center justify-center"
                  >
                    <ArrowLeft className="h-4 w-4 mr-2" />
                    Go Back
                  </button>
                  
                  <button
                    onClick={this.handleGoHome}
                    className="bg-gray-100 text-gray-700 py-3 px-4 rounded-lg font-medium hover:bg-gray-200 transition-colors duration-200 flex items-center justify-center"
                  >
                    <Home className="h-4 w-4 mr-2" />
                    Go Home
                  </button>
                </div>
              </div>

              {/* Support Information */}
              <div className="mt-6 pt-6 border-t border-gray-200 text-center">
                <p className="text-sm text-gray-500">
                  If this problem persists, please contact our support team.
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  Error ID: {this.state.errorId}
                </p>
              </div>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

// Hook for functional components
export const useErrorHandler = () => {
  const [error, setError] = React.useState<Error | null>(null)

  const handleError = React.useCallback((error: Error) => {
    setError(error)
    
    // Log error
    console.error('Error caught by hook:', error)
    
    // In production, send to error reporting service
    // Example: Sentry.captureException(error)
  }, [])

  const clearError = React.useCallback(() => {
    setError(null)
  }, [])

  return { error, handleError, clearError }
}

// Higher-order component for error handling
export const withErrorBoundary = <P extends object>(
  Component: React.ComponentType<P>,
  fallback?: ReactNode
) => {
  const WrappedComponent = (props: P) => (
    <ErrorBoundary fallback={fallback}>
      <Component {...props} />
    </ErrorBoundary>
  )

  WrappedComponent.displayName = `withErrorBoundary(${Component.displayName || Component.name})`

  return WrappedComponent
}

// Error boundary for specific error types
export class NetworkErrorBoundary extends ErrorBoundary {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Only handle network-related errors
    if (error.name === 'NetworkError' || error.message.includes('fetch')) {
      super.componentDidCatch(error, errorInfo)
    } else {
      // Re-throw non-network errors
      throw error
    }
  }
}

export class ValidationErrorBoundary extends ErrorBoundary {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Only handle validation errors
    if (error.name === 'ValidationError' || error.message.includes('validation')) {
      super.componentDidCatch(error, errorInfo)
    } else {
      // Re-throw non-validation errors
      throw error
    }
  }
} 