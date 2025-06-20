# 🧪 Testing Framework Documentation

**Comprehensive testing setup and guide for the Multi-Agent Expert Sourcing application.**

> 📖 **Navigation**: [Main README](README.md) | **[Complete Testing Guide]** | [Backend Tests](backend/tests/README.md) | [Tailwind Debug](frontend/TAILWIND_DEBUG_GUIDE.md)

---

## ⚡ **Quick Start - Run Tests Now**

### **🎯 Everything (Recommended)**
```bash
./test-all.sh
```
*Runs all backend tests plus frontend testing with comprehensive summary*

### **🔥 Quick Commands**
```bash
# Frontend tests
cd frontend && bun run test

# Backend tests (67 working tests)
cd backend && uv run pytest tests/ -v

# E2E tests
cd frontend && bunx playwright test

# Database check
cd backend && uv run python scripts/test_db.py

# Type safety
cd frontend && bunx tsc --noEmit
```

### **📊 Current Test Status**
✅ **67 Backend Tests** - pytest + FastAPI TestClient (working reliably)
✅ **Frontend Testing** - Jest + React Testing Library
✅ **E2E Testing** - Playwright cross-browser testing
✅ **Quality Assurance** - ESLint + TypeScript
✅ **CV Processing** - Core tests working, complex tests disabled

### **⚡ Daily Workflow**
```bash
# Before coding
./test-all.sh                    # Ensure clean start

# During development
cd frontend && bun run test:watch   # Watch mode
cd backend && uv run pytest -v     # Quick backend check

# Before committing
./test-all.sh                    # Full verification
```

---

## 📋 **Testing Strategy Overview**

### **Testing Pyramid**
```
    🏔️ E2E Tests (Playwright)
      - Full user workflows
      - Cross-browser compatibility
      - Mobile responsiveness

  🧱 Integration Tests (React Testing Library)
    - Component interactions
    - API integration
    - User interactions

🏗️ Unit Tests (Jest + React Testing Library + pytest)
  - Individual components
  - Utility functions
  - API endpoints
  - Business logic
```

## 🎯 **Frontend Testing Stack**

### **Technologies Used**
- **Jest 29.7.0** - JavaScript testing framework
- **React Testing Library 14.1.2** - React component testing utilities
- **Playwright 1.40.1** - End-to-end testing framework
- **@testing-library/jest-dom 6.1.5** - Custom Jest matchers
- **@testing-library/user-event 14.5.1** - User interaction simulation
- **MSW 2.0.11** - API mocking for isolated testing

### **Test Structure**
```
frontend/
├── __tests__/               # Integration tests
│   └── page.test.tsx       # Main chat page tests
├── components/
│   └── ui/
│       └── __tests__/      # Unit tests for UI components
│           └── button.test.tsx
├── e2e/                    # End-to-end tests
│   └── chat.spec.ts        # E2E chat functionality tests
├── jest.config.js          # Jest configuration
├── jest.setup.js           # Test setup and mocks
├── playwright.config.ts    # Playwright configuration
└── .lintstagedrc.js       # Pre-commit hooks configuration
```

### **Running Frontend Tests**

#### **Unit & Integration Tests**
```bash
cd frontend

# Run all tests
bun run test

# Run tests in watch mode
bun run test:watch

# Run tests with coverage
bun run test:coverage

# Run specific test file
bun run test button.test.tsx

# Run tests related to changed files
bun run test --onlyChanged
```

#### **End-to-End Tests**
```bash
cd frontend

# Install Playwright browsers (first time only)
bunx playwright install

# Run E2E tests
bun run test:e2e

# Run E2E tests with UI mode
bun run test:e2e:ui

# Run specific E2E test
bunx playwright test chat.spec.ts

# Run tests in specific browser
bunx playwright test --project=chromium
```

#### **All Tests**
```bash
cd frontend

# Run linting, unit tests, and build
bun run test:all
```

## 🐍 **Backend Testing Stack**

### **Technologies Used**
- **pytest 7.4.0** - Python testing framework
- **pytest-asyncio 0.21.0** - Async test support
- **httpx 0.24.0** - Async HTTP client for FastAPI testing
- **pytest-cov 4.1.0** - Coverage reporting
- **pytest-mock 3.11.0** - Mocking utilities

### **Current Test Status (67 Working Tests)**
```
backend/tests/
├── test_simple.py       # 14 tests - Basic functionality ✅
├── test_api.py          # 33 tests - API endpoints ✅ (1 disabled)
├── test_cv_extraction.py # 6 tests - CV service ✅ (4 skipped)
├── test_cv_agents.py    # 12 tests - CV workflow ✅ (2 disabled)
└── fixtures/            # Test data files
    └── test-cv.pdf      # Sample CV for testing
```

### **Disabled Tests (For Future Integration)**
- `test_cv_upload_database_storage` - Makes real OpenAI API calls (73+ seconds)
- `test_cv_workflow_with_real_file` - Makes real OpenAI API calls (31+ seconds)
- `test_extraction_tools_functionality` - Broken mock (needs fixing)

### **Running Backend Tests**

#### **Install Test Dependencies**
```bash
cd backend

# Install with test dependencies
uv sync --group test

# Or add test dependencies individually
uv add --group test pytest pytest-asyncio httpx pytest-cov pytest-mock
```

#### **Run Tests**
```bash
cd backend

# Run all tests (fast - 6 seconds)
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html --cov-report=term

# Run specific test file
uv run pytest tests/test_api.py

# Run specific test class
uv run pytest tests/test_api.py::TestChatEndpoint

# Run with verbose output
uv run pytest -v

# Run and stop on first failure
uv run pytest -x
```

#### **Database Tests**
```bash
cd backend

# Test database connectivity
uv run python scripts/test_db.py
```

## 🚀 **CV Tests Integration**

### **Smart Test Design**
The CV processing tests are designed to work reliably:

```bash
# CV tests run automatically with backend tests
cd backend && uv run pytest tests/ -v

# Specific CV test files
cd backend && uv run pytest tests/test_cv_extraction.py -v
cd backend && uv run pytest tests/test_cv_agents.py -v
```

### **What Happens When Dependencies Are Missing:**
- Tests gracefully skip with `pytest.skip()`
- No hanging or failures
- Clear messages about what's missing
- Core functionality remains testable

### **Test Categories:**
- **Always Run**: Import tests, configuration validation, mocked functionality
- **Conditional**: Real API tests when `OPENAI_API_KEY` is set
- **Disabled**: Tests making expensive real API calls (marked for integration)

## 🪝 **Pre-commit Integration**

**Current Setup**: Pre-commit hooks are configured and ready to use!

```bash
# Manual testing (comprehensive)
./test-all.sh

# Pre-commit hooks (fast quality checks)
cd backend && uv run pre-commit run --all-files
```

**What the hooks do:**
- ✅ Backend: Ruff linting/formatting + quick tests (test_simple.py)
- ✅ Frontend: ESLint + TypeScript + quick Jest tests
- ✅ File validation: YAML, JSON, trailing whitespace

> 📖 **Setup Guide**: See [Generic CI/CD Setup Guide](../ai_generic_docs/CI_CD_Setup.md) for detailed pre-commit installation and configuration

## 📊 **Coverage Requirements**

### **Frontend Coverage Thresholds**
```javascript
// jest.config.js
coverageThreshold: {
  global: {
    branches: 70,
    functions: 70,
    lines: 70,
    statements: 70,
  },
}
```

### **Backend Coverage Thresholds**
```toml
# pyproject.toml
[tool.coverage.report]
exclude_lines = [
  "pragma: no cover",
  "def __repr__",
  "raise AssertionError",
  "raise NotImplementedError",
  "if __name__ == .__main__.:",
]
```

## 🔧 **Test Configuration Files**

### **Jest Configuration (frontend/jest.config.js)**
- **Environment**: jsdom for React testing
- **Setup**: Custom test utilities and mocks
- **Module mapping**: Path aliases (@/ → frontend/)
- **Coverage**: Comprehensive reporting with thresholds

### **Playwright Configuration (frontend/playwright.config.ts)**
- **Browsers**: Chromium, Firefox, WebKit
- **Mobile**: iPhone 12, Pixel 5
- **Features**: Screenshots, videos, traces
- **Server**: Auto-start development server

### **pytest Configuration (backend/pyproject.toml)**
- **Test discovery**: Automatic test file detection
- **Async support**: Built-in asyncio mode
- **Coverage**: Source code coverage tracking
- **Fixtures**: Database and client setup

## 🧩 **Writing Tests**

### **Frontend Component Tests**
```typescript
// Example: Button component test
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from '../button'

describe('Button Component', () => {
  it('calls onClick handler when clicked', async () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)

    const button = screen.getByRole('button')
    await userEvent.click(button)

    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

### **Frontend Page Tests**
```typescript
// Example: Page integration test
import { render, screen } from '@testing-library/react'
import ChatPage from '../page'

// Mock fetch
global.fetch = jest.fn()

describe('ChatPage', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('sends message when form is submitted', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ answer: 'AI response' }),
    })

    render(<ChatPage />)
    // ... test implementation
  })
})
```

### **E2E Tests**
```typescript
// Example: E2E test
import { test, expect } from '@playwright/test'

test('should complete chat workflow', async ({ page }) => {
  await page.goto('/')

  // Mock API
  await page.route('**/chat', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ answer: 'Mocked response' }),
    })
  })

  // Test user interaction
  await page.fill('[placeholder="Ask me anything…"]', 'Test message')
  await page.click('button:has-text("Send")')

  await expect(page.getByText('Mocked response')).toBeVisible()
})
```

### **Backend API Tests**
```python
# Example: FastAPI test
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_chat_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/chat",
            json={"prompt": "Find me a developer"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
```

### **CV Upload Tests**
```python
# Example: CV upload test
import io
from fastapi.testclient import TestClient
from main import app

def test_cv_upload_success():
    client = TestClient(app)
    pdf_content = b"Mock PDF content"

    response = client.post(
        "/upload-cv",
        files={"file": ("resume.pdf", io.BytesIO(pdf_content), "application/pdf")}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "CV uploaded successfully"
    assert data["filename"] == "resume.pdf"
```

## 🚀 **CI/CD Integration**

> 📖 **Full CI/CD Setup**: See [Generic CI/CD Setup Guide](../ai_generic_docs/CI_CD_Setup.md) for complete GitHub Actions workflows, protected branches, and deployment automation

**Current Status**: Ready for CI/CD implementation with existing test infrastructure

## 📝 **Best Practices**

### **General Testing Principles**
1. **Test Behavior, Not Implementation** - Focus on what the user experiences
2. **Arrange, Act, Assert** - Structure tests clearly
3. **Independent Tests** - Each test should run in isolation
4. **Descriptive Names** - Test names should describe the expected behavior
5. **Mock External Dependencies** - Avoid real API calls in unit tests

### **Frontend Testing Guidelines**
- **Use `screen.getByRole()`** for better accessibility testing
- **Test user interactions** with `@testing-library/user-event`
- **Mock API calls** to avoid external dependencies
- **Test error states** and loading states
- **Verify accessibility** attributes and keyboard navigation

### **Backend Testing Guidelines**
- **Use fixtures** for common test setup
- **Test both success and error paths**
- **Mock external services** (OpenAI, database)
- **Test async functions** with `pytest-asyncio`
- **Validate request/response schemas**

### **E2E Testing Guidelines**
- **Test critical user journeys** end-to-end
- **Use page object models** for complex flows
- **Mock external APIs** when possible
- **Test across different browsers** and devices
- **Keep tests stable** and avoid flaky assertions

## 🔍 **Debugging Tests**

### **Frontend Debugging**
```bash
# Run tests with debugger
bun run test --detectOpenHandles --forceExit

# Debug specific test
bun run test --testNamePattern="should handle user input"

# Debug with VS Code
# Set breakpoints and run "Debug Jest Tests" configuration
```

### **Backend Debugging**
```bash
# Run with verbose output
uv run pytest -v -s

# Debug specific test
uv run pytest -v tests/test_api.py::test_chat_endpoint

# Run with pdb debugger
uv run pytest --pdb

# Debug async tests
uv run pytest -v --tb=short
```

### **E2E Debugging**
```bash
# Run with headed browser
bunx playwright test --headed

# Debug mode (step through tests)
bunx playwright test --debug

# Generate test code
bunx playwright codegen localhost:3000
```

## 📈 **Performance Testing**

### **Frontend Performance**
- **Bundle size analysis** with Next.js bundle analyzer
- **Lighthouse CI** for performance metrics
- **React DevTools Profiler** for component performance

### **Backend Performance**
- **Load testing** with `locust` or `artillery`
- **Database query optimization** with SQLAlchemy logging
- **Memory profiling** with `memory-profiler`

## 🔧 **Troubleshooting**

### **Common Issues**

#### **"Module not found" errors**
```bash
# Frontend
bun install
bun run test

# Backend
uv sync --group test
```

#### **Tests timing out**
```javascript
// Increase timeout in Jest
jest.setTimeout(30000)

// Or in specific test
test('async test', async () => {
  // test implementation
}, 30000)
```

#### **Playwright browser issues**
```bash
# Reinstall browsers
bunx playwright install --force

# Check system requirements
bunx playwright install-deps
```

#### **Database connection errors**
```bash
# Check environment variables
cat backend/.env

# Test database connectivity
cd backend && uv run python scripts/test_db.py
```

## 🆘 **Quick Fixes**

```bash
# Missing dependencies
cd frontend && bun install
cd backend && uv sync

# Database issues
cd backend && uv run python scripts/test_db.py

# Type errors
cd frontend && bunx tsc --noEmit
```

---

## 📚 **Additional Resources**

- **[Backend Test Details](backend/tests/README.md)** - Backend-specific test structure and debugging
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Playwright Documentation](https://playwright.dev/)
- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

**Happy Testing! 🎉**
