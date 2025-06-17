"""
Integration Tests Package

This package contains tests that:
- Make real API calls to external services (OpenAI, etc.)
- Require specific environment setup
- Take longer to run (> 30 seconds)
- Are suitable for CI/CD pipeline but not local pre-commit hooks

These tests are run separately from the fast unit tests to maintain
a clear distinction between different test categories.
"""
