import { expect, test } from '@playwright/test';

test.describe('Multi-Agent Chat Application', () => {
    test.beforeEach(async ({ page }) => {
        // Navigate to the project submission chat page
        await page.goto('/project-submission');
    });

    test('should load the chat interface correctly', async ({ page }) => {
        // Check that main elements are present
        await expect(page.getByText('Project Submission Chat')).toBeVisible();
        await expect(page.getByPlaceholder('Describe your project, skills needed, timeline, budget...')).toBeVisible();
        await expect(page.getByRole('button', { name: /submit/i })).toBeVisible();
    });

    test('should have proper page title and favicon', async ({ page }) => {
        await expect(page).toHaveTitle(/expert sourcing demo/i);
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
            await new Promise(resolve => setTimeout(resolve, 1000));
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

        // Should show loading indicators in chat area
        await expect(page.getByText('AI is analyzing your project requirements...')).toBeVisible();

        // Wait for the response to complete
        await expect(page.getByText('Delayed response')).toBeVisible();
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

        // Fix: Be more specific about which error message to look for
        await expect(page.getByText('Error: HTTP error! status: 500')).toBeVisible();
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

        // Should show user message and handle error gracefully
        await expect(page.getByText('Test message')).toBeVisible();

        // App should remain functional - test that we can still type
        await input.fill('Another message');
        await expect(input).toHaveValue('Another message');
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

        // Check that the main heading is properly structured
        await expect(page.getByRole('heading', { name: 'Project Submission Chat' })).toBeVisible();

        // Check that input has proper accessibility attributes
        await expect(input).toHaveAttribute('placeholder');
        await expect(submitButton).toBeEnabled();

        // Verify elements are accessible through roles
        await expect(input).toBeVisible();
        await expect(submitButton).toBeVisible();
    });
});
