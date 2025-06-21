# Test info

- Name: Multi-Agent Chat Application >> should maintain chat history
- Location: /Users/jensbosseparra/github_projects/multi-agent-expert-sourcing/frontend/e2e/chat.spec.ts:192:9

# Error details

```
Error: Timed out 5000ms waiting for expect(locator).toBeVisible()

Locator: getByText('Response 1')
Expected: visible
Received: <element(s) not found>
Call log:
  - expect.toBeVisible with timeout 5000ms
  - waiting for getByText('Response 1')

    at /Users/jensbosseparra/github_projects/multi-agent-expert-sourcing/frontend/e2e/chat.spec.ts:212:52
```

# Page snapshot

```yaml
- main:
  - link "← Back to Home":
    - /url: /
  - heading "Project Submission Chat" [level=1]
  - paragraph: Describe your project requirements and our AI will help match you with the right freelancers
  - textbox "Describe your project, skills needed, timeline, budget...": First message
  - button "Submit"
```

# Test source

```ts
  112 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  113 |         const submitButton = page.getByRole('button', { name: /submit/i });
  114 |
  115 |         await input.fill('Find me a Python developer');
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
> 212 |         await expect(page.getByText('Response 1')).toBeVisible();
      |                                                    ^ Error: Timed out 5000ms waiting for expect(locator).toBeVisible()
  213 |
  214 |         // Send second message
  215 |         await input.fill('Second message');
  216 |         await submitButton.click();
  217 |
  218 |         // Both messages should be visible
  219 |         await expect(page.getByText('First message')).toBeVisible();
  220 |         await expect(page.getByText('Response 1')).toBeVisible();
  221 |         await expect(page.getByText('Second message')).toBeVisible();
  222 |         await expect(page.getByText('Response 2')).toBeVisible();
  223 |     });
  224 |
  225 |     test('should be responsive on mobile devices', async ({ page }) => {
  226 |         // Simulate mobile viewport
  227 |         await page.setViewportSize({ width: 375, height: 667 });
  228 |
  229 |         // Check that elements are still visible and usable
  230 |         await expect(page.getByText('Project Submission Chat')).toBeVisible();
  231 |         await expect(page.getByPlaceholder('Describe your project, skills needed, timeline, budget...')).toBeVisible();
  232 |         await expect(page.getByRole('button', { name: /submit/i })).toBeVisible();
  233 |
  234 |         // Test interaction on mobile
  235 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  236 |         await input.fill('Mobile test');
  237 |         await expect(input).toHaveValue('Mobile test');
  238 |     });
  239 |
  240 |     test('should have proper accessibility attributes', async ({ page }) => {
  241 |         const input = page.getByPlaceholder('Describe your project, skills needed, timeline, budget...');
  242 |         const submitButton = page.getByRole('button', { name: /submit/i });
  243 |
  244 |         // Check that the main heading is properly structured
  245 |         await expect(page.getByRole('heading', { name: 'Project Submission Chat' })).toBeVisible();
  246 |
  247 |         // Check that input has proper accessibility attributes
  248 |         await expect(input).toHaveAttribute('placeholder');
  249 |         await expect(submitButton).toBeEnabled();
  250 |
  251 |         // Verify elements are accessible through roles
  252 |         await expect(input).toBeVisible();
  253 |         await expect(submitButton).toBeVisible();
  254 |     });
  255 | });
  256 |
```
