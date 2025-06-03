# Test info

- Name: Multi-Agent Chat Application >> should display AI response after successful request
- Location: /Users/jensbosseparra/github_projects/multi-agent-expert-sourcing/frontend/e2e/chat.spec.ts:101:9

# Error details

```
Error: locator.fill: Test timeout of 30000ms exceeded.
Call log:
  - waiting for getByPlaceholder('Describe your project, skills needed, timeline, budget...')

    at /Users/jensbosseparra/github_projects/multi-agent-expert-sourcing/frontend/e2e/chat.spec.ts:114:21
```

# Page snapshot

```yaml
- heading "404" [level=1]
- heading "This page could not be found." [level=2]
- img
- alert
```

# Test source

```ts
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
   78 |     test('should show loading state while waiting for response', async ({ page }) => {
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
> 114 |         await input.fill('Find me a Python developer');
      |                     ^ Error: locator.fill: Test timeout of 30000ms exceeded.
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
  179 |         // Try to send without typing anything
  180 |         await submitButton.click();
  181 |
  182 |         // Should not have made any API calls or added messages
  183 |         // (In a real test, you might check for lack of new chat bubbles)
  184 |         await expect(submitButton).toBeEnabled(); // Button should still be enabled
  185 |     });
  186 |
  187 |     test('should maintain chat history', async ({ page }) => {
  188 |         // Mock multiple API responses
  189 |         let responseCount = 0;
  190 |         await page.route('**/chat', async route => {
  191 |             responseCount++;
  192 |             await route.fulfill({
  193 |                 status: 200,
  194 |                 contentType: 'application/json',
  195 |                 body: JSON.stringify({ answer: `Response ${responseCount}` }),
  196 |             });
  197 |         });
  198 |
  199 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  200 |         const submitButton = page.getByRole('button', { name: /submit/i });
  201 |
  202 |         // Send first message
  203 |         await input.fill('First message');
  204 |         await submitButton.click();
  205 |
  206 |         // Wait for response
  207 |         await expect(page.getByText('Response 1')).toBeVisible();
  208 |
  209 |         // Send second message
  210 |         await input.fill('Second message');
  211 |         await submitButton.click();
  212 |
  213 |         // Both messages should be visible
  214 |         await expect(page.getByText('First message')).toBeVisible();
```