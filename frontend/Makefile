.PHONY: help install test test-unit test-e2e test-all dev build start clean lint format type-check

# Default target
help:
	@echo "Frontend Commands:"
	@echo "  make install      - Install dependencies with Bun"
	@echo "  make dev          - Start development server"
	@echo "  make build        - Build for production"
	@echo "  make start        - Start production server"
	@echo "  make test         - Run unit tests"
	@echo "  make test-e2e     - Run E2E tests with Playwright"
	@echo "  make test-all     - Run all tests and linting"
	@echo "  make lint         - Run ESLint"
	@echo "  make type-check   - Run TypeScript type checking"
	@echo "  make clean        - Clean build artifacts and cache"
	@echo "  make format       - Format code (future enhancement)"

# Install dependencies with Bun
install:
	@echo "📦 Installing frontend dependencies with Bun..."
	bun install
	@echo "✅ Frontend dependencies installed successfully"

# Start development server
dev:
	@echo "🚀 Starting frontend development server..."
	@echo "🎨 Next.js will be available at http://localhost:3000"
	bun dev

# Build for production
build:
	@echo "🏗️  Building frontend for production..."
	bun run build
	@echo "✅ Frontend build complete"

# Start production server
start: build
	@echo "🌟 Starting production frontend server..."
	bun start

# Run unit tests
test:
	@echo "🧪 Running frontend unit tests..."
	bun run test

# Run unit tests with coverage
test-coverage:
	@echo "🧪 Running frontend tests with coverage..."
	bun run test:coverage

# Run E2E tests
test-e2e:
	@echo "🎭 Running E2E tests with Playwright..."
	@echo "⚠️  Make sure backend is running on http://localhost:8000"
	bun run test:e2e

# Run E2E tests with UI
test-e2e-ui:
	@echo "🎭 Running E2E tests with Playwright UI..."
	bun run test:e2e:ui

# Run all tests (unit + lint + build)
test-all:
	@echo "🧪 Running all frontend tests and checks..."
	bun run test:all

# Run ESLint
lint:
	@echo "🔍 Running ESLint..."
	bun run lint

# Run TypeScript type checking
type-check:
	@echo "🔍 Running TypeScript type checking..."
	bunx tsc --noEmit

# Clean build artifacts and cache
clean:
	@echo "🧹 Cleaning frontend build artifacts and cache..."
	rm -rf .next/
	rm -rf coverage/
	rm -rf test-results/
	rm -rf playwright-report/
	rm -rf node_modules/.cache/
	rm -f tsconfig.tsbuildinfo
	@echo "✅ Frontend cleanup complete"

# Format code (future enhancement)
format:
	@echo "🎨 Formatting frontend code..."
	@echo "⚠️  Code formatting not configured yet"
	@echo "💡 Consider adding Prettier configuration"

# Development setup - install and verify
setup: install type-check
	@echo "🎯 Frontend setup complete! Ready for development."
	@echo "📝 Run 'make dev' to start the development server"

# Quick health check
health:
	@echo "🩺 Frontend health check..."
	@echo "📦 Checking Bun version:"
	@bun --version
	@echo "📝 Checking TypeScript:"
	@bunx tsc --version
	@echo "✅ Frontend environment healthy" 