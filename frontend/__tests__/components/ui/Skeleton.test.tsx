import React from 'react'
import { render, screen } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { Skeleton, CardSkeleton, TableSkeleton, ChartSkeleton, DashboardSkeleton } from '@/components/ui/Skeleton'

expect.extend(toHaveNoViolations)

describe('Skeleton Components', () => {
  describe('Skeleton', () => {
    it('renders with default props', () => {
      const { container } = render(<Skeleton />)
      const skeleton = container.querySelector('.skeleton')
      expect(skeleton).toBeInTheDocument()
      expect(skeleton).toHaveClass('skeleton')
    })

    it('renders with custom className', () => {
      const { container } = render(<Skeleton className="custom-class" />)
      const skeleton = container.querySelector('.skeleton')
      expect(skeleton).toHaveClass('skeleton', 'custom-class')
    })

    it('renders with custom dimensions', () => {
      const { container } = render(<Skeleton width={100} height={50} />)
      const skeleton = container.querySelector('.skeleton')
      expect(skeleton).toHaveStyle({ width: '100px', height: '50px' })
    })

    it('renders text variant with multiple lines', () => {
      const { container } = render(<Skeleton variant="text" lines={3} />)
      const skeletons = container.querySelectorAll('.skeleton')
      expect(skeletons.length).toBeGreaterThanOrEqual(3)
    })

    it('renders circular variant', () => {
      const { container } = render(<Skeleton variant="circular" />)
      const skeleton = container.querySelector('.skeleton')
      expect(skeleton).toHaveClass('rounded-full')
    })

    it('renders card variant', () => {
      const { container } = render(<Skeleton variant="card" />)
      const skeleton = container.querySelector('.skeleton')
      expect(skeleton).toHaveClass('h-48', 'w-full', 'rounded-lg')
    })

    it('should have no accessibility violations', async () => {
      const { container } = render(<Skeleton />)
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })
  })

  describe('CardSkeleton', () => {
    it('renders card skeleton structure', () => {
      const { container } = render(<CardSkeleton />)
      const skeletons = container.querySelectorAll('.skeleton')
      expect(skeletons.length).toBeGreaterThan(0)
      expect(container.querySelector('.card-cyber')).toBeInTheDocument()
    })

    it('should have no accessibility violations', async () => {
      const { container } = render(<CardSkeleton />)
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })
  })

  describe('TableSkeleton', () => {
    it('renders table skeleton with default rows and columns', () => {
      const { container } = render(<TableSkeleton />)
      const skeletons = container.querySelectorAll('.skeleton')
      // Should have multiple skeleton elements for table structure
      expect(skeletons.length).toBeGreaterThan(10)
    })

    it('renders table skeleton with custom rows and columns', () => {
      const { container } = render(<TableSkeleton rows={3} columns={2} />)
      const skeletons = container.querySelectorAll('.skeleton')
      // Should have skeleton elements for custom table structure
      expect(skeletons.length).toBeGreaterThan(5)
    })

    it('should have no accessibility violations', async () => {
      const { container } = render(<TableSkeleton />)
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })
  })

  describe('ChartSkeleton', () => {
    it('renders chart skeleton structure', () => {
      const { container } = render(<ChartSkeleton />)
      const skeletons = container.querySelectorAll('.skeleton')
      expect(skeletons.length).toBeGreaterThan(0)
    })

    it('should have no accessibility violations', async () => {
      const { container } = render(<ChartSkeleton />)
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })
  })

  describe('DashboardSkeleton', () => {
    it('renders dashboard skeleton structure', () => {
      const { container } = render(<DashboardSkeleton />)
      const skeletons = container.querySelectorAll('.skeleton')
      expect(skeletons.length).toBeGreaterThan(0)
    })

    it('should have no accessibility violations', async () => {
      const { container } = render(<DashboardSkeleton />)
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })
  })
})