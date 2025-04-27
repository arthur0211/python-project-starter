# Python Project Starter (PPS)

A tool to help non-technical users initialize and manage Python projects with professional standards. This tool simplifies project creation and common Git operations with easy-to-use commands.

## Features

- **Simple Project Creation**: Create new Python projects with proper structure and configuration
- **Modern Tooling Setup**: Automatically configures industry-standard tools like Ruff and Mypy
- **Git Made Easy**: Simplified Git commands for saving and syncing changes
- **Best Practices Built-in**: Follows Python community standards for project structure and tooling

## Project Status

**Current Development Stage**: Beta

This project is currently in active development with most core features implemented. We're now in the user testing phase and seeking feedback from non-technical Python users.

**Next Steps**:
- Conducting user testing sessions (planned for May 2025)
- Implementing improvements based on feedback
- Publishing to PyPI for wider availability

**Contribution Status**: Open to contributions, especially for:
- Improving error handling
- Adding more templates
- Enhancing documentation
- Fixing identified bugs

## Installation

### Prerequisites

- Python 3.10 or higher
- Git installed and configured on your system
- UV package manager (recommended)

### Install from PyPI

```bash
# Using pip
pip install python-project-starter

# Using UV (recommended)
uv pip install python-project-starter
```

### Install for Development

```bash
# Clone the repository
git clone https://github.com/arthur0211/python-project-starter.git
cd python-project-starter

# Create a virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"

# Install the package in development mode
# Already done by the command above
```

## Quick Start

### Creating a New Project

```bash
# Create a new project in the current directory
pps new my_project

# Create in a specific directory
pps new my_project --dir /path/to/directory
```

This will:
1. Create project directory structure with `src` layout
2. Set up a proper `pyproject.toml` with modern configurations
3. Initialize a Git repository
4. Create a virtual environment with essential development tools

### Saving Your Changes

After making changes to your code, save them to Git:

```bash
# Save changes with a descriptive message
pps save -m "Add new feature X"
```

This single command replaces the traditional Git workflow:
```bash
git add .
git commit -m "Add new feature X"
```

### Syncing with Remote Repository

Update your local code with remote changes and share your work:

```bash
# Pull remote changes and push your local changes
pps sync
```

This combines:
```bash
git pull
git push
```

### Checking Project Status

```bash
# See the status of your project
pps status
```

## Command Reference

| Command | Description |
|---------|-------------|
| `pps new NAME` | Create a new Python project |
| `pps save -m "MESSAGE"` | Save changes to Git |
| `pps sync` | Sync with remote repository |
| `pps status` | Check project status |

## Project Structure

Projects created with PPS follow the recommended "src layout":

```
my_project/
├── README.md
├── pyproject.toml
├── src/
│   └── my_project/
│       └── __init__.py
└── tests/
```

## CI/CD

This project includes GitHub Actions workflows that automatically:

- Run linting checks with Ruff
- Perform type checking with Mypy
- Run tests with pytest across multiple Python versions
- Build the package for distribution
- Optionally publish to PyPI when tags are created

## User Feedback

We value user feedback to improve PPS for non-technical users. The project includes:

- Comprehensive user testing plan
- Feedback collection forms
- Recruitment materials for testers

If you're interested in participating in user testing, please see the [user testing documentation](docs/user_testing_plan.md).

## Why Use PPS?

- **For Beginners**: Simplifies project setup and version control
- **For Teams**: Ensures consistent project structure and tooling
- **For Everyone**: Reduces cognitive load when managing Python projects

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
