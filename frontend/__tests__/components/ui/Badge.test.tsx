import React from 'react'
import { render, screen } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { Badge } from '@/components/ui/badge'

expect.extend(toHaveNoViolations)

describe('Badge', () => {
  it('renders with default props', () => {
    render(<Badge>Default Badge</Badge>)
    const badge = screen.getByText('Default Badge')
    expect(badge).toBeInTheDocument()
    expect(badge).toHaveClass('cyber-badge')
  })

  it('renders with different variants', () => {
    const { rerender } = render(<Badge variant="default">Default</Badge>)
    expect(screen.getByText('Default')).toHaveClass('bg-cyber-cyan/20', 'text-cyber-cyan')

    rerender(<Badge variant="secondary">Secondary</Badge>)
    expect(screen.getByText('Secondary')).toHaveClass('bg-cyber-purple/20', 'text-cyber-purple')

    rerender(<Badge variant="destructive">Destructive</Badge>)
    expect(screen.getByText('Destructive')).toHaveClass('bg-cyber-pink/20', 'text-cyber-pink')

    rerender(<Badge variant="outline">Outline</Badge>)
    expect(screen.getByText('Outline')).toHaveClass('border-cyber-cyan/30', 'text-cyber-cyan')
  })

  it('applies custom className', () => {
    render(<Badge className="custom-class">Badge</Badge>)
    const badge = screen.getByText('Badge')
    expect(badge).toHaveClass('custom-class')
  })

  it('renders children correctly', () => {
    render(
      <Badge>
        <span>Complex</span> Badge
      </Badge>
    )
    expect(screen.getByText('Complex')).toBeInTheDocument()
    expect(screen.getByText('Badge')).toBeInTheDocument()
  })

  it('should have no accessibility violations', async () => {
    const { container } = render(<Badge>Accessible Badge</Badge>)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
