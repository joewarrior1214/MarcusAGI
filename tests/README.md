# Tests Directory

This directory contains all test files for Marcus AGI systems.

## Structure

- **`integration/`** - Integration tests that test multiple systems working together
- **`systems/`** - Unit tests for individual systems and components
- **`utilities/`** - Test utilities and helper functions

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/systems/
python -m pytest tests/integration/

# Run with coverage
python -m pytest tests/ --cov=core
```

## Test Coverage Goals
- Core systems: 90%+ coverage
- Integration points: 85%+ coverage
- Critical paths: 100% coverage
