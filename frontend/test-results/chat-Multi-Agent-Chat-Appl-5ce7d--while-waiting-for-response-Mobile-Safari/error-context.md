# Test info

- Name: Multi-Agent Chat Application >> should show loading state while waiting for response
- Location: /Users/jensbosseparra/github_projects/multi-agent-expert-sourcing/frontend/e2e/chat.spec.ts:78:9

# Error details

```
Error: browserType.launch: Executable doesn't exist at /Users/jensbosseparra/Library/Caches/ms-playwright/webkit-2158/pw_run.sh
╔═════════════════════════════════════════════════════════════════════════╗
║ Looks like Playwright Test or Playwright was just installed or updated. ║
║ Please run the following command to download new browsers:              ║
║                                                                         ║
║     npx playwright install                                              ║
║                                                                         ║
║ <3 Playwright Team                                                      ║
╚═════════════════════════════════════════════════════════════════════════╝
```

# Test source

```ts
   1 | import { expect, test } from '@playwright/test';
   2 |
   3 | test.describe('Multi-Agent Chat Application', () => {
   4 |     test.beforeEach(async ({ page }) => {
   5 |         // Navigate to the project chat page
   6 |         await page.goto('/project');
   7 |     });
   8 |
   9 |     test('should load the chat interface correctly', async ({ page }) => {
   10 |         // Check that main elements are present
   11 |         await expect(page.getByText('Project Submission Chat')).toBeVisible();
   12 |         await expect(page.getByPlaceholder('Describe your project, skills needed, timeline, budget...')).toBeVisible();
   13 |         await expect(page.getByRole('button', { name: /submit/i })).toBeVisible();
   14 |     });
   15 |
   16 |     test('should have proper page title and favicon', async ({ page }) => {
   17 |         await expect(page).toHaveTitle(/multi-agent/i);
   18 |     });
   19 |
   20 |     test('should display input field and submit button', async ({ page }) => {
   21 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
   22 |         const submitButton = page.getByRole('button', { name: /submit/i });
   23 |
   24 |         await expect(input).toBeEnabled();
   25 |         await expect(submitButton).toBeEnabled();
   26 |     });
   27 |
   28 |     test('should handle user input correctly', async ({ page }) => {
   29 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
   30 |
   31 |         // Type a message
   32 |         await input.fill('Hello, I need help finding a developer');
   33 |         await expect(input).toHaveValue('Hello, I need help finding a developer');
   34 |     });
   35 |
   36 |     test('should clear input after sending message', async ({ page }) => {
   37 |         // Mock the API response to avoid actual backend calls
   38 |         await page.route('**/chat', async route => {
   39 |             await route.fulfill({
   40 |                 status: 200,
   41 |                 contentType: 'application/json',
   42 |                 body: JSON.stringify({ answer: 'I can help you find a developer!' }),
   43 |             });
   44 |         });
   45 |
   46 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
   47 |         const submitButton = page.getByRole('button', { name: /submit/i });
   48 |
   49 |         await input.fill('Test message');
   50 |         await submitButton.click();
   51 |
   52 |         // Input should be cleared after sending
   53 |         await expect(input).toHaveValue('');
   54 |     });
   55 |
   56 |     test('should display user message immediately', async ({ page }) => {
   57 |         // Mock the API response
   58 |         await page.route('**/chat', async route => {
   59 |             // Add a delay to simulate network request
   60 |             await new Promise(resolve => setTimeout(resolve, 1000));
   61 |             await route.fulfill({
   62 |                 status: 200,
   63 |                 contentType: 'application/json',
   64 |                 body: JSON.stringify({ answer: 'Mock AI response' }),
   65 |             });
   66 |         });
   67 |
   68 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
   69 |         const submitButton = page.getByRole('button', { name: /submit/i });
   70 |
   71 |         await input.fill('Test user message');
   72 |         await submitButton.click();
   73 |
   74 |         // User message should appear immediately (optimistic UI)
   75 |         await expect(page.getByText('Test user message')).toBeVisible();
   76 |     });
   77 |
>  78 |     test('should show loading state while waiting for response', async ({ page }) => {
      |         ^ Error: browserType.launch: Executable doesn't exist at /Users/jensbosseparra/Library/Caches/ms-playwright/webkit-2158/pw_run.sh
   79 |         // Mock a slow API response
   80 |         await page.route('**/chat', async route => {
   81 |             await new Promise(resolve => setTimeout(resolve, 2000));
   82 |             await route.fulfill({
   83 |                 status: 200,
   84 |                 contentType: 'application/json',
   85 |                 body: JSON.stringify({ answer: 'Delayed response' }),
   86 |             });
   87 |         });
   88 |
   89 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
   90 |         const submitButton = page.getByRole('button', { name: /submit/i });
   91 |
   92 |         await input.fill('Test message');
   93 |         await submitButton.click();
   94 |
   95 |         // Should show loading indicators
   96 |         await expect(page.getByText('AI is analyzing your project requirements...')).toBeVisible();
   97 |         await expect(page.getByText('Analyzing...')).toBeVisible();
   98 |         await expect(submitButton).toBeDisabled();
   99 |     });
  100 |
  101 |     test('should display AI response after successful request', async ({ page }) => {
  102 |         // Mock successful API response
  103 |         await page.route('**/chat', async route => {
  104 |             await route.fulfill({
  105 |                 status: 200,
  106 |                 contentType: 'application/json',
  107 |                 body: JSON.stringify({ answer: 'This is an AI response from the expert sourcing system' }),
  108 |             });
  109 |         });
  110 |
  111 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  112 |         const submitButton = page.getByRole('button', { name: /submit/i });
  113 |
  114 |         await input.fill('Find me a Python developer');
  115 |         await submitButton.click();
  116 |
  117 |         // Should display the AI response
  118 |         await expect(page.getByText('This is an AI response from the expert sourcing system')).toBeVisible();
  119 |     });
  120 |
  121 |     test('should handle API errors gracefully', async ({ page }) => {
  122 |         // Mock API error
  123 |         await page.route('**/chat', async route => {
  124 |             await route.fulfill({
  125 |                 status: 500,
  126 |                 contentType: 'application/json',
  127 |                 body: JSON.stringify({ error: 'Internal server error' }),
  128 |             });
  129 |         });
  130 |
  131 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  132 |         const submitButton = page.getByRole('button', { name: /submit/i });
  133 |
  134 |         await input.fill('Test message');
  135 |         await submitButton.click();
  136 |
  137 |         // Should display error message
  138 |         await expect(page.getByText(/error/i)).toBeVisible();
  139 |     });
  140 |
  141 |     test('should handle network errors gracefully', async ({ page }) => {
  142 |         // Mock network error
  143 |         await page.route('**/chat', async route => {
  144 |             await route.abort('failed');
  145 |         });
  146 |
  147 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  148 |         const submitButton = page.getByRole('button', { name: /submit/i });
  149 |
  150 |         await input.fill('Test message');
  151 |         await submitButton.click();
  152 |
  153 |         // Should display network error message
  154 |         await expect(page.getByText(/network error/i)).toBeVisible();
  155 |     });
  156 |
  157 |     test('should allow sending message with Enter key', async ({ page }) => {
  158 |         // Mock API response
  159 |         await page.route('**/chat', async route => {
  160 |             await route.fulfill({
  161 |                 status: 200,
  162 |                 contentType: 'application/json',
  163 |                 body: JSON.stringify({ answer: 'Response via Enter key' }),
  164 |             });
  165 |         });
  166 |
  167 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  168 |
  169 |         await input.fill('Test Enter key');
  170 |         await input.press('Enter');
  171 |
  172 |         // Should send the message and display response
  173 |         await expect(page.getByText('Response via Enter key')).toBeVisible();
  174 |     });
  175 |
  176 |     test('should prevent sending empty messages', async ({ page }) => {
  177 |         const submitButton = page.getByRole('button', { name: /submit/i });
  178 |
```