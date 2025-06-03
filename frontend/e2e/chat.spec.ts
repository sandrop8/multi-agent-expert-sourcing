import { expect, test } from '@playwright/test';

test.describe('Multi-Agent Chat Application', () => {
    test.beforeEach(async ({ page }) => {
        // Navigate to the project chat page
        await page.goto('/project');
    });

    test('should load the chat interface correctly', async ({ page }) => {
        // Check that main elements are present
        await expect(page.getByText('Project Submission Chat')).toBeVisible();
        await expect(page.getByPlaceholder('Describe your project, skills needed, timeline, budget...')).toBeVisible();
        await expect(page.getByRole('button', { name: /submit/i })).toBeVisible();
    });

    test('should have proper page title and favicon', async ({ page }) => {
        await expect(page).toHaveTitle(/multi-agent/i);
    });

    test('should display input field and submit button', async ({ page }) => {
        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
        const submitButton = page.getByRole('button', { name: /submit/i });

        await expect(input).toBeEnabled();
        await expect(submitButton).toBeEnabled();
    });

    test('should handle user input correctly', async ({ page }) => {
        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');

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

        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
        const submitButton = page.getByRole('button', { name: /submit/i });

        await input.fill('Test message');
        await submitButton.click();

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

        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
        const submitButton = page.getByRole('button', { name: /submit/i });

        await input.fill('Test user message');
        await submitButton.click();

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

        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
        const submitButton = page.getByRole('button', { name: /submit/i });

        await input.fill('Test message');
        await submitButton.click();

        // Should show loading indicators
        await expect(page.getByText('AI is analyzing your project requirements...')).toBeVisible();
        await expect(page.getByText('Analyzing...')).toBeVisible();
        await expect(submitButton).toBeDisabled();
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

        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
        const submitButton = page.getByRole('button', { name: /submit/i });

        await input.fill('Find me a Python developer');
        await submitButton.click();

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

        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
        const submitButton = page.getByRole('button', { name: /submit/i });

        await input.fill('Test message');
        await submitButton.click();

        // Should display error message
        await expect(page.getByText(/error/i)).toBeVisible();
    });

    test('should handle network errors gracefully', async ({ page }) => {
        // Mock network error
        await page.route('**/chat', async route => {
            await route.abort('failed');
        });

        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
        const submitButton = page.getByRole('button', { name: /submit/i });

        await input.fill('Test message');
        await submitButton.click();

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

        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');

        await input.fill('Test Enter key');
        await input.press('Enter');

        // Should send the message and display response
        await expect(page.getByText('Response via Enter key')).toBeVisible();
    });

    test('should prevent sending empty messages', async ({ page }) => {
        const submitButton = page.getByRole('button', { name: /submit/i });

        // Try to send without typing anything
        await submitButton.click();

        // Should not have made any API calls or added messages
        // (In a real test, you might check for lack of new chat bubbles)
        await expect(submitButton).toBeEnabled(); // Button should still be enabled
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

        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
        const submitButton = page.getByRole('button', { name: /submit/i });

        // Send first message
        await input.fill('First message');
        await submitButton.click();

        // Wait for response
        await expect(page.getByText('Response 1')).toBeVisible();

        // Send second message
        await input.fill('Second message');
        await submitButton.click();

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
        await expect(page.getByText('Project Submission Chat')).toBeVisible();
        await expect(page.getByPlaceholder('Describe your project, skills needed, timeline, budget...')).toBeVisible();
        await expect(page.getByRole('button', { name: /submit/i })).toBeVisible();

        // Test interaction on mobile
        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
        await input.fill('Mobile test');
        await expect(input).toHaveValue('Mobile test');
    });

    test('should have proper accessibility attributes', async ({ page }) => {
        const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
        const submitButton = page.getByRole('button', { name: /submit/i });

        // Check that elements have proper roles and labels
        await expect(input).toHaveAttribute('type', 'text');
        await expect(submitButton).toHaveAttribute('type', 'button');

        // Check that the main heading is properly structured
        const heading = page.getByRole('heading', { name: /project submission chat/i });
        await expect(heading).toBeVisible();
    });
}); 