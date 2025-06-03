import { fireEvent, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button, buttonVariants } from '../button'

describe('Button Component', () => {
    describe('Rendering', () => {
        it('renders a button with default variant and size', () => {
            render(<Button>Click me</Button>)
            const button = screen.getByRole('button', { name: /click me/i })
            expect(button).toBeInTheDocument()
            expect(button).toHaveClass('bg-primary', 'text-primary-foreground', 'h-10', 'px-4', 'py-2')
        })

        it('renders with custom className', () => {
            render(<Button className="custom-class">Test</Button>)
            const button = screen.getByRole('button')
            expect(button).toHaveClass('custom-class')
        })

        it('renders as child component when asChild is true', () => {
            render(
                <Button asChild>
                    <a href="/test">Link Button</a>
                </Button>
            )
            const link = screen.getByRole('link')
            expect(link).toBeInTheDocument()
            expect(link).toHaveAttribute('href', '/test')
        })
    })

    describe('Variants', () => {
        it('renders destructive variant correctly', () => {
            render(<Button variant="destructive">Delete</Button>)
            const button = screen.getByRole('button')
            expect(button).toHaveClass('bg-destructive', 'text-destructive-foreground')
        })

        it('renders outline variant correctly', () => {
            render(<Button variant="outline">Outline</Button>)
            const button = screen.getByRole('button')
            expect(button).toHaveClass('border', 'border-input', 'bg-background')
        })

        it('renders secondary variant correctly', () => {
            render(<Button variant="secondary">Secondary</Button>)
            const button = screen.getByRole('button')
            expect(button).toHaveClass('bg-secondary', 'text-secondary-foreground')
        })

        it('renders ghost variant correctly', () => {
            render(<Button variant="ghost">Ghost</Button>)
            const button = screen.getByRole('button')
            expect(button).toHaveClass('hover:bg-accent', 'hover:text-accent-foreground')
        })

        it('renders link variant correctly', () => {
            render(<Button variant="link">Link</Button>)
            const button = screen.getByRole('button')
            expect(button).toHaveClass('text-primary', 'underline-offset-4', 'hover:underline')
        })
    })

    describe('Sizes', () => {
        it('renders small size correctly', () => {
            render(<Button size="sm">Small</Button>)
            const button = screen.getByRole('button')
            expect(button).toHaveClass('h-9', 'rounded-md', 'px-3')
        })

        it('renders large size correctly', () => {
            render(<Button size="lg">Large</Button>)
            const button = screen.getByRole('button')
            expect(button).toHaveClass('h-11', 'rounded-md', 'px-8')
        })

        it('renders icon size correctly', () => {
            render(<Button size="icon">Icon</Button>)
            const button = screen.getByRole('button')
            expect(button).toHaveClass('h-10', 'w-10')
        })
    })

    describe('States', () => {
        it('handles disabled state correctly', () => {
            render(<Button disabled>Disabled</Button>)
            const button = screen.getByRole('button')
            expect(button).toBeDisabled()
            expect(button).toHaveClass('disabled:pointer-events-none', 'disabled:opacity-50')
        })

        it('maintains focus styles', () => {
            render(<Button>Focus me</Button>)
            const button = screen.getByRole('button')
            expect(button).toHaveClass('focus-visible:outline-none', 'focus-visible:ring-2')
        })
    })

    describe('Interactions', () => {
        it('calls onClick handler when clicked', async () => {
            const handleClick = jest.fn()
            render(<Button onClick={handleClick}>Click me</Button>)

            const button = screen.getByRole('button')
            await userEvent.click(button)

            expect(handleClick).toHaveBeenCalledTimes(1)
        })

        it('does not call onClick when disabled', async () => {
            const handleClick = jest.fn()
            render(
                <Button onClick={handleClick} disabled>
                    Disabled
                </Button>
            )

            const button = screen.getByRole('button')
            await userEvent.click(button)

            expect(handleClick).not.toHaveBeenCalled()
        })

        it('handles keyboard events', () => {
            const handleClick = jest.fn()
            render(<Button onClick={handleClick}>Keyboard</Button>)

            const button = screen.getByRole('button')
            fireEvent.keyDown(button, { key: 'Enter', code: 'Enter' })

            expect(handleClick).toHaveBeenCalledTimes(1)
        })
    })

    describe('Button Variants Function', () => {
        it('generates correct class names for default configuration', () => {
            const classes = buttonVariants()
            expect(classes).toContain('bg-primary')
            expect(classes).toContain('h-10')
        })

        it('generates correct class names for custom variant and size', () => {
            const classes = buttonVariants({ variant: 'outline', size: 'lg' })
            expect(classes).toContain('border')
            expect(classes).toContain('h-11')
        })
    })

    describe('Accessibility', () => {
        it('has proper ARIA attributes', () => {
            render(<Button aria-label="Custom label">Button</Button>)
            const button = screen.getByRole('button')
            expect(button).toHaveAttribute('aria-label', 'Custom label')
        })

        it('supports custom ARIA attributes', () => {
            render(
                <Button aria-describedby="description" aria-pressed="false">
                    Toggle
                </Button>
            )
            const button = screen.getByRole('button')
            expect(button).toHaveAttribute('aria-describedby', 'description')
            expect(button).toHaveAttribute('aria-pressed', 'false')
        })
    })
}) 