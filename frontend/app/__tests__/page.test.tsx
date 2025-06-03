import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ChatPage from '../page'

// Mock fetch globally
const mockFetch = jest.fn()
global.fetch = mockFetch

// Mock scrollIntoView since it's used in the component
const mockScrollIntoView = jest.fn()
Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', {
    value: mockScrollIntoView,
    writable: true,
})

describe('ChatPage', () => {
    beforeEach(() => {
        mockFetch.mockClear()
        mockScrollIntoView.mockClear()
        console.log = jest.fn() // Mock console.log
        console.error = jest.fn() // Mock console.error
    })

    describe('Initial Render', () => {
        it('renders the chat interface correctly', () => {
            render(<ChatPage />)

            expect(screen.getByText('Multi Agent Chat')).toBeInTheDocument()
            expect(screen.getByPlaceholderText('Ask me anything…')).toBeInTheDocument()
            expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument()
        })

        it('starts with empty chat history', () => {
            render(<ChatPage />)

            // Should not show any chat messages initially
            expect(screen.queryByText(/AI is thinking.../)).not.toBeInTheDocument()
        })

        it('has input and send button enabled initially', () => {
            render(<ChatPage />)

            const input = screen.getByPlaceholderText('Ask me anything…')
            const sendButton = screen.getByRole('button', { name: /send/i })

            expect(input).not.toBeDisabled()
            expect(sendButton).not.toBeDisabled()
        })
    })

    describe('User Input Handling', () => {
        it('updates input value when user types', async () => {
            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')

            await userEvent.type(input, 'Hello, world!')

            expect(input).toHaveValue('Hello, world!')
        })

        it('clears input after sending message', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'Hello there!' }),
            })

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')
            const sendButton = screen.getByRole('button', { name: /send/i })

            await userEvent.type(input, 'Test message')
            await userEvent.click(sendButton)

            expect(input).toHaveValue('')
        })

        it('sends message when Enter key is pressed', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'Response' }),
            })

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')

            await userEvent.type(input, 'Test message')
            fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' })

            expect(mockFetch).toHaveBeenCalledWith(
                'http://localhost:8000/chat',
                expect.objectContaining({
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: 'Test message' }),
                })
            )
        })

        it('does not send empty or whitespace-only messages', async () => {
            render(<ChatPage />)
            const sendButton = screen.getByRole('button', { name: /send/i })

            // Try sending empty message
            await userEvent.click(sendButton)
            expect(mockFetch).not.toHaveBeenCalled()

            // Try sending whitespace-only message
            const input = screen.getByPlaceholderText('Ask me anything…')
            await userEvent.type(input, '   ')
            await userEvent.click(sendButton)
            expect(mockFetch).not.toHaveBeenCalled()
        })
    })

    describe('Chat Flow', () => {
        it('displays user message immediately (optimistic UI)', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'AI response' }),
            })

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')
            const sendButton = screen.getByRole('button', { name: /send/i })

            await userEvent.type(input, 'Hello AI')
            await userEvent.click(sendButton)

            // User message should appear immediately
            expect(screen.getByText('Hello AI')).toBeInTheDocument()
        })

        it('shows loading state while waiting for response', async () => {
            // Create a promise that we can resolve manually
            let resolvePromise: (value: any) => void
            const mockPromise = new Promise((resolve) => {
                resolvePromise = resolve
            })

            mockFetch.mockReturnValueOnce(mockPromise)

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')
            const sendButton = screen.getByRole('button', { name: /send/i })

            await userEvent.type(input, 'Test message')
            await userEvent.click(sendButton)

            // Should show loading state
            expect(screen.getByText('AI is thinking...')).toBeInTheDocument()
            expect(screen.getByText('Sending...')).toBeInTheDocument()
            expect(sendButton).toBeDisabled()

            // Resolve the promise
            resolvePromise!({
                ok: true,
                json: async () => ({ answer: 'AI response' }),
            })

            await waitFor(() => {
                expect(screen.queryByText('AI is thinking...')).not.toBeInTheDocument()
            })
        })

        it('displays AI response after successful API call', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'This is the AI response' }),
            })

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')
            const sendButton = screen.getByRole('button', { name: /send/i })

            await userEvent.type(input, 'Test message')
            await userEvent.click(sendButton)

            await waitFor(() => {
                expect(screen.getByText('This is the AI response')).toBeInTheDocument()
            })
        })

        it('prevents multiple simultaneous requests', async () => {
            // Create a long-running promise
            const mockPromise = new Promise(() => { }) // Never resolves
            mockFetch.mockReturnValueOnce(mockPromise)

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')

            await userEvent.type(input, 'First message')
            fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' })

            // Try to send another message while first is loading
            await userEvent.type(input, 'Second message')
            fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' })

            // Should only have called fetch once
            expect(mockFetch).toHaveBeenCalledTimes(1)
        })
    })

    describe('Error Handling', () => {
        it('handles network errors gracefully', async () => {
            mockFetch.mockRejectedValueOnce(new TypeError('Failed to fetch'))

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')
            const sendButton = screen.getByRole('button', { name: /send/i })

            await userEvent.type(input, 'Test message')
            await userEvent.click(sendButton)

            await waitFor(() => {
                expect(screen.getByText(/Network error: Cannot connect to backend/)).toBeInTheDocument()
            })
        })

        it('handles HTTP errors gracefully', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: false,
                status: 500,
            })

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')
            const sendButton = screen.getByRole('button', { name: /send/i })

            await userEvent.type(input, 'Test message')
            await userEvent.click(sendButton)

            await waitFor(() => {
                expect(screen.getByText(/Error: HTTP error! status: 500/)).toBeInTheDocument()
            })
        })

        it('resets loading state after error', async () => {
            mockFetch.mockRejectedValueOnce(new Error('Test error'))

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')
            const sendButton = screen.getByRole('button', { name: /send/i })

            await userEvent.type(input, 'Test message')
            await userEvent.click(sendButton)

            await waitFor(() => {
                expect(screen.queryByText('AI is thinking...')).not.toBeInTheDocument()
                expect(screen.queryByText('Sending...')).not.toBeInTheDocument()
                expect(sendButton).not.toBeDisabled()
            })
        })
    })

    describe('Auto-scroll Behavior', () => {
        it('scrolls to bottom when new messages are added', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'AI response' }),
            })

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')
            const sendButton = screen.getByRole('button', { name: /send/i })

            await userEvent.type(input, 'Test message')
            await userEvent.click(sendButton)

            // Should scroll after user message
            expect(mockScrollIntoView).toHaveBeenCalled()

            await waitFor(() => {
                expect(screen.getByText('AI response')).toBeInTheDocument()
            })

            // Should scroll again after AI response
            expect(mockScrollIntoView).toHaveBeenCalledTimes(2)
        })
    })

    describe('API Configuration', () => {
        it('uses correct API URL from environment', async () => {
            mockFetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ answer: 'Response' }),
            })

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')
            const sendButton = screen.getByRole('button', { name: /send/i })

            await userEvent.type(input, 'Test')
            await userEvent.click(sendButton)

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

            render(<ChatPage />)
            const input = screen.getByPlaceholderText('Ask me anything…')
            const sendButton = screen.getByRole('button', { name: /send/i })

            await userEvent.type(input, 'Test')
            await userEvent.click(sendButton)

            expect(console.log).toHaveBeenCalledWith('API Configuration:')
            expect(console.log).toHaveBeenCalledWith('- NEXT_PUBLIC_API_URL:', 'http://localhost:8000')
        })
    })
}) 