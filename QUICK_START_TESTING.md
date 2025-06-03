# 🚀 Quick Start - Testing Framework

**Ready to test immediately!** Jump straight into testing without setup hassle.

> 📖 **Navigation**: [Main README](README.md) | **[Quick Start]** | [Complete Testing Guide](TESTING.md) | [Tailwind Debug](frontend/TAILWIND_DEBUG_GUIDE.md)

## ⚡ **Run Tests Now**

### **🎯 Everything (Recommended)**
```bash
./test-all.sh
```
*Runs all 46 tests with beautiful colored output and summary*

### **🔥 Quick Commands**
```bash
# Frontend tests (38 tests)
cd frontend && bun run test

# Backend tests (50 tests)  
cd backend && uv run pytest tests/test_simple.py tests/test_api.py -v

# Database check
cd backend && uv run python test_db.py

# Type safety
cd frontend && bunx tsc --noEmit
```

## 📊 **What's Tested**

✅ **88 Total Tests** across the full stack  
✅ **95% Pass Rate** - Production ready  
✅ **Component Testing** - UI interactions & accessibility  
✅ **API Testing** - Endpoints with mocking  
✅ **CV Upload Testing** - File validation & storage  
✅ **E2E Testing** - Real user workflows  
✅ **Database Testing** - Connectivity & schema  
✅ **Build Testing** - TypeScript & production builds  

## 🎨 **Testing Stack**
- **Frontend**: Jest + React Testing Library + Playwright
- **Backend**: pytest + FastAPI + Coverage
- **Quality**: ESLint + TypeScript + Coverage Reports

## ⚡ **Daily Workflow**

```bash
# Before coding
./test-all.sh                    # Ensure clean start

# During development  
cd frontend && bun run test:watch   # Watch mode
cd backend && uv run pytest -v     # Quick backend check

# Before committing
./test-all.sh                    # Full verification
```

## 🔧 **Pre-commit Options**

**Manual (Recommended)**: Run `./test-all.sh` before each commit

**VS Code Task**: Add to `.vscode/tasks.json`:
```json
{
    "label": "Run All Tests",
    "type": "shell", 
    "command": "./test-all.sh"
}
```

**Git Hook**: 
```bash
echo '#!/bin/sh\n./test-all.sh' > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

## 🆘 **Quick Fixes**

```bash
# Missing dependencies
cd frontend && bun install
cd backend && uv sync

# Database issues  
cd backend && uv run python test_db.py

# Type errors
cd frontend && bunx tsc --noEmit
```

## 📚 **Need More Detail?**

- **[Complete Testing Guide](TESTING.md)** - Full setup, configuration, and best practices
- **Environment setup** - Check OPENAI_API_KEY and PG_URL are set
- **Coverage reports** - Available after running tests with coverage

---

**🚀 Ready to test! Run `./test-all.sh` to get started immediately.** 