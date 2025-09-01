import React from 'react'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe, toHaveNoViolations } from 'jest-axe'
import CommandPalette, { useCommandPalette } from '@/components/ui/CommandPalette'

expect.extend(toHaveNoViolations)

// Mock useRouter
const mockPush = jest.fn()
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}))

describe('CommandPalette', () => {
  beforeEach(() => {
    mockPush.mockClear()
  })

  it('renders when open', () => {
    render(<CommandPalette isOpen={true} onClose={jest.fn()} />)
    expect(screen.getByPlaceholderText('Search commands...')).toBeInTheDocument()
  })

  it('does not render when closed', () => {
    render(<CommandPalette isOpen={false} onClose={jest.fn()} />)
    expect(screen.queryByPlaceholderText('Search commands...')).not.toBeInTheDocument()
  })

  it('calls onClose when escape is pressed', async () => {
    const onClose = jest.fn()
    render(<CommandPalette isOpen={true} onClose={onClose} />)
    
    const input = screen.getByPlaceholderText('Search commands...')
    fireEvent.keyDown(input, { key: 'Escape' })
    
    expect(onClose).toHaveBeenCalled()
  })

  it('calls onClose when backdrop is clicked', async () => {
    const onClose = jest.fn()
    render(<CommandPalette isOpen={true} onClose={onClose} />)
    
    const backdrop = screen.getByRole('dialog').parentElement
    fireEvent.click(backdrop!)
    
    expect(onClose).toHaveBeenCalled()
  })

  it('filters commands based on search query', async () => {
    const user = userEvent.setup()
    render(<CommandPalette isOpen={true} onClose={jest.fn()} />)
    
    const input = screen.getByPlaceholderText('Search commands...')
    await act(async () => {
      await user.type(input, 'dashboard')
    })
    
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
    expect(screen.queryByText('Pricing Calculator')).not.toBeInTheDocument()
  })

  it('navigates with arrow keys', async () => {
    render(<CommandPalette isOpen={true} onClose={jest.fn()} />)
    
    const input = screen.getByPlaceholderText('Search commands...')
    fireEvent.keyDown(input, { key: 'ArrowDown' })
    fireEvent.keyDown(input, { key: 'ArrowUp' })
    
    // Should not throw errors
    expect(input).toBeInTheDocument()
  })

  it('executes command on enter', async () => {
    const onClose = jest.fn()
    render(<CommandPalette isOpen={true} onClose={onClose} />)
    
    const input = screen.getByPlaceholderText('Search commands...')
    fireEvent.keyDown(input, { key: 'Enter' })
    
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalled()
      expect(onClose).toHaveBeenCalled()
    })
  })

  it('executes command on click', async () => {
    const onClose = jest.fn()
    render(<CommandPalette isOpen={true} onClose={onClose} />)
    
    const dashboardCommand = screen.getByText('Dashboard')
    fireEvent.click(dashboardCommand)
    
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/dashboard')
      expect(onClose).toHaveBeenCalled()
    })
  })

  it('shows no results message when no commands match', async () => {
    const user = userEvent.setup()
    render(<CommandPalette isOpen={true} onClose={jest.fn()} />)
    
    const input = screen.getByPlaceholderText('Search commands...')
    await user.type(input, 'nonexistent')
    
    expect(screen.getByText('No commands found')).toBeInTheDocument()
  })

  it('groups commands by category', () => {
    render(<CommandPalette isOpen={true} onClose={jest.fn()} />)
    
    expect(screen.getByText('Navigation')).toBeInTheDocument()
    expect(screen.getByText('Actions')).toBeInTheDocument()
  })

  it('should have no accessibility violations', async () => {
    const { container } = render(<CommandPalette isOpen={true} onClose={jest.fn()} />)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})

describe('useCommandPalette hook', () => {
  const TestComponent = () => {
    const { isOpen, open, close, toggle } = useCommandPalette()
    return (
      <div>
        <div data-testid="is-open">{isOpen.toString()}</div>
        <button onClick={open} data-testid="open">Open</button>
        <button onClick={close} data-testid="close">Close</button>
        <button onClick={toggle} data-testid="toggle">Toggle</button>
      </div>
    )
  }

  it('manages command palette state', async () => {
    const user = userEvent.setup()
    render(<TestComponent />)
    
    expect(screen.getByTestId('is-open')).toHaveTextContent('false')
    
    await user.click(screen.getByTestId('open'))
    expect(screen.getByTestId('is-open')).toHaveTextContent('true')
    
    await user.click(screen.getByTestId('close'))
    expect(screen.getByTestId('is-open')).toHaveTextContent('false')
    
    await user.click(screen.getByTestId('toggle'))
    expect(screen.getByTestId('is-open')).toHaveTextContent('true')
  })

  it('responds to Cmd+K keyboard shortcut', async () => {
    render(<TestComponent />)
    
    expect(screen.getByTestId('is-open')).toHaveTextContent('false')
    
    fireEvent.keyDown(document, { key: 'k', metaKey: true })
    expect(screen.getByTestId('is-open')).toHaveTextContent('true')
    
    fireEvent.keyDown(document, { key: 'k', metaKey: true })
    expect(screen.getByTestId('is-open')).toHaveTextContent('false')
  })

  it('responds to Ctrl+K keyboard shortcut', async () => {
    render(<TestComponent />)
    
    expect(screen.getByTestId('is-open')).toHaveTextContent('false')
    
    fireEvent.keyDown(document, { key: 'k', ctrlKey: true })
    expect(screen.getByTestId('is-open')).toHaveTextContent('true')
  })
})
