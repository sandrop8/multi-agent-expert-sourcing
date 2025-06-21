# Test info

- Name: Multi-Agent Chat Application >> should display AI response after successful request
- Location: /Users/jensbosseparra/github_projects/multi-agent-expert-sourcing/frontend/e2e/chat.spec.ts:102:9

# Error details

```
Error: locator.fill: Test timeout of 30000ms exceeded.
Call log:
  - waiting for getByPlaceholder('Describe your project, skills needed, timeline, budget...')

    at /Users/jensbosseparra/github_projects/multi-agent-expert-sourcing/frontend/e2e/chat.spec.ts:115:21
```

# Page snapshot

```yaml
- text: missing required error components, refreshing...
```

# Test source

```ts
   15 |
   16 |     test('should have proper page title and favicon', async ({ page }) => {
   17 |         await expect(page).toHaveTitle(/expert sourcing demo/i);
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
   81 |             await new Promise(resolve => setTimeout(resolve, 1000));
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
   95 |         // Should show loading indicators in chat area
   96 |         await expect(page.getByText('AI is analyzing your project requirements...')).toBeVisible();
   97 |
   98 |         // Wait for the response to complete
   99 |         await expect(page.getByText('Delayed response')).toBeVisible();
  100 |     });
  101 |
  102 |     test('should display AI response after successful request', async ({ page }) => {
  103 |         // Mock successful API response
  104 |         await page.route('**/chat', async route => {
  105 |             await route.fulfill({
  106 |                 status: 200,
  107 |                 contentType: 'application/json',
  108 |                 body: JSON.stringify({ answer: 'This is an AI response from the expert sourcing system' }),
  109 |             });
  110 |         });
  111 |
  112 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  113 |         const submitButton = page.getByRole('button', { name: /submit/i });
  114 |
> 115 |         await input.fill('Find me a Python developer');
      |                     ^ Error: locator.fill: Test timeout of 30000ms exceeded.
  116 |         await submitButton.click();
  117 |
  118 |         // Should display the AI response
  119 |         await expect(page.getByText('This is an AI response from the expert sourcing system')).toBeVisible();
  120 |     });
  121 |
  122 |     test('should handle API errors gracefully', async ({ page }) => {
  123 |         // Mock API error
  124 |         await page.route('**/chat', async route => {
  125 |             await route.fulfill({
  126 |                 status: 500,
  127 |                 contentType: 'application/json',
  128 |                 body: JSON.stringify({ error: 'Internal server error' }),
  129 |             });
  130 |         });
  131 |
  132 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  133 |         const submitButton = page.getByRole('button', { name: /submit/i });
  134 |
  135 |         await input.fill('Test message');
  136 |         await submitButton.click();
  137 |
  138 |         // Fix: Be more specific about which error message to look for
  139 |         await expect(page.getByText('Error: HTTP error! status: 500')).toBeVisible();
  140 |     });
  141 |
  142 |     test('should handle network errors gracefully', async ({ page }) => {
  143 |         // Mock network error
  144 |         await page.route('**/chat', async route => {
  145 |             await route.abort('failed');
  146 |         });
  147 |
  148 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  149 |         const submitButton = page.getByRole('button', { name: /submit/i });
  150 |
  151 |         await input.fill('Test message');
  152 |         await submitButton.click();
  153 |
  154 |         // Should show user message and handle error gracefully
  155 |         await expect(page.getByText('Test message')).toBeVisible();
  156 |
  157 |         // App should remain functional - test that we can still type
  158 |         await input.fill('Another message');
  159 |         await expect(input).toHaveValue('Another message');
  160 |     });
  161 |
  162 |     test('should allow sending message with Enter key', async ({ page }) => {
  163 |         // Mock API response
  164 |         await page.route('**/chat', async route => {
  165 |             await route.fulfill({
  166 |                 status: 200,
  167 |                 contentType: 'application/json',
  168 |                 body: JSON.stringify({ answer: 'Response via Enter key' }),
  169 |             });
  170 |         });
  171 |
  172 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  173 |
  174 |         await input.fill('Test Enter key');
  175 |         await input.press('Enter');
  176 |
  177 |         // Should send the message and display response
  178 |         await expect(page.getByText('Response via Enter key')).toBeVisible();
  179 |     });
  180 |
  181 |     test('should prevent sending empty messages', async ({ page }) => {
  182 |         const submitButton = page.getByRole('button', { name: /submit/i });
  183 |
  184 |         // Try to send without typing anything
  185 |         await submitButton.click();
  186 |
  187 |         // Should not have made any API calls or added messages
  188 |         // (In a real test, you might check for lack of new chat bubbles)
  189 |         await expect(submitButton).toBeEnabled(); // Button should still be enabled
  190 |     });
  191 |
  192 |     test('should maintain chat history', async ({ page }) => {
  193 |         // Mock multiple API responses
  194 |         let responseCount = 0;
  195 |         await page.route('**/chat', async route => {
  196 |             responseCount++;
  197 |             await route.fulfill({
  198 |                 status: 200,
  199 |                 contentType: 'application/json',
  200 |                 body: JSON.stringify({ answer: `Response ${responseCount}` }),
  201 |             });
  202 |         });
  203 |
  204 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  205 |         const submitButton = page.getByRole('button', { name: /submit/i });
  206 |
  207 |         // Send first message
  208 |         await input.fill('First message');
  209 |         await submitButton.click();
  210 |
  211 |         // Wait for response
  212 |         await expect(page.getByText('Response 1')).toBeVisible();
  213 |
  214 |         // Send second message
  215 |         await input.fill('Second message');
```
