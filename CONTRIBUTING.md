# Contributing to Apple Wallet Card Generator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/wallet-card-generator.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Install development dependencies: `make install-dev`

## Development Workflow

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint
```

### Project Structure

- `src/wallet_card/` - Main source code
- `tests/` - Test suite
- `config/` - Configuration examples
- `docker/` - Docker configuration

## Coding Standards

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Write tests for new features

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add support for custom templates
fix: Resolve image resizing issue
docs: Update README with new examples
test: Add tests for validator module
```

## Pull Request Process

1. Ensure all tests pass: `make test`
2. Ensure code is formatted: `make format`
3. Ensure linters pass: `make lint`
4. Update documentation if needed
5. Submit pull request with clear description

## Adding New Features

### New Templates

1. Create a new template class in `src/wallet_card/templates/`
2. Extend `BaseTemplate`
3. Implement `get_template_config()` method
4. Add tests in `tests/`
5. Update documentation

### New CLI Commands

1. Add command to `src/wallet_card/cli/commands.py`
2. Use Click decorators
3. Add help text and examples
4. Update README

## Questions?

Feel free to open an issue for questions or discussions!

