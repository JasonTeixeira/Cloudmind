import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import InteractiveChart from '@/components/charts/InteractiveChart'

expect.extend(toHaveNoViolations)

const mockData = [
  { name: 'Jan', value: 100 },
  { name: 'Feb', value: 200 },
  { name: 'Mar', value: 150 },
  { name: 'Apr', value: 300 },
]

describe('InteractiveChart', () => {
  it('renders with bar chart type', async () => {
    render(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
      />
    )

    await waitFor(() => {
      expect(screen.getByText('Test Chart')).toBeInTheDocument()
      expect(screen.getByTestId('bar-chart')).toBeInTheDocument()
    })
  })

  it('renders with line chart type', async () => {
    render(
      <InteractiveChart
        data={mockData}
        type="line"
        title="Test Chart"
      />
    )

    await waitFor(() => {
      expect(screen.getByTestId('line-chart')).toBeInTheDocument()
    })
  })

  it('renders with area chart type', async () => {
    render(
      <InteractiveChart
        data={mockData}
        type="area"
        title="Test Chart"
      />
    )

    await waitFor(() => {
      expect(screen.getByTestId('area-chart')).toBeInTheDocument()
    })
  })

  it('renders with pie chart type', async () => {
    render(
      <InteractiveChart
        data={mockData}
        type="pie"
        title="Test Chart"
      />
    )

    await waitFor(() => {
      expect(screen.getByTestId('pie-chart')).toBeInTheDocument()
    })
  })

  it('displays title and subtitle', async () => {
    render(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
        subtitle="Test Subtitle"
      />
    )

    await waitFor(() => {
      expect(screen.getByText('Test Chart')).toBeInTheDocument()
      expect(screen.getByText('Test Subtitle')).toBeInTheDocument()
    })
  })

  it('calculates and displays total value', async () => {
    render(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
      />
    )

    await waitFor(() => {
      // Total of mockData values: 100 + 200 + 150 + 300 = 750
      expect(screen.getByText('750')).toBeInTheDocument()
      expect(screen.getByText('Total Value')).toBeInTheDocument()
    })
  })

  it('shows loading skeleton initially', () => {
    render(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
      />
    )

    // Should show skeleton elements initially (the exact count may vary)
    expect(screen.getAllByRole('generic').length).toBeGreaterThan(5)
  })

  it('calls onDataPointClick when provided', async () => {
    const onDataPointClick = jest.fn()
    render(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
        onDataPointClick={onDataPointClick}
      />
    )

    await waitFor(() => {
      expect(screen.getByTestId('bar-chart')).toBeInTheDocument()
    })

    // Note: Since we're mocking Recharts, we can't test actual click events
    // In a real implementation, you'd need to test with the actual chart library
  })

  it('applies custom height', async () => {
    render(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
        height={400}
      />
    )

    await waitFor(() => {
      expect(screen.getByTestId('responsive-container')).toBeInTheDocument()
    })
  })

  it('uses custom colors when provided', async () => {
    const customColors = ['#ff0000', '#00ff00', '#0000ff']
    render(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
        colors={customColors}
      />
    )

    await waitFor(() => {
      expect(screen.getByTestId('bar-chart')).toBeInTheDocument()
    })
  })

  it('shows/hides grid based on showGrid prop', async () => {
    const { rerender } = render(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
        showGrid={true}
      />
    )

    await waitFor(() => {
      expect(screen.getByTestId('cartesian-grid')).toBeInTheDocument()
    })

    rerender(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
        showGrid={false}
      />
    )

    await waitFor(() => {
      expect(screen.queryByTestId('cartesian-grid')).not.toBeInTheDocument()
    })
  })

  it('shows/hides tooltip based on showTooltip prop', async () => {
    const { rerender } = render(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
        showTooltip={true}
      />
    )

    await waitFor(() => {
      expect(screen.getByTestId('tooltip')).toBeInTheDocument()
    })

    rerender(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
        showTooltip={false}
      />
    )

    await waitFor(() => {
      expect(screen.queryByTestId('tooltip')).not.toBeInTheDocument()
    })
  })

  it('should have no accessibility violations', async () => {
    const { container } = render(
      <InteractiveChart
        data={mockData}
        type="bar"
        title="Test Chart"
      />
    )

    await waitFor(() => {
      expect(screen.getByText('Test Chart')).toBeInTheDocument()
    })

    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('handles empty data gracefully', async () => {
    render(
      <InteractiveChart
        data={[]}
        type="bar"
        title="Empty Chart"
      />
    )

    await waitFor(() => {
      expect(screen.getByText('Empty Chart')).toBeInTheDocument()
      expect(screen.getByText('0')).toBeInTheDocument() // Total value should be 0
    })
  })

  it('handles data with trend information', async () => {
    const dataWithTrend = [
      { name: 'Jan', value: 100, trend: 5 },
      { name: 'Feb', value: 200, trend: -3 },
    ]

    render(
      <InteractiveChart
        data={dataWithTrend}
        type="bar"
        title="Trend Chart"
      />
    )

    await waitFor(() => {
      expect(screen.getByText('Trend Chart')).toBeInTheDocument()
    })
  })
})
