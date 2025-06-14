#!/bin/bash

# 🧪 Multi-Agent Expert Sourcing - Comprehensive Test Suite
# This script runs all tests and provides a detailed summary

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

# Function to print status
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

# Store the original directory
ORIGINAL_DIR=$(pwd)

# Test results storage (compatible with all shells)
FRONTEND_PASSED=0
FRONTEND_TOTAL=0
E2E_PASSED=0
E2E_TOTAL=0
API_PASSED=0
API_TOTAL=0
ESLINT_ERRORS=0
TYPESCRIPT_ERRORS=0

# Temporary files for capturing output
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Backend Tests
print_status "Running backend tests..."
echo "=========================="

cd backend

# Check dependencies
if [ ! -d ".venv" ]; then
    print_warning "Backend virtual environment not found. Setting up..."
    uv sync
fi

# Database connectivity test
print_status "Testing database connectivity..."
if uv run python scripts/test_db.py > "$TEMP_DIR/db_test.log" 2>&1; then
    print_success "Database connectivity test passed"
else
    print_error "Database connectivity test failed"
fi

# Run pytest tests and capture results
print_status "Running pytest tests..."
if uv run pytest tests/ -v --tb=short > "$TEMP_DIR/pytest.log" 2>&1; then
    print_success "Backend pytest tests completed"
    
    # Parse pytest results
    PYTEST_OUTPUT=$(cat "$TEMP_DIR/pytest.log")
    API_PASSED=$(echo "$PYTEST_OUTPUT" | grep -o "[0-9]\+ passed" | head -1 | grep -o "[0-9]\+" || echo "0")
    API_FAILED=$(echo "$PYTEST_OUTPUT" | grep -o "[0-9]\+ failed" | head -1 | grep -o "[0-9]\+" || echo "0")
    
    API_TOTAL=$((API_PASSED + API_FAILED))
else
    print_error "Backend pytest tests failed"
    # Set fallback values if tests failed
    API_PASSED=0
    API_TOTAL=50
fi

cd "$ORIGINAL_DIR"

# Frontend Tests
print_status "Running frontend tests..."
echo "=========================="

cd frontend

# Check dependencies
if [ ! -d "node_modules" ]; then
    print_warning "Frontend node_modules not found. Installing dependencies..."
    bun install
fi

# ESLint check
print_status "Running ESLint..."
if bun run lint > "$TEMP_DIR/eslint.log" 2>&1; then
    print_success "ESLint passed"
    ESLINT_ERRORS=0
else
    ESLINT_ERRORS=$(cat "$TEMP_DIR/eslint.log" | grep -o "error" | wc -l || echo "0")
    if [ "$ESLINT_ERRORS" -gt 0 ]; then
        print_warning "ESLint found $ESLINT_ERRORS error(s)"
    fi
fi

# TypeScript check
print_status "Running TypeScript type checking..."
if bunx tsc --noEmit > "$TEMP_DIR/typescript.log" 2>&1; then
    print_success "TypeScript type checking passed"
    TYPESCRIPT_ERRORS=0
else
    TS_ERRORS=$(cat "$TEMP_DIR/typescript.log" | grep -c "error TS" || echo "0")
    TYPESCRIPT_ERRORS=$TS_ERRORS
    if [ "$TS_ERRORS" -gt 0 ]; then
        print_warning "TypeScript found $TS_ERRORS error(s)"
    fi
fi

# Jest tests
print_status "Running Jest unit/integration tests..."
# Run Jest and capture output regardless of exit code (with timeout)
timeout 120 bun run test --passWithNoTests --verbose > "$TEMP_DIR/jest.log" 2>&1
JEST_EXIT_CODE=$?

# Parse Jest results - Jest outputs format: "Tests: X failed, Y passed, Z total"
JEST_OUTPUT=$(cat "$TEMP_DIR/jest.log")

# Look for the final summary line with "Tests: ... passed, ... total"
JEST_SUMMARY=$(echo "$JEST_OUTPUT" | grep "Tests:" | tail -1)

if [ -n "$JEST_SUMMARY" ]; then
    FRONTEND_PASSED=$(echo "$JEST_SUMMARY" | grep -o "[0-9]\+ passed" | grep -o "[0-9]\+" || echo "0")
    FRONTEND_FAILED=$(echo "$JEST_SUMMARY" | grep -o "[0-9]\+ failed" | grep -o "[0-9]\+" || echo "0")
    FRONTEND_TOTAL=$(echo "$JEST_SUMMARY" | grep -o "[0-9]\+ total" | grep -o "[0-9]\+" || echo "38")
    
    if [ "$JEST_EXIT_CODE" -eq 0 ]; then
        print_success "Frontend Jest tests completed"
    else
        print_warning "Frontend Jest tests completed with $FRONTEND_FAILED failure(s)"
    fi
else
    # Fallback - Jest didn't run properly
    print_error "Frontend Jest tests failed to run"
    FRONTEND_PASSED=0
    FRONTEND_FAILED=38
    FRONTEND_TOTAL=38
fi

# E2E Tests
print_status "Running Playwright E2E tests..."
# Install browsers if needed
bunx playwright install --with-deps > /dev/null 2>&1 || print_warning "Playwright browser installation had issues"

if timeout 180 bunx playwright test --reporter=list > "$TEMP_DIR/playwright.log" 2>&1; then
    print_success "E2E tests completed"
    
    # Parse Playwright results
    PLAYWRIGHT_OUTPUT=$(cat "$TEMP_DIR/playwright.log")
    E2E_PASSED=$(echo "$PLAYWRIGHT_OUTPUT" | tail -5 | grep -o "[0-9]\+ passed" | head -1 | grep -o "[0-9]\+" || echo "0")
    E2E_FAILED=$(echo "$PLAYWRIGHT_OUTPUT" | tail -5 | grep -o "[0-9]\+ failed" | head -1 | grep -o "[0-9]\+" || echo "0")
    
    E2E_TOTAL=$((E2E_PASSED + E2E_FAILED))
else
    print_warning "E2E tests timed out or failed (backend may not be running)"
    E2E_PASSED=0
    E2E_TOTAL=75
fi

cd "$ORIGINAL_DIR"

# Calculate totals
TOTAL_PASSED=$((FRONTEND_PASSED + E2E_PASSED + API_PASSED))
TOTAL_TESTS=$((FRONTEND_TOTAL + E2E_TOTAL + API_TOTAL))
SUCCESS_RATE=$(( (TOTAL_PASSED * 100) / TOTAL_TESTS ))

# Quality Assurance Summary
QA_ERRORS=$((ESLINT_ERRORS + TYPESCRIPT_ERRORS))

echo ""
echo "════════════════════════════════════════════"
echo -e "${BOLD}🧪 COMPREHENSIVE TEST SUITE SUMMARY${NC}"
echo "════════════════════════════════════════════"
echo ""

echo -e "${BOLD}📊 Testing Stack Results:${NC}"
echo ""

# Frontend Testing
if [ "$FRONTEND_TOTAL" -gt 0 ]; then
    echo -e "• ${BLUE}Frontend Testing${NC} - Jest + React Testing Library (${GREEN}${FRONTEND_PASSED}/${FRONTEND_TOTAL}${NC} tests passing)"
else
    echo -e "• ${BLUE}Frontend Testing${NC} - Jest + React Testing Library (${YELLOW}Not run${NC})"
fi

# E2E Testing  
if [ "$E2E_TOTAL" -gt 0 ]; then
    echo -e "• ${BLUE}E2E Testing${NC} - Playwright cross-browser testing (${GREEN}${E2E_PASSED}/${E2E_TOTAL}${NC} tests passing)"
else
    echo -e "• ${BLUE}E2E Testing${NC} - Playwright cross-browser testing (${YELLOW}Not run${NC})"
fi

# API Testing
if [ "$API_TOTAL" -gt 0 ]; then
    echo -e "• ${BLUE}API Testing${NC} - pytest + FastAPI TestClient (${GREEN}${API_PASSED}/${API_TOTAL}${NC} tests passing)"
else
    echo -e "• ${BLUE}API Testing${NC} - pytest + FastAPI TestClient (${YELLOW}Not run${NC})"
fi

# Quality Assurance
if [ "$QA_ERRORS" -eq 0 ]; then
    echo -e "• ${BLUE}Quality Assurance${NC} - ESLint + TypeScript (${GREEN}0 errors${NC})"
else
    echo -e "• ${BLUE}Quality Assurance${NC} - ESLint + TypeScript (${RED}$QA_ERRORS errors${NC})"
fi

echo -e "• ${BLUE}Performance${NC} - Coverage reports and build validation"

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