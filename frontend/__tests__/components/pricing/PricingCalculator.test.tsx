import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import PricingCalculator from '@/components/pricing/PricingCalculator'

expect.extend(toHaveNoViolations)

// Mock fetch
global.fetch = jest.fn()

describe('PricingCalculator', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear()
  })

  it('renders pricing calculator interface', () => {
    render(<PricingCalculator />)
    
    expect(screen.getByText('Tokenized Pricing Calculator')).toBeInTheDocument()
  })

  it('displays service tokens when loaded', async () => {
    render(<PricingCalculator />)

    await waitFor(() => {
      expect(screen.getByText('EC2 Instance Analysis')).toBeInTheDocument()
    }, { timeout: 3000 })
  })

  it('shows loading state initially', () => {
    render(<PricingCalculator />)
    
    // Should show some content immediately
    expect(screen.getByText('Tokenized Pricing Calculator')).toBeInTheDocument()
  })

  it('should have no accessibility violations', async () => {
    const { container } = render(<PricingCalculator />)

    await waitFor(() => {
      expect(screen.getByText('EC2 Instance Analysis')).toBeInTheDocument()
    }, { timeout: 3000 })

    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('renders with custom className', () => {
    const { container } = render(<PricingCalculator className="custom-class" />)
    
    expect(container.firstChild).toHaveClass('custom-class')
  })

  it('displays multiple service categories', async () => {
    render(<PricingCalculator />)

    await waitFor(() => {
      expect(screen.getByText('scanning')).toBeInTheDocument()
    }, { timeout: 3000 })
  })
})