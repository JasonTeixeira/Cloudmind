/// <reference types="cypress" />

describe('CloudMind Comprehensive E2E Tests', () => {
  beforeEach(() => {
    // Visit the application
    cy.visit('/')
    
    // Wait for the app to load
    cy.get('[data-testid="app-container"]', { timeout: 10000 }).should('be.visible')
  })

  describe('Authentication & User Management', () => {
    it('should allow user registration with valid data', () => {
      cy.visit('/register')
      
      // Fill registration form
      cy.get('[data-testid="email-input"]').type('test@cloudmind.com')
      cy.get('[data-testid="username-input"]').type('testuser')
      cy.get('[data-testid="password-input"]').type('SecurePass123!')
      cy.get('[data-testid="confirm-password-input"]').type('SecurePass123!')
      
      // Submit form
      cy.get('[data-testid="register-button"]').click()
      
      // Verify success
      cy.url().should('include', '/dashboard')
      cy.get('[data-testid="user-menu"]').should('be.visible')
    })

    it('should allow user login with valid credentials', () => {
      cy.visit('/login')
      
      // Fill login form
      cy.get('[data-testid="email-input"]').type('test@cloudmind.com')
      cy.get('[data-testid="password-input"]').type('SecurePass123!')
      
      // Submit form
      cy.get('[data-testid="login-button"]').click()
      
      // Verify success
      cy.url().should('include', '/dashboard')
      cy.get('[data-testid="user-menu"]').should('be.visible')
    })

    it('should handle invalid login credentials', () => {
      cy.visit('/login')
      
      // Fill with invalid credentials
      cy.get('[data-testid="email-input"]').type('invalid@test.com')
      cy.get('[data-testid="password-input"]').type('wrongpassword')
      
      // Submit form
      cy.get('[data-testid="login-button"]').click()
      
      // Verify error message
      cy.get('[data-testid="error-message"]').should('be.visible')
      cy.get('[data-testid="error-message"]').should('contain', 'Invalid credentials')
    })

    it('should allow user logout', () => {
      // Login first
      cy.login('test@cloudmind.com', 'SecurePass123!')
      
      // Open user menu
      cy.get('[data-testid="user-menu"]').click()
      
      // Click logout
      cy.get('[data-testid="logout-button"]').click()
      
      // Verify redirect to login
      cy.url().should('include', '/login')
    })

    it('should handle password reset flow', () => {
      cy.visit('/forgot-password')
      
      // Enter email
      cy.get('[data-testid="email-input"]').type('test@cloudmind.com')
      cy.get('[data-testid="reset-button"]').click()
      
      // Verify success message
      cy.get('[data-testid="success-message"]').should('be.visible')
      cy.get('[data-testid="success-message"]').should('contain', 'Reset email sent')
    })
  })

  describe('Dashboard & Navigation', () => {
    beforeEach(() => {
      cy.login('test@cloudmind.com', 'SecurePass123!')
    })

    it('should display main dashboard with key metrics', () => {
      cy.visit('/dashboard')
      
      // Check for key dashboard elements
      cy.get('[data-testid="total-cost"]').should('be.visible')
      cy.get('[data-testid="security-score"]').should('be.visible')
      cy.get('[data-testid="active-projects"]').should('be.visible')
      cy.get('[data-testid="system-health"]').should('be.visible')
      
      // Verify metrics have values
      cy.get('[data-testid="total-cost"]').should('not.be.empty')
      cy.get('[data-testid="security-score"]').should('not.be.empty')
    })

    it('should navigate between different sections', () => {
      // Test navigation to cost analysis
      cy.get('[data-testid="nav-cost-analysis"]').click()
      cy.url().should('include', '/cost-analysis')
      cy.get('[data-testid="cost-analysis-page"]').should('be.visible')
      
      // Test navigation to security
      cy.get('[data-testid="nav-security"]').click()
      cy.url().should('include', '/security')
      cy.get('[data-testid="security-page"]').should('be.visible')
      
      // Test navigation to infrastructure
      cy.get('[data-testid="nav-infrastructure"]').click()
      cy.url().should('include', '/infrastructure')
      cy.get('[data-testid="infrastructure-page"]').should('be.visible')
      
      // Test navigation to monitoring
      cy.get('[data-testid="nav-monitoring"]').click()
      cy.url().should('include', '/monitoring')
      cy.get('[data-testid="monitoring-page"]').should('be.visible')
    })

    it('should display real-time updates via WebSocket', () => {
      cy.visit('/dashboard')
      
      // Wait for WebSocket connection
      cy.window().then((win) => {
        expect(win.websocket).to.exist
      })
      
      // Check for real-time indicators
      cy.get('[data-testid="realtime-indicator"]').should('be.visible')
    })
  })

  describe('Cost Analysis & Optimization', () => {
    beforeEach(() => {
      cy.login('test@cloudmind.com', 'SecurePass123!')
      cy.visit('/cost-analysis')
    })

    it('should display cost breakdown and trends', () => {
      // Check for cost breakdown chart
      cy.get('[data-testid="cost-breakdown-chart"]').should('be.visible')
      
      // Check for cost trends
      cy.get('[data-testid="cost-trends-chart"]').should('be.visible')
      
      // Verify cost categories are displayed
      cy.get('[data-testid="cost-category"]').should('have.length.at.least', 3)
    })

    it('should generate cost optimization recommendations', () => {
      // Click generate recommendations button
      cy.get('[data-testid="generate-recommendations"]').click()
      
      // Wait for recommendations to load
      cy.get('[data-testid="recommendation-item"]', { timeout: 10000 }).should('be.visible')
      
      // Verify recommendation content
      cy.get('[data-testid="recommendation-item"]').should('have.length.at.least', 1)
      cy.get('[data-testid="savings-amount"]').should('be.visible')
    })

    it('should allow cost analysis filtering', () => {
      // Test date range filter
      cy.get('[data-testid="date-range-picker"]').click()
      cy.get('[data-testid="last-30-days"]').click()
      
      // Verify filtered results
      cy.get('[data-testid="cost-data"]').should('be.visible')
      
      // Test cloud provider filter
      cy.get('[data-testid="provider-filter"]').click()
      cy.get('[data-testid="aws-filter"]').click()
      
      // Verify filtered results
      cy.get('[data-testid="cost-data"]').should('be.visible')
    })

    it('should export cost reports', () => {
      // Click export button
      cy.get('[data-testid="export-report"]').click()
      
      // Select export format
      cy.get('[data-testid="export-pdf"]').click()
      
      // Verify download started
      cy.readFile('cypress/downloads/cost-report.pdf').should('exist')
    })
  })

  describe('Security & Compliance', () => {
    beforeEach(() => {
      cy.login('test@cloudmind.com', 'SecurePass123!')
      cy.visit('/security')
    })

    it('should display security overview and score', () => {
      // Check security score
      cy.get('[data-testid="security-score"]').should('be.visible')
      cy.get('[data-testid="security-score"]').should('contain.text', '%')
      
      // Check security overview
      cy.get('[data-testid="security-overview"]').should('be.visible')
      cy.get('[data-testid="vulnerabilities-count"]').should('be.visible')
      cy.get('[data-testid="compliance-status"]').should('be.visible')
    })

    it('should run security scans', () => {
      // Click run scan button
      cy.get('[data-testid="run-security-scan"]').click()
      
      // Wait for scan to start
      cy.get('[data-testid="scan-progress"]', { timeout: 10000 }).should('be.visible')
      
      // Wait for scan to complete
      cy.get('[data-testid="scan-complete"]', { timeout: 60000 }).should('be.visible')
      
      // Verify scan results
      cy.get('[data-testid="vulnerability-item"]').should('be.visible')
    })

    it('should display vulnerability details', () => {
      // Click on a vulnerability
      cy.get('[data-testid="vulnerability-item"]').first().click()
      
      // Verify vulnerability details
      cy.get('[data-testid="vulnerability-details"]').should('be.visible')
      cy.get('[data-testid="severity-level"]').should('be.visible')
      cy.get('[data-testid="remediation-steps"]').should('be.visible')
    })

    it('should generate compliance reports', () => {
      // Click generate compliance report
      cy.get('[data-testid="generate-compliance-report"]').click()
      
      // Wait for report generation
      cy.get('[data-testid="report-generated"]', { timeout: 30000 }).should('be.visible')
      
      // Verify report content
      cy.get('[data-testid="compliance-score"]').should('be.visible')
      cy.get('[data-testid="compliance-item"]').should('have.length.at.least', 1)
    })
  })

  describe('Infrastructure Management', () => {
    beforeEach(() => {
      cy.login('test@cloudmind.com', 'SecurePass123!')
      cy.visit('/infrastructure')
    })

    it('should display infrastructure overview', () => {
      // Check infrastructure overview
      cy.get('[data-testid="infrastructure-overview"]').should('be.visible')
      cy.get('[data-testid="resource-count"]').should('be.visible')
      cy.get('[data-testid="health-status"]').should('be.visible')
      
      // Verify resource types are displayed
      cy.get('[data-testid="resource-type"]').should('have.length.at.least', 3)
    })

    it('should allow resource management', () => {
      // Click on a resource
      cy.get('[data-testid="resource-item"]').first().click()
      
      // Verify resource details
      cy.get('[data-testid="resource-details"]').should('be.visible')
      cy.get('[data-testid="resource-actions"]').should('be.visible')
      
      // Test resource actions
      cy.get('[data-testid="edit-resource"]').should('be.visible')
      cy.get('[data-testid="delete-resource"]').should('be.visible')
    })

    it('should display performance metrics', () => {
      // Check performance charts
      cy.get('[data-testid="cpu-usage-chart"]').should('be.visible')
      cy.get('[data-testid="memory-usage-chart"]').should('be.visible')
      cy.get('[data-testid="network-usage-chart"]').should('be.visible')
      
      // Verify metrics have values
      cy.get('[data-testid="cpu-usage"]').should('not.be.empty')
      cy.get('[data-testid="memory-usage"]').should('not.be.empty')
    })
  })

  describe('AI & Machine Learning', () => {
    beforeEach(() => {
      cy.login('test@cloudmind.com', 'SecurePass123!')
      cy.visit('/ai-insights')
    })

    it('should display AI insights and predictions', () => {
      // Check AI insights
      cy.get('[data-testid="ai-insights"]').should('be.visible')
      cy.get('[data-testid="prediction-item"]').should('be.visible')
      
      // Verify insight content
      cy.get('[data-testid="insight-title"]').should('be.visible')
      cy.get('[data-testid="insight-confidence"]').should('be.visible')
    })

    it('should generate AI-powered recommendations', () => {
      // Click generate AI recommendations
      cy.get('[data-testid="generate-ai-recommendations"]').click()
      
      // Wait for recommendations
      cy.get('[data-testid="ai-recommendation"]', { timeout: 15000 }).should('be.visible')
      
      // Verify recommendation content
      cy.get('[data-testid="recommendation-priority"]').should('be.visible')
      cy.get('[data-testid="recommendation-impact"]').should('be.visible')
    })

    it('should display model performance metrics', () => {
      // Check model metrics
      cy.get('[data-testid="model-accuracy"]').should('be.visible')
      cy.get('[data-testid="model-precision"]').should('be.visible')
      cy.get('[data-testid="model-recall"]').should('be.visible')
      
      // Verify metrics have values
      cy.get('[data-testid="model-accuracy"]').should('not.be.empty')
    })
  })

  describe('Monitoring & Observability', () => {
    beforeEach(() => {
      cy.login('test@cloudmind.com', 'SecurePass123!')
      cy.visit('/monitoring')
    })

    it('should display real-time monitoring data', () => {
      // Check monitoring dashboard
      cy.get('[data-testid="monitoring-dashboard"]').should('be.visible')
      cy.get('[data-testid="system-metrics"]').should('be.visible')
      
      // Verify real-time updates
      cy.get('[data-testid="realtime-indicator"]').should('be.visible')
    })

    it('should display alert history', () => {
      // Check alert history
      cy.get('[data-testid="alert-history"]').should('be.visible')
      cy.get('[data-testid="alert-item"]').should('be.visible')
      
      // Verify alert details
      cy.get('[data-testid="alert-severity"]').should('be.visible')
      cy.get('[data-testid="alert-timestamp"]').should('be.visible')
    })

    it('should allow alert configuration', () => {
      // Click configure alerts
      cy.get('[data-testid="configure-alerts"]').click()
      
      // Verify alert configuration form
      cy.get('[data-testid="alert-threshold"]').should('be.visible')
      cy.get('[data-testid="alert-channel"]').should('be.visible')
      
      // Test alert configuration
      cy.get('[data-testid="cpu-threshold"]').type('80')
      cy.get('[data-testid="save-alert-config"]').click()
      
      // Verify success
      cy.get('[data-testid="alert-config-saved"]').should('be.visible')
    })
  })

  describe('Reporting & Analytics', () => {
    beforeEach(() => {
      cy.login('test@cloudmind.com', 'SecurePass123!')
      cy.visit('/reports')
    })

    it('should generate comprehensive reports', () => {
      // Click generate report
      cy.get('[data-testid="generate-report"]').click()
      
      // Select report type
      cy.get('[data-testid="comprehensive-report"]').click()
      
      // Wait for report generation
      cy.get('[data-testid="report-generated"]', { timeout: 30000 }).should('be.visible')
      
      // Verify report sections
      cy.get('[data-testid="cost-section"]').should('be.visible')
      cy.get('[data-testid="security-section"]').should('be.visible')
      cy.get('[data-testid="performance-section"]').should('be.visible')
    })

    it('should export reports in multiple formats', () => {
      // Generate a report first
      cy.get('[data-testid="generate-report"]').click()
      cy.get('[data-testid="comprehensive-report"]').click()
      cy.get('[data-testid="report-generated"]', { timeout: 30000 }).should('be.visible')
      
      // Test PDF export
      cy.get('[data-testid="export-pdf"]').click()
      cy.readFile('cypress/downloads/report.pdf').should('exist')
      
      // Test Excel export
      cy.get('[data-testid="export-excel"]').click()
      cy.readFile('cypress/downloads/report.xlsx').should('exist')
    })

    it('should display analytics dashboard', () => {
      // Check analytics dashboard
      cy.get('[data-testid="analytics-dashboard"]').should('be.visible')
      cy.get('[data-testid="trend-chart"]').should('be.visible')
      cy.get('[data-testid="comparison-chart"]').should('be.visible')
    })
  })

  describe('PWA & Offline Functionality', () => {
    it('should work offline with cached data', () => {
      // Visit the app to cache data
      cy.visit('/')
      cy.login('test@cloudmind.com', 'SecurePass123!')
      cy.visit('/dashboard')
      
      // Simulate offline mode
      cy.window().then((win) => {
        cy.stub(win.navigator, 'onLine').value(false)
      })
      
      // Reload page
      cy.reload()
      
      // Verify offline functionality
      cy.get('[data-testid="offline-indicator"]').should('be.visible')
      cy.get('[data-testid="cached-data"]').should('be.visible')
    })

    it('should sync data when coming back online', () => {
      // Simulate going online
      cy.window().then((win) => {
        cy.stub(win.navigator, 'onLine').value(true)
      })
      
      // Trigger online event
      cy.window().then((win) => {
        win.dispatchEvent(new Event('online'))
      })
      
      // Verify sync indicator
      cy.get('[data-testid="sync-indicator"]').should('be.visible')
    })
  })

  describe('Performance & Load Testing', () => {
    it('should load dashboard within performance budget', () => {
      cy.visit('/')
      cy.login('test@cloudmind.com', 'SecurePass123!')
      
      // Measure page load time
      cy.visit('/dashboard', {
        onBeforeLoad: (win) => {
          win.performance.mark('start-loading')
        }
      })
      
      cy.get('[data-testid="dashboard-loaded"]').should('be.visible').then(() => {
        cy.window().then((win) => {
          win.performance.mark('end-loading')
          win.performance.measure('dashboard-load', 'start-loading', 'end-loading')
          
          const measure = win.performance.getEntriesByName('dashboard-load')[0]
          expect(measure.duration).to.be.lessThan(3000) // 3 seconds budget
        })
      })
    })

    it('should handle large datasets efficiently', () => {
      cy.visit('/cost-analysis')
      
      // Load large dataset
      cy.get('[data-testid="load-large-dataset"]').click()
      
      // Verify data loads without performance issues
      cy.get('[data-testid="cost-data"]', { timeout: 10000 }).should('be.visible')
      cy.get('[data-testid="loading-indicator"]').should('not.exist')
    })
  })

  describe('Accessibility & Usability', () => {
    it('should meet accessibility standards', () => {
      cy.visit('/')
      cy.injectAxe()
      cy.checkA11y()
    })

    it('should be keyboard navigable', () => {
      cy.visit('/')
      cy.login('test@cloudmind.com', 'SecurePass123!')
      
      // Test keyboard navigation
      cy.get('body').tab()
      cy.focused().should('be.visible')
      
      // Navigate through main menu
      cy.get('[data-testid="nav-menu"]').focus()
      cy.get('[data-testid="nav-cost-analysis"]').focus()
      cy.get('[data-testid="nav-security"]').focus()
    })

    it('should work with screen readers', () => {
      cy.visit('/')
      
      // Check for ARIA labels
      cy.get('[aria-label]').should('exist')
      cy.get('[role]').should('exist')
      
      // Check for proper heading structure
      cy.get('h1').should('exist')
      cy.get('h2').should('exist')
    })
  })

  describe('Error Handling & Edge Cases', () => {
    it('should handle network errors gracefully', () => {
      // Intercept API calls and return errors
      cy.intercept('GET', '/api/v1/dashboard/metrics', { statusCode: 500 })
      cy.intercept('GET', '/api/v1/projects', { statusCode: 404 })
      
      cy.visit('/dashboard')
      
      // Verify error handling
      cy.get('[data-testid="error-message"]').should('be.visible')
      cy.get('[data-testid="retry-button"]').should('be.visible')
    })

    it('should handle malformed data gracefully', () => {
      // Intercept API calls and return malformed data
      cy.intercept('GET', '/api/v1/cost/analyses', { 
        body: { invalid: 'data' },
        statusCode: 200 
      })
      
      cy.visit('/cost-analysis')
      
      // Verify graceful handling
      cy.get('[data-testid="data-error"]').should('be.visible')
    })

    it('should handle concurrent user actions', () => {
      cy.visit('/dashboard')
      
      // Perform multiple actions simultaneously
      cy.get('[data-testid="refresh-data"]').click()
      cy.get('[data-testid="generate-report"]').click()
      cy.get('[data-testid="export-data"]').click()
      
      // Verify no conflicts
      cy.get('[data-testid="loading-indicator"]').should('not.exist')
    })
  })
})

// Custom commands for common operations
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/login')
  cy.get('[data-testid="email-input"]').type(email)
  cy.get('[data-testid="password-input"]').type(password)
  cy.get('[data-testid="login-button"]').click()
  cy.url().should('include', '/dashboard')
})

Cypress.Commands.add('waitForWebSocket', () => {
  cy.window().then((win) => {
    return new Cypress.Promise((resolve) => {
      if (win.websocket && win.websocket.readyState === WebSocket.OPEN) {
        resolve()
      } else {
        const checkWebSocket = () => {
          if (win.websocket && win.websocket.readyState === WebSocket.OPEN) {
            resolve()
          } else {
            setTimeout(checkWebSocket, 100)
          }
        }
        checkWebSocket()
      }
    })
  })
}) 