.PHONY: help install-all dev-backend dev-frontend dev-all test-all clean-all

# Default target
help:
	@echo "🚀 Multi-Agent Expert Sourcing Project"
	@echo ""
	@echo "Available commands:"
	@echo "  make install-all     - Install dependencies for both backend and frontend"
	@echo "  make dev-backend     - Start backend development server"
	@echo "  make dev-frontend    - Start frontend development server"
	@echo "  make dev-all         - Start both backend and frontend (in background)"
	@echo "  make test-all        - Run all tests (backend and frontend)"
	@echo "  make clean-all       - Clean all cache and temporary files"
	@echo ""
	@echo "Backend-specific commands (from backend directory):"
	@echo "  cd backend && make help"

# Install dependencies for both backend and frontend
install-all:
	@echo "🔧 Installing all dependencies..."
	cd backend && make install
	cd frontend && make install
	@echo "✅ All dependencies installed successfully"

# Start backend development server
dev-backend:
	@echo "🚀 Starting backend server..."
	cd backend && make dev

# Start frontend development server
dev-frontend:
	@echo "🚀 Starting frontend server..."
	cd frontend && make dev

# Start both services (backend in background, frontend in foreground)
dev-all:
	@echo "🚀 Starting both backend and frontend servers..."
	@echo "🔙 Backend will run in background on port 8000"
	@echo "🎨 Frontend will run in foreground on port 3000"
	cd backend && uv run uvicorn main:app --reload --port 8000 &
	sleep 3
	cd frontend && bun dev

# Run all tests
test-all:
	@echo "🧪 Running all tests..."
	./test-all.sh

# Clean all cache and temporary files
clean-all:
	@echo "🧹 Cleaning all cache and temporary files..."
	cd backend && make clean
	cd frontend && make clean
	@echo "✅ All cleanup complete"

# Quick setup for new developers
setup: install-all
	@echo "🎯 Project setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Configure your .env file in backend/ directory"
	@echo "2. Run 'make dev-backend' to start the backend"
	@echo "3. Run 'make dev-frontend' to start the frontend"
	@echo "4. Or run 'make dev-all' to start both services"
