import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ProjectSubmissionPage from '../project/page'

// Mock fetch globally
const mockFetch = jest.fn()
global.fetch = mockFetch

// Mock scrollIntoView since it's used in the component
const mockScrollIntoView = jest.fn()
Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', {
    value: mockScrollIntoView,
    writable: true,
})

// Mock next/link
jest.mock('next/link', () => {
    const MockLink = ({ children, href, ...props }: { children: React.ReactNode; href: string;[key: string]: string | React.ReactNode }) => {
        return <a href={href} {...props}>{children}</a>
    }
    MockLink.displayName = 'MockLink'
    return MockLink
})

describe('ProjectSubmissionPage', () => {
    beforeEach(() => {
        mockFetch.mockClear()
        mockScrollIntoView.mockClear()
        console.log = jest.fn() // Mock console.log
        console.error = jest.fn() // Mock console.error
    })

    describe('Initial Render', () => {
        it('renders the project submission interface correctly', () => {
            render(<ProjectSubmissionPage />)

            expect(screen.getByText('Project Submission Chat')).toBeInTheDocument()
            expect(screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')).toBeInTheDocument()
            expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument()
        })

        it('starts with empty chat history', () => {
            render(<ProjectSubmissionPage />)

            // Should not show any chat messages initially
            expect(screen.queryByText(/AI is analyzing your project requirements.../)).not.toBeInTheDocument()
        })

        it('has input and submit button enabled initially', () => {
            render(<ProjectSubmissionPage />)

            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            const submitButton = screen.getByRole('button', { name: /submit/i })

            expect(input).not.toBeDisabled()
            expect(submitButton).not.toBeDisabled()
        })

        it('shows back to home link', () => {
            render(<ProjectSubmissionPage />)

            const backLink = screen.getByText('← Back to Home')
            expect(backLink).toBeInTheDocument()
            expect(backLink.closest('a')).toHaveAttribute('href', '/')
        })
    })

    describe('User Input Handling', () => {
        it('updates input value when user types', async () => {
            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')

            await userEvent.type(input, 'I need a React developer')

            expect(input).toHaveValue('I need a React developer')
        })

        it('clears input after sending message', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'Hello there!' }),
            })

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            const submitButton = screen.getByRole('button', { name: /submit/i })

            await userEvent.type(input, 'Test project description')
            await userEvent.click(submitButton)

            expect(input).toHaveValue('')
        })

        it('sends message when Enter key is pressed', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'Response' }),
            })

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')

            await userEvent.type(input, 'Test project description')
            fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' })

            expect(mockFetch).toHaveBeenCalledWith(
                'http://localhost:8000/chat',
                expect.objectContaining({
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: 'Test project description' }),
                })
            )
        })

        it('does not send empty or whitespace-only messages', async () => {
            render(<ProjectSubmissionPage />)
            const submitButton = screen.getByRole('button', { name: /submit/i })

            // Try sending empty message
            await userEvent.click(submitButton)
            expect(mockFetch).not.toHaveBeenCalled()

            // Try sending whitespace-only message
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            await userEvent.type(input, '   ')
            await userEvent.click(submitButton)
            expect(mockFetch).not.toHaveBeenCalled()
        })
    })

    describe('Chat Flow', () => {
        it('displays user message immediately (optimistic UI)', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'AI response' }),
            })

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            const submitButton = screen.getByRole('button', { name: /submit/i })

            await userEvent.type(input, 'Need a mobile app developer')
            await userEvent.click(submitButton)

            // User message should appear immediately
            expect(screen.getByText('Need a mobile app developer')).toBeInTheDocument()
        })

        it('shows loading state while waiting for response', async () => {
            // Create a promise that we can resolve manually
            let resolvePromise: (value: { ok: boolean; json: () => Promise<{ answer: string }> }) => void
            const mockPromise = new Promise((resolve) => {
                resolvePromise = resolve
            })

            mockFetch.mockReturnValueOnce(mockPromise)

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            const submitButton = screen.getByRole('button', { name: /submit/i })

            await userEvent.type(input, 'Test project description')
            await userEvent.click(submitButton)

            // Should show loading state
            expect(screen.getByText('AI is analyzing your project requirements...')).toBeInTheDocument()
            expect(screen.getByText('Analyzing...')).toBeInTheDocument()
            expect(submitButton).toBeDisabled()

            // Resolve the promise
            resolvePromise!({
                ok: true,
                json: async () => ({ answer: 'AI response' }),
            })

            await waitFor(() => {
                expect(screen.queryByText('AI is analyzing your project requirements...')).not.toBeInTheDocument()
            })
        })

        it('displays AI response after successful API call', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'This is the AI response' }),
            })

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            const submitButton = screen.getByRole('button', { name: /submit/i })

            await userEvent.type(input, 'Test project description')
            await userEvent.click(submitButton)

            await waitFor(() => {
                expect(screen.getByText('This is the AI response')).toBeInTheDocument()
            })
        })

        it('prevents multiple simultaneous requests', async () => {
            // Create a long-running promise
            const mockPromise = new Promise(() => { }) // Never resolves
            mockFetch.mockReturnValueOnce(mockPromise)

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')

            await userEvent.type(input, 'First project description')
            fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' })

            // Try to send another message while first is loading
            await userEvent.type(input, 'Second project description')
            fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' })

            // Should only have called fetch once
            expect(mockFetch).toHaveBeenCalledTimes(1)
        })
    })

    describe('Error Handling', () => {
        it('handles network errors gracefully', async () => {
            mockFetch.mockRejectedValueOnce(new TypeError('Failed to fetch'))

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            const submitButton = screen.getByRole('button', { name: /submit/i })

            await userEvent.type(input, 'Test project description')
            await userEvent.click(submitButton)

            await waitFor(() => {
                expect(screen.getByText(/Network error: Cannot connect to backend/)).toBeInTheDocument()
            })
        })

        it('handles HTTP errors gracefully', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: false,
                status: 500,
            })

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            const submitButton = screen.getByRole('button', { name: /submit/i })

            await userEvent.type(input, 'Test project description')
            await userEvent.click(submitButton)

            await waitFor(() => {
                expect(screen.getByText(/Error: HTTP error! status: 500/)).toBeInTheDocument()
            })
        })

        it('resets loading state after error', async () => {
            mockFetch.mockRejectedValueOnce(new Error('Test error'))

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            const submitButton = screen.getByRole('button', { name: /submit/i })

            await userEvent.type(input, 'Test project description')
            await userEvent.click(submitButton)

            await waitFor(() => {
                expect(screen.queryByText('AI is analyzing your project requirements...')).not.toBeInTheDocument()
                expect(screen.queryByText('Analyzing...')).not.toBeInTheDocument()
                expect(submitButton).not.toBeDisabled()
            })
        })
    })

    describe('Auto-scroll Behavior', () => {
        it('scrolls to bottom when new messages are added', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'AI response' }),
            })

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            const submitButton = screen.getByRole('button', { name: /submit/i })

            await userEvent.type(input, 'Test project description')
            await userEvent.click(submitButton)

            // Should scroll after user message
            expect(mockScrollIntoView).toHaveBeenCalled()

            await waitFor(() => {
                expect(screen.getByText('AI response')).toBeInTheDocument()
            })

            // Should scroll again after AI response
            expect(mockScrollIntoView).toHaveBeenCalledTimes(3)
        })
    })

    describe('API Configuration', () => {
        it('uses correct API URL from environment', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'Response' }),
            })

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            const submitButton = screen.getByRole('button', { name: /submit/i })

            await userEvent.type(input, 'Test')
            await userEvent.click(submitButton)

            expect(mockFetch).toHaveBeenCalledWith(
                'http://localhost:8000/chat',
                expect.any(Object)
            )
        })

        it('logs API configuration for debugging', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'Response' }),
            })

            render(<ProjectSubmissionPage />)
            const input = screen.getByPlaceholderText('Describe your project, skills needed, timeline, budget...')
            const submitButton = screen.getByRole('button', { name: /submit/i })

            await userEvent.type(input, 'Test')
            await userEvent.click(submitButton)

            expect(console.log).toHaveBeenCalledWith('API Configuration:')
            expect(console.log).toHaveBeenCalledWith('- NEXT_PUBLIC_API_URL:', 'http://localhost:8000')
        })
    })
}) 