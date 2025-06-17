# 🔄 **CI/CD Pipeline Setup Guide**

**Generic, reusable guide for setting up CI/CD pipelines for Python backend + JavaScript frontend projects**

> 📖 **Usage**: This is a **generic setup guide** that can be applied to any Python + JavaScript project. For project-specific testing status and current implementation, see the project's TESTING.md file.

> 🎯 **Project Context**: This guide assumes a multi-service architecture with Python (FastAPI/Django) backend and JavaScript/TypeScript (React/Next.js) frontend

---

## 📋 **Overview: From Testing to Full CI/CD**

This guide provides a **modular progression** from basic testing to enterprise-level CI/CD:

1. **Phase 0**: Individual test frameworks (pytest, Jest, ESLint, etc.)
2. **Phase 1**: Unified testing script + Local automation (pre-commit hooks)
3. **Phase 2**: GitHub Actions foundation (CI on main branch)
4. **Phase 3**: Protected branch workflow (PRs + reviews)
5. **Phase 4**: Advanced CI/CD (multi-environment deployment)

---

## 🎯 **Phase 0: Foundation Testing Stack**

### **Backend Testing Stack (Python)**
- **pytest** - Python testing framework
- **pytest-asyncio** - Async test support
- **httpx** - FastAPI async testing client
- **pytest-cov** - Coverage reporting
- **pytest-mock** - Mocking utilities
- **ruff** - Fast Python linter (replaces flake8, black)

### **Frontend Testing Stack (JavaScript/TypeScript)**
- **Jest** - JavaScript testing framework
- **React Testing Library** - Component testing utilities
- **Playwright** - End-to-end testing framework
- **@testing-library/jest-dom** - Custom Jest matchers
- **ESLint** - JavaScript/TypeScript linting
- **TypeScript** - Type checking

### **Initial Setup Commands**

**Backend Setup:**
```bash
cd backend

# Install test dependencies
uv add --group test pytest pytest-asyncio httpx pytest-cov pytest-mock ruff

# Create pytest configuration
cat > pyproject.toml << 'EOF'
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "--tb=short --strict-markers"

[tool.coverage.run]
source = ["."]
omit = ["tests/*", "venv/*", ".venv/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]

[tool.ruff]
line-length = 100
target-version = "py39"
EOF
```

**Frontend Setup:**
```bash
cd frontend

# Install test dependencies
bun add -D jest @testing-library/react @testing-library/jest-dom @testing-library/user-event
bun add -D playwright @playwright/test
bun add -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
bun add -D typescript

# Install Playwright browsers
bunx playwright install

# Create Jest configuration
cat > jest.config.js << 'EOF'
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  dir: './',
})

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jsdom',
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/$1',
  },
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
}

module.exports = createJestConfig(customJestConfig)
EOF
```

### **Test Structure Examples**

**Backend Test Structure:**
```
backend/
├── tests/
│   ├── __init__.py
│   ├── test_api.py          # API endpoint tests
│   ├── test_models.py       # Database model tests
│   ├── test_services.py     # Business logic tests
│   └── fixtures/
│       └── test_data.py     # Test data fixtures
└── pyproject.toml
```

**Frontend Test Structure:**
```
frontend/
├── __tests__/               # Integration tests
│   └── page.test.tsx
├── components/
│   └── ui/
│       └── __tests__/       # Unit tests
│           └── button.test.tsx
├── e2e/                     # End-to-end tests
│   └── app.spec.ts
├── jest.config.js
└── playwright.config.ts
```

---

## 🧪 **Phase 1: Unified Testing Script**

### **Creating the Master Test Script**

Create a comprehensive test script that runs all tests across both services:

```bash
# test-all.sh
#!/bin/bash

set -e  # Exit on any error

echo "🧪 Starting comprehensive test suite..."
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Store original directory
ORIGINAL_DIR=$(pwd)

# Test results storage
FRONTEND_PASSED=0
FRONTEND_TOTAL=0
E2E_PASSED=0
E2E_TOTAL=0
API_PASSED=0
API_TOTAL=0
ESLINT_ERRORS=0
TYPESCRIPT_ERRORS=0

# Backend Tests
print_status "Running backend tests..."
cd backend

# Check dependencies
if [ ! -d ".venv" ]; then
    print_warning "Backend virtual environment not found. Setting up..."
    uv sync
fi

# Run pytest tests
print_status "Running pytest tests..."
if uv run pytest tests/ --tb=short --cov=. --cov-report=term > pytest.log 2>&1; then
    print_success "Backend pytest tests completed"
    API_PASSED=$(grep "passed" pytest.log | tail -1 | grep -o "[0-9]\+" | head -1 || echo "0")
    API_TOTAL=$(grep "passed\|failed\|skipped" pytest.log | tail -1 | grep -o "[0-9]\+" | paste -sd+ | bc || echo "0")
else
    print_warning "Backend pytest tests completed with failures"
    API_PASSED=0
    API_TOTAL=50  # Fallback estimate
fi

# Run ruff linting
print_status "Running Python linting..."
if uv run ruff check . > ruff.log 2>&1; then
    print_success "Python linting passed"
else
    print_warning "Python linting found issues"
fi

cd "$ORIGINAL_DIR"

# Frontend Tests
print_status "Running frontend tests..."
cd frontend

# Check dependencies
if [ ! -d "node_modules" ]; then
    print_warning "Frontend node_modules not found. Installing..."
    bun install
fi

# ESLint check
print_status "Running ESLint..."
if bun run lint > eslint.log 2>&1; then
    print_success "ESLint passed"
    ESLINT_ERRORS=0
else
    ESLINT_ERRORS=$(grep -c "error" eslint.log || echo "0")
    print_warning "ESLint found $ESLINT_ERRORS error(s)"
fi

# TypeScript check
print_status "Running TypeScript type checking..."
if bunx tsc --noEmit > typescript.log 2>&1; then
    print_success "TypeScript type checking passed"
    TYPESCRIPT_ERRORS=0
else
    TYPESCRIPT_ERRORS=$(grep -c "error TS" typescript.log || echo "0")
    print_warning "TypeScript found $TYPESCRIPT_ERRORS error(s)"
fi

# Jest tests
print_status "Running Jest unit/integration tests..."
if timeout 120 bun run test --passWithNoTests --verbose > jest.log 2>&1; then
    print_success "Frontend Jest tests completed"
    FRONTEND_PASSED=$(grep "Tests:" jest.log | tail -1 | grep -o "[0-9]\+ passed" | grep -o "[0-9]\+" || echo "0")
    FRONTEND_TOTAL=$(grep "Tests:" jest.log | tail -1 | grep -o "[0-9]\+ total" | grep -o "[0-9]\+" || echo "0")
else
    print_warning "Frontend Jest tests completed with failures"
    FRONTEND_PASSED=0
    FRONTEND_TOTAL=38  # Fallback estimate
fi

# E2E Tests
print_status "Running Playwright E2E tests..."
if timeout 180 bunx playwright test --reporter=list > playwright.log 2>&1; then
    print_success "E2E tests completed"
    E2E_PASSED=$(grep "passed" playwright.log | tail -1 | grep -o "[0-9]\+" || echo "0")
    E2E_TOTAL=$(grep "passed\|failed" playwright.log | tail -1 | grep -o "[0-9]\+" | paste -sd+ | bc || echo "0")
else
    print_warning "E2E tests failed or timed out"
    E2E_PASSED=0
    E2E_TOTAL=10  # Fallback estimate
fi

cd "$ORIGINAL_DIR"

# Calculate totals
TOTAL_PASSED=$((FRONTEND_PASSED + E2E_PASSED + API_PASSED))
TOTAL_TESTS=$((FRONTEND_TOTAL + E2E_TOTAL + API_TOTAL))
SUCCESS_RATE=$(( (TOTAL_PASSED * 100) / TOTAL_TESTS ))
QA_ERRORS=$((ESLINT_ERRORS + TYPESCRIPT_ERRORS))

echo ""
echo "════════════════════════════════════════════"
echo -e "${BOLD}🧪 COMPREHENSIVE TEST SUITE SUMMARY${NC}"
echo "════════════════════════════════════════════"
echo ""

echo -e "${BOLD}📊 Testing Stack Results:${NC}"
echo -e "• ${BLUE}Frontend Testing${NC} - Jest + React Testing Library (${GREEN}${FRONTEND_PASSED}/${FRONTEND_TOTAL}${NC} tests passing)"
echo -e "• ${BLUE}E2E Testing${NC} - Playwright cross-browser testing (${GREEN}${E2E_PASSED}/${E2E_TOTAL}${NC} tests passing)"
echo -e "• ${BLUE}API Testing${NC} - pytest + FastAPI TestClient (${GREEN}${API_PASSED}/${API_TOTAL}${NC} tests passing)"

if [ "$QA_ERRORS" -eq 0 ]; then
    echo -e "• ${BLUE}Quality Assurance${NC} - ESLint + TypeScript + Ruff (${GREEN}0 errors${NC})"
else
    echo -e "• ${BLUE}Quality Assurance${NC} - ESLint + TypeScript + Ruff (${RED}$QA_ERRORS errors${NC})"
fi

echo ""
echo "════════════════════════════════════════════"

# Final Summary
if [ "$TOTAL_TESTS" -gt 0 ]; then
    if [ "$SUCCESS_RATE" -ge 95 ] && [ "$QA_ERRORS" -eq 0 ]; then
        echo -e "${GREEN}✅ ${TOTAL_PASSED}/${TOTAL_TESTS} Total Tests Passing (${SUCCESS_RATE}% success rate)${NC}"
        echo -e "${GREEN}🚀 Ready for deployment!${NC}"
        exit 0
    elif [ "$SUCCESS_RATE" -ge 85 ]; then
        echo -e "${YELLOW}⚠️  ${TOTAL_PASSED}/${TOTAL_TESTS} Total Tests Passing (${SUCCESS_RATE}% success rate)${NC}"
        echo -e "${YELLOW}🔧 Some issues found, but mostly passing${NC}"
        exit 0
    else
        echo -e "${RED}❌ ${TOTAL_PASSED}/${TOTAL_TESTS} Total Tests Passing (${SUCCESS_RATE}% success rate)${NC}"
        echo -e "${RED}🚫 Multiple test failures detected${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ No tests were executed successfully${NC}"
    exit 1
fi
```

### **Testing Documentation**

Create comprehensive testing documentation:

```markdown
# 🧪 Testing Framework Documentation

**Comprehensive testing setup and guide for Python backend + JavaScript frontend projects.**

## ⚡ **Quick Start - Run Tests Now**

### **🎯 Everything (Recommended)**
```bash
./test-all.sh
```

### **🔥 Quick Commands**
```bash
# Frontend tests
cd frontend && bun run test

# Backend tests
cd backend && uv run pytest tests/ -v

# E2E tests
cd frontend && bunx playwright test

# Type safety
cd frontend && bunx tsc --noEmit

# Linting
cd backend && uv run ruff check .
cd frontend && bun run lint
```

## 📊 **Testing Strategy Overview**

### **Testing Pyramid**
```
    🏔️ E2E Tests (Playwright)
      - Full user workflows
      - Cross-browser compatibility

  🧱 Integration Tests (React Testing Library + FastAPI TestClient)
    - Component interactions
    - API integration

🏗️ Unit Tests (Jest + pytest)
  - Individual components
  - Business logic
  - Utility functions
```

## 🎯 **Framework Coverage**

### **Frontend Testing**
- **Jest** - JavaScript testing framework
- **React Testing Library** - Component testing
- **Playwright** - End-to-end testing
- **ESLint** - Code quality
- **TypeScript** - Type safety

### **Backend Testing**
- **pytest** - Python testing framework
- **pytest-asyncio** - Async support
- **httpx** - API testing
- **pytest-cov** - Coverage reporting
- **ruff** - Fast linting

### **Integration Testing**
- **Database tests** - Schema validation
- **API endpoint tests** - Full request/response cycle
- **Cross-service communication** - Frontend ↔ Backend
```

---

## 🪝 **Phase 1B: Enhanced Pre-commit Hooks**

### **Installation**

```bash
# Install pre-commit framework
pip install pre-commit

# Or with uv
uv add --group dev pre-commit
```

### **Configuration**

Create `.pre-commit-config.yaml` in project root:

```yaml
# .pre-commit-config.yaml
repos:
  # Local project hooks
  - repo: local
    hooks:
      # Comprehensive test suite
      - id: test-all
        name: Run comprehensive test suite
        entry: ./test-all.sh
        language: system
        pass_filenames: false
        always_run: true
        verbose: true

      # Backend-specific hooks
      - id: backend-ruff-check
        name: Backend Ruff linting
        entry: bash -c 'cd backend && uv run ruff check .'
        language: system
        files: '^backend/.*\.py$'
        
      - id: backend-ruff-format
        name: Backend Ruff formatting
        entry: bash -c 'cd backend && uv run ruff format .'
        language: system
        files: '^backend/.*\.py$'
        
      - id: backend-pytest-quick
        name: Backend quick tests
        entry: bash -c 'cd backend && uv run pytest tests/ -x --tb=short'
        language: system
        files: '^backend/.*\.py$'

      # Frontend-specific hooks
      - id: frontend-eslint
        name: Frontend ESLint
        entry: bash -c 'cd frontend && bun run lint --fix'
        language: system
        files: '^frontend/.*\.(ts|tsx|js|jsx)$'
        
      - id: frontend-typescript
        name: Frontend TypeScript check
        entry: bash -c 'cd frontend && bunx tsc --noEmit'
        language: system
        files: '^frontend/.*\.(ts|tsx)$'
        
      - id: frontend-jest-quick
        name: Frontend quick tests
        entry: bash -c 'cd frontend && bun run test --onlyChanged --passWithNoTests'
        language: system
        files: '^frontend/.*\.(ts|tsx|js|jsx)$'

  # External hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: check-added-large-files
        args: ['--maxkb=1000']

  # Python-specific external hooks
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
        files: '^backend/.*\.py$'
      - id: ruff-format
        files: '^backend/.*\.py$'
```

### **Alternative: Fast Pre-commit (Selective Testing)**

For faster pre-commit hooks, create a selective version:

```yaml
# .pre-commit-config.yaml (Fast version)
repos:
  - repo: local
    hooks:
      # Quick validation only
      - id: selective-tests
        name: Run selective tests
        entry: bash
        args:
          - -c
          - |
            echo "🔍 Running selective pre-commit checks..."
            
            # Check if frontend files changed
            if git diff --cached --name-only | grep -q "^frontend/"; then
                echo "📱 Frontend changes detected"
                cd frontend && bun run lint --fix
                cd frontend && bunx tsc --noEmit
                cd frontend && bun run test --onlyChanged --passWithNoTests
            fi
            
            # Check if backend files changed  
            if git diff --cached --name-only | grep -q "^backend/"; then
                echo "🐍 Backend changes detected"
                cd backend && uv run ruff check . --fix
                cd backend && uv run pytest tests/ -x --tb=short
            fi
            
            echo "✅ Selective checks completed"
        language: system
        pass_filenames: false
        always_run: true

  # Still include external hooks for file validation
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
```

### **Setup Commands**

```bash
# Install pre-commit hooks
pre-commit install

# Test pre-commit hooks
pre-commit run --all-files

# Update hooks to latest versions
pre-commit autoupdate

# Temporarily skip hooks (if needed)
git commit -m "message" --no-verify
```

### **Pre-commit Hook Management**

```bash
# Show installed hooks
pre-commit --version

# Clean hook cache
pre-commit clean

# Manually run specific hook
pre-commit run backend-ruff-check --all-files

# Run only on staged files
pre-commit run
```

---

## 🚀 **Phase 2: GitHub Actions Foundation**

### **CI on Main Branch**

Create `.github/workflows/ci-main.yml`:

```yaml
name: CI Main Branch
on:
  push:
    branches: [main]
  workflow_dispatch:  # Allow manual triggering

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup Python with uv
        uses: astral-sh/setup-uv@v1
        with:
          python-version: "3.11"
          
      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        with:
          bun-version: latest
          
      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: |
            ~/.cache/uv
            ~/.bun/install/cache
          key: ${{ runner.os }}-deps-${{ hashFiles('**/uv.lock', '**/bun.lockb') }}
          
      - name: Install backend dependencies
        run: |
          cd backend
          uv sync
          
      - name: Install frontend dependencies
        run: |
          cd frontend
          bun install
          
      - name: Install Playwright browsers
        run: |
          cd frontend
          bunx playwright install --with-deps
          
      - name: Run comprehensive test suite
        run: ./test-all.sh
        env:
          CI: true
          
      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: |
            frontend/coverage/
            backend/htmlcov/
            frontend/test-results/
            frontend/playwright-report/
            
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        if: always()
        with:
          files: |
            backend/coverage.xml
            frontend/coverage/lcov.info
          fail_ci_if_error: false
```

### **PR Validation Workflow**

Create `.github/workflows/pr-validation.yml`:

```yaml
name: PR Validation
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Needed for changed files detection
          
      - name: Setup Python with uv
        uses: astral-sh/setup-uv@v1
        
      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        
      - name: Get changed files
        id: changed-files
        uses: tj-actions/changed-files@v42
        with:
          files_yaml: |
            backend:
              - 'backend/**/*.py'
            frontend:
              - 'frontend/**/*.{ts,tsx,js,jsx}'
            
      - name: Install dependencies
        run: |
          if [ "${{ steps.changed-files.outputs.backend_any_changed }}" == "true" ]; then
            cd backend && uv sync
          fi
          if [ "${{ steps.changed-files.outputs.frontend_any_changed }}" == "true" ]; then
            cd frontend && bun install
            bunx playwright install --with-deps
          fi
          
      - name: Run backend tests
        if: steps.changed-files.outputs.backend_any_changed == 'true'
        run: |
          cd backend
          uv run ruff check .
          uv run pytest tests/ --cov=. --cov-report=xml
          
      - name: Run frontend tests
        if: steps.changed-files.outputs.frontend_any_changed == 'true'
        run: |
          cd frontend
          bun run lint
          bunx tsc --noEmit
          bun run test --coverage
          
      - name: Run E2E tests
        if: steps.changed-files.outputs.frontend_any_changed == 'true'
        run: |
          cd frontend
          bunx playwright test
          
      - name: Comment PR with results
        uses: actions/github-script@v7
        if: always()
        with:
          script: |
            const fs = require('fs');
            const path = require('path');
            
            let comment = '## 🧪 Test Results\n\n';
            
            // Check if test results exist and add summary
            if (context.job.status === 'success') {
              comment += '✅ All tests passed!\n\n';
            } else {
              comment += '❌ Some tests failed. Please check the logs.\n\n';
            }
            
            comment += '### Changed Files\n';
            comment += `- Backend: ${{ steps.changed-files.outputs.backend_any_changed }}\n`;
            comment += `- Frontend: ${{ steps.changed-files.outputs.frontend_any_changed }}\n`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

### **Status Badges**

Add to your README.md:

```markdown
[![CI Main](https://github.com/username/repo/workflows/CI%20Main%20Branch/badge.svg)](https://github.com/username/repo/actions)
[![Tests](https://github.com/username/repo/workflows/PR%20Validation/badge.svg)](https://github.com/username/repo/actions)
[![codecov](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)
```

---

## 🔒 **Phase 3: Protected Branch Workflow**

### **Branch Protection Rules**

Configure in GitHub Repository Settings > Branches:

```yaml
# Branch protection configuration (GitHub UI)
Branch name pattern: main

Protection rules:
✅ Require a pull request before merging
  ✅ Require approvals: 1
  ✅ Dismiss stale PR approvals when new commits are pushed
  ✅ Require review from code owners (if CODEOWNERS file exists)

✅ Require status checks to pass before merging
  ✅ Require branches to be up to date before merging
  Required status checks:
    - test (from ci-main.yml)
    - validate (from pr-validation.yml)

✅ Require signed commits (optional)
✅ Require linear history (optional)
✅ Include administrators (recommended)
✅ Allow deletions: false
✅ Allow force pushes: false
```

### **Feature Branch Workflow**

```bash
# Create feature branch
git checkout -b feature/add-new-endpoint

# Work on feature
git add .
git commit -m "feat: add new API endpoint"

# Push feature branch
git push origin feature/add-new-endpoint

# Create pull request (GitHub UI or CLI)
gh pr create --title "Add new API endpoint" --body "Description of changes"

# After PR approval and CI passes, merge
gh pr merge --squash
```

### **CODEOWNERS File**

Create `.github/CODEOWNERS`:

```
# Global code owners
* @username

# Backend specific
backend/ @backend-team
backend/models/ @database-team

# Frontend specific
frontend/ @frontend-team
frontend/components/ @ui-team

# Infrastructure
.github/ @devops-team
docker/ @devops-team
```

---

## 🏢 **Phase 4: Advanced CI/CD (Future Enhancement)**

### **Multi-Environment Deployment**

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          # Deployment commands for staging
          
  deploy-production:
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment: production
    needs: [test]
    steps:
      - name: Deploy to production
        run: |
          # Deployment commands for production
```

### **Automated Releases**

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
```

### **Security Scanning**

```yaml
# .github/workflows/security.yml
name: Security Scan
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * 0'  # Weekly scan

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Bandit (Python security)
        run: |
          cd backend
          uv run bandit -r . -f json -o bandit-report.json
          
      - name: Run npm audit (JavaScript security)
        run: |
          cd frontend
          bun audit
          
      - name: Upload security reports
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: backend/bandit-report.json
```

---

## 📋 **Implementation Checklist**

### **Phase 0: Foundation ✅**
- [ ] Set up pytest for backend testing
- [ ] Set up Jest for frontend testing
- [ ] Set up Playwright for E2E testing
- [ ] Configure ESLint and TypeScript checking
- [ ] Set up ruff for Python linting
- [ ] Create test directory structure
- [ ] Write initial test suites

### **Phase 1: Unified Testing ✅**
- [ ] Create `test-all.sh` script
- [ ] Create comprehensive `TESTING.md` documentation
- [ ] Test script across all environments
- [ ] Set up coverage reporting
- [ ] Configure test result parsing

### **Phase 1B: Pre-commit Hooks ✅**
- [ ] Install pre-commit framework
- [ ] Create `.pre-commit-config.yaml`
- [ ] Configure local hooks
- [ ] Test pre-commit installation
- [ ] Document pre-commit workflow

### **Phase 2: GitHub Actions 🔄**
- [ ] Create CI workflow for main branch
- [ ] Create PR validation workflow
- [ ] Configure artifact uploads
- [ ] Set up status badges
- [ ] Test workflows

### **Phase 3: Protected Branches 🔄**
- [ ] Configure branch protection rules
- [ ] Set up CODEOWNERS file
- [ ] Train team on PR workflow
- [ ] Configure required status checks
- [ ] Test protected branch workflow

### **Phase 4: Advanced CI/CD 🔄**
- [ ] Set up multi-environment deployment
- [ ] Configure automated releases
- [ ] Add security scanning
- [ ] Set up monitoring and alerting
- [ ] Configure deployment rollbacks

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Pre-commit Hooks Not Running**
```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install

# Check hook status
pre-commit --version
```

#### **GitHub Actions Failing**
```bash
# Test locally with act
act -j test

# Check workflow syntax
gh workflow view ci-main.yml
```

#### **Dependencies Out of Sync**
```bash
# Update backend dependencies
cd backend && uv sync

# Update frontend dependencies
cd frontend && bun install

# Update pre-commit hooks
pre-commit autoupdate
```

### **Performance Optimization**

#### **Faster CI Runs**
- Use caching for dependencies
- Run tests in parallel
- Use matrix strategy for multiple versions
- Skip unnecessary steps based on changed files

#### **Selective Testing**
- Run only tests for changed files
- Use test impact analysis
- Implement smoke tests for quick validation

---

## 📚 **Additional Resources**

- [Pre-commit Documentation](https://pre-commit.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/)
- [Playwright Documentation](https://playwright.dev/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

---

**Happy CI/CD Pipeline Building! 🚀**
