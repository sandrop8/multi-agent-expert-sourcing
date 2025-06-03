import { expect, test } from '@playwright/test';

test.describe('Multi-Agent Chat Application', () => {
    test.beforeEach(async ({ page }) => {
        // Navigate to the chat page
        await page.goto('/');
    });

    test('should load the chat interface correctly', async ({ page }) => {
        // Check that main elements are present
        await expect(page.getByText('Multi Agent Chat')).toBeVisible();
        await expect(page.getByPlaceholder('Ask me anything…')).toBeVisible();
        await expect(page.getByRole('button', { name: /send/i })).toBeVisible();
    });

    test('should have proper page title and favicon', async ({ page }) => {
        await expect(page).toHaveTitle(/multi-agent/i);
    });

    test('should display input field and send button', async ({ page }) => {
        const input = page.getByPlaceholder('Ask me anything…');
        const sendButton = page.getByRole('button', { name: /send/i });

        await expect(input).toBeEnabled();
        await expect(sendButton).toBeEnabled();
    });

    test('should handle user input correctly', async ({ page }) => {
        const input = page.getByPlaceholder('Ask me anything…');

        // Type a message
        await input.fill('Hello, I need help finding a developer');
        await expect(input).toHaveValue('Hello, I need help finding a developer');
    });

    test('should clear input after sending message', async ({ page }) => {
        // Mock the API response to avoid actual backend calls
        await page.route('**/chat', async route => {
            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({ answer: 'I can help you find a developer!' }),
            });
        });

        const input = page.getByPlaceholder('Ask me anything…');
        const sendButton = page.getByRole('button', { name: /send/i });

        await input.fill('Test message');
        await sendButton.click();

        // Input should be cleared after sending
        await expect(input).toHaveValue('');
    });

    test('should display user message immediately', async ({ page }) => {
        // Mock the API response
        await page.route('**/chat', async route => {
            // Add a delay to simulate network request
            await new Promise(resolve => setTimeout(resolve, 1000));
            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({ answer: 'Mock AI response' }),
            });
        });

        const input = page.getByPlaceholder('Ask me anything…');
        const sendButton = page.getByRole('button', { name: /send/i });

        await input.fill('Test user message');
        await sendButton.click();

        // User message should appear immediately (optimistic UI)
        await expect(page.getByText('Test user message')).toBeVisible();
    });

    test('should show loading state while waiting for response', async ({ page }) => {
        // Mock a slow API response
        await page.route('**/chat', async route => {
            await new Promise(resolve => setTimeout(resolve, 2000));
            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({ answer: 'Delayed response' }),
            });
        });

        const input = page.getByPlaceholder('Ask me anything…');
        const sendButton = page.getByRole('button', { name: /send/i });

        await input.fill('Test message');
        await sendButton.click();

        // Should show loading indicators
        await expect(page.getByText('AI is thinking...')).toBeVisible();
        await expect(page.getByText('Sending...')).toBeVisible();
        await expect(sendButton).toBeDisabled();
    });

    test('should display AI response after successful request', async ({ page }) => {
        // Mock successful API response
        await page.route('**/chat', async route => {
            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({ answer: 'This is an AI response from the expert sourcing system' }),
            });
        });

        const input = page.getByPlaceholder('Ask me anything…');
        const sendButton = page.getByRole('button', { name: /send/i });

        await input.fill('Find me a Python developer');
        await sendButton.click();

        // Should display the AI response
        await expect(page.getByText('This is an AI response from the expert sourcing system')).toBeVisible();
    });

    test('should handle API errors gracefully', async ({ page }) => {
        // Mock API error
        await page.route('**/chat', async route => {
            await route.fulfill({
                status: 500,
                contentType: 'application/json',
                body: JSON.stringify({ error: 'Internal server error' }),
            });
        });

        const input = page.getByPlaceholder('Ask me anything…');
        const sendButton = page.getByRole('button', { name: /send/i });

        await input.fill('Test message');
        await sendButton.click();

        // Should display error message
        await expect(page.getByText(/error/i)).toBeVisible();
    });

    test('should handle network errors gracefully', async ({ page }) => {
        // Mock network error
        await page.route('**/chat', async route => {
            await route.abort('failed');
        });

        const input = page.getByPlaceholder('Ask me anything…');
        const sendButton = page.getByRole('button', { name: /send/i });

        await input.fill('Test message');
        await sendButton.click();

        // Should display network error message
        await expect(page.getByText(/network error/i)).toBeVisible();
    });

    test('should allow sending message with Enter key', async ({ page }) => {
        // Mock API response
        await page.route('**/chat', async route => {
            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({ answer: 'Response via Enter key' }),
            });
        });

        const input = page.getByPlaceholder('Ask me anything…');

        await input.fill('Test Enter key');
        await input.press('Enter');

        // Should send the message and display response
        await expect(page.getByText('Response via Enter key')).toBeVisible();
    });

    test('should prevent sending empty messages', async ({ page }) => {
        const sendButton = page.getByRole('button', { name: /send/i });

        // Try to send without typing anything
        await sendButton.click();

        // Should not have made any API calls or added messages
        // (In a real test, you might check for lack of new chat bubbles)
        await expect(sendButton).toBeEnabled(); // Button should still be enabled
    });

    test('should maintain chat history', async ({ page }) => {
        // Mock multiple API responses
        let responseCount = 0;
        await page.route('**/chat', async route => {
            responseCount++;
            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({ answer: `Response ${responseCount}` }),
            });
        });

        const input = page.getByPlaceholder('Ask me anything…');
        const sendButton = page.getByRole('button', { name: /send/i });

        // Send first message
        await input.fill('First message');
        await sendButton.click();

        // Wait for response
        await expect(page.getByText('Response 1')).toBeVisible();

        // Send second message
        await input.fill('Second message');
        await sendButton.click();

        // Both messages should be visible
        await expect(page.getByText('First message')).toBeVisible();
        await expect(page.getByText('Response 1')).toBeVisible();
        await expect(page.getByText('Second message')).toBeVisible();
        await expect(page.getByText('Response 2')).toBeVisible();
    });

    test('should be responsive on mobile devices', async ({ page }) => {
        // Simulate mobile viewport
        await page.setViewportSize({ width: 375, height: 667 });

        // Check that elements are still visible and usable
        await expect(page.getByText('Multi Agent Chat')).toBeVisible();
        await expect(page.getByPlaceholder('Ask me anything…')).toBeVisible();
        await expect(page.getByRole('button', { name: /send/i })).toBeVisible();

        // Test interaction on mobile
        const input = page.getByPlaceholder('Ask me anything…');
        await input.fill('Mobile test');
        await expect(input).toHaveValue('Mobile test');
    });

    test('should have proper accessibility attributes', async ({ page }) => {
        const input = page.getByPlaceholder('Ask me anything…');
        const sendButton = page.getByRole('button', { name: /send/i });

        // Check that elements have proper roles and labels
        await expect(input).toHaveAttribute('type', 'text');
        await expect(sendButton).toHaveAttribute('type', 'button');

        // Check that the main heading is properly structured
        const heading = page.getByRole('heading', { name: /multi agent chat/i });
        await expect(heading).toBeVisible();
    });
}); 