# Contributing to Python Project Starter

Thank you for your interest in contributing to Python Project Starter! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. **Fork the repository**

   Start by forking the [Python Project Starter repository](https://github.com/arthur0211/python-project-starter).

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR-USERNAME/python-project-starter.git
   cd python-project-starter
   ```

3. **Set up the development environment**

   ```bash
   # Create a virtual environment using UV (recommended)
   uv venv

   # Activate the virtual environment
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate

   # Install development dependencies
   uv sync --dev

   # Install the package in development mode
   pip install -e .

   # Install pre-commit hooks
   pre-commit install
   ```

## Development Workflow

1. **Create a branch for your feature or bugfix**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-you-are-fixing
   ```

2. **Make your changes**

   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests and linting**

   ```bash
   # Run tests
   pytest

   # Run linting checks
   ruff check .
   ruff format --check .

   # Run type checking
   mypy src
   ```

4. **Commit your changes**

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test changes
   - `chore:` for maintenance tasks

   Example:
   ```bash
   git commit -m "feat: add support for custom templates"
   ```

5. **Push your changes**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a pull request**

   - Go to the [Python Project Starter repository](https://github.com/arthur0211/python-project-starter)
   - Click "Pull requests" and then "New pull request"
   - Click "compare across forks"
   - Select your fork and branch
   - Click "Create pull request"

## Code Standards

- **PEP 8**: Follow PEP 8 conventions, which are enforced by Ruff
- **Type Hints**: Use type hints on all functions and methods
- **Docstrings**: Use Google-style docstrings for all public functions, classes, and methods
- **Tests**: Add tests for all new functionality

## Areas for Contribution

We particularly welcome contributions in these areas:

1. **Error Handling Improvements**
   - Better error messages for common Git issues
   - More robust handling of environmental issues

2. **Template Additions**
   - Templates for specific project types (web, data science, etc.)
   - Improved configuration files

3. **Documentation Enhancements**
   - Clearer examples for non-technical users
   - Translations of documentation

4. **Core Functionality**
   - Additional commands for common workflow tasks
   - Performance improvements

## Questions?

If you have any questions about contributing, feel free to open an issue on GitHub or reach out to the maintainers directly.

Thank you for helping improve Python Project Starter!
