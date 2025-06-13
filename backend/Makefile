.PHONY: help install test test-db dev clean lint format

# Default target
help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies and sync environment"
	@echo "  make test-db    - Test database connection"
	@echo "  make test       - Run all tests"
	@echo "  make dev        - Start development server"
	@echo "  make clean      - Clean cache and temporary files"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code"

# Install dependencies and sync environment
install:
	@echo "🔧 Installing dependencies with uv..."
	uv sync
	@echo "✅ Dependencies installed successfully"

# Test database connection
test-db:
	@echo "🔗 Testing database connection..."
	uv run python test_db.py

# Run all tests
test:
	@echo "🧪 Running tests..."
	uv run pytest tests/ -v

# Start development server
dev:
	@echo "🚀 Starting backend development server..."
	@echo "📍 Make sure you're in the backend directory"
	@echo "🔗 Server will be available at http://localhost:8000"
	@echo "📖 API docs available at http://localhost:8000/docs"
	uv run uvicorn main:app --reload --port 8000

# Clean cache and temporary files
clean:
	@echo "🧹 Cleaning cache and temporary files..."
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -f .coverage
	rm -f test.db
	@echo "✅ Cleanup complete"

# Run linting (future enhancement)
lint:
	@echo "🔍 Running linting checks..."
	uv run python -m py_compile *.py
	@echo "✅ Linting complete"

# Format code (future enhancement)
format:
	@echo "🎨 Formatting code..."
	@echo "⚠️  Code formatting not configured yet"

# Development workflow - install and test before starting
setup: install test-db
	@echo "🎯 Backend setup complete! Ready for development."
	@echo "📝 Run 'make dev' to start the development server" 