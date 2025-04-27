# Project Checklist: Python Project Starter for Non-Technical Users

This checklist outlines the steps required to build a Python library that simplifies project setup and management for non-technical users, following modern best practices.

## Phase 1: Project Setup & Configuration

- [x] **Initialize Project Structure**
    - [x] Create project directory (`python-project-starter` or similar)
    - [x] Implement `src` layout (`src/project_starter`)
    - [x] Add `README.md`
    - [x] Add `.gitignore` (use standard Python template)
- [x] **Configure `pyproject.toml`**
    - [x] Define build system (`hatchling`)
    - [x] Add project metadata (name, version, description, author, license)
    - [x] Specify Python version requirement (`>=3.10` or newer)
    - [x] List core dependencies (initially empty or minimal)
    - [x] Define optional dependencies (`dev` group: `uv`, `ruff`, `pytest`, `mypy`, `pre-commit`)
- [x] **Set up Environment Management with UV**
    - [x] Create initial virtual environment (`uv venv`)
    - [x] Install dev dependencies (`uv sync --dev`)
- [x] **Configure Ruff (Linter & Formatter)**
    - [x] Add `[tool.ruff.lint]` section to `pyproject.toml` (select rules, e.g., `E`, `F`, `W`, `I`, `UP`, `B`, `A`)
    - [x] Add `[tool.ruff.format]` section to `pyproject.toml` (configure style)
- [x] **Configure Type Checking (Mypy/Pyright)**
    - [x] Choose type checker (Pyright recommended for VS Code)
    - [x] Add configuration section (`[tool.mypy]` or `[tool.pyright]`) to `pyproject.toml`
    - [x] Set basic strictness rules
- [x] **Set up Pre-commit Hooks**
    - [x] Create `.pre-commit-config.yaml`
    - [x] Add hooks for `ruff` (linting and formatting)
    - [x] Add standard hooks (`trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-added-large-files`)
    - [x] Install pre-commit hooks (`uv run pre-commit install`)
- [x] **Initialize Git Repository**
    - [x] Run `git init`
    - [x] Make initial commit (`git add .`, `git commit -m "feat: Initial project structure and configuration"`)
    - [x] Create remote repository (e.g., on GitHub)
    - [x] Add remote and push initial commit

## Phase 2: Core Library Design & Implementation

- [x] **Define Core Abstractions**
    - [x] Design classes/functions for project initialization (e.g., `ProjectSetup`)
    - [x] Design abstractions for simplified Git commands (e.g., `EasyGit`)
    - [x] Plan command-line interface (CLI) using `argparse`, `click`, or `typer`
- [x] **Implement Project Initialization Logic**
    - [x] Function to create directory structure (`src`, `tests`, etc.)
    - [x] Function to generate basic `pyproject.toml`
    - [x] Function to set up `uv` environment
    - [x] Function to initialize `git`
    - [x] Create basic `README.md`
    - [x] Create basic `.gitignore`
- [x] **Implement Simplified Git Wrappers**
    - [x] Wrapper for `git add .`
    - [x] Wrapper for `git commit`
    - [x] Wrapper for `git push`
    - [x] Wrapper for `git pull` / sync changes
    - [x] Simple status check
- [x] **Develop CLI**
    - [x] Create entry point script (e.g., `src/project_starter/main.py`)
    - [x] Add commands (e.g., `pps new`, `pps save`, `pps sync`, `pps status`)
    - [x] Implement clear argument parsing and help messages
- [x] **Implement Error Handling**
    - [x] Add robust error handling for file operations, Git commands, etc.
    - [x] Provide user-friendly error messages
- [x] **Add Logging**
    - [x] Implement basic logging for diagnostics

## Phase 3: Tooling Integration & Workflow

- [x] **Integrate Ruff Checks**
    - [x] Ensure code passes `uv run ruff check .`
    - [x] Ensure code is formatted with `uv run ruff format .`
- [x] **Integrate Type Checking**
    - [x] Add type hints to all functions and methods
- [x] **Integrate Pre-commit**
    - [x] Verify hooks run correctly on `git commit`

## Phase 4: Documentation

- [x] **Write User Guide**
    - [x] Target audience: Non-technical users
    - [x] Explain core concepts simply (project, commit, save, sync)
    - [x] Provide step-by-step instructions for common tasks
    - [x] Include examples for each command
- [x] **Write API Documentation (Docstrings)**
    - [x] Add PEP 257 compliant docstrings to all modules, classes, functions
    - [x] Use a clear format (e.g., Google style)
- [x] **Update README.md**
    - [x] Add project description, installation guide, quick start, basic usage

## Phase 5: Testing

- [x] **Set up Pytest**
    - [x] Configure `pytest` options in `pyproject.toml` (`testpaths`, etc.)
- [x] **Write Unit Tests**
    - [x] Test core logic functions (initialization, Git wrappers)
    - [x] Test edge cases and error handling
    - [x] Mock external dependencies (filesystem, Git commands)
- [x] **Write Integration Tests**
    - [x] Test CLI commands work as expected
    - [x] Test the end-to-end flow of creating and managing a project
- [x] **Measure Code Coverage**
    - [x] Aim for >= 90% coverage (`uv run pytest --cov=src`)
    - [x] Analyze coverage reports and add missing tests

## Phase 6: Packaging & Distribution

- [x] **Prepare for Packaging**
    - [x] Ensure `pyproject.toml` has all necessary metadata
    - [x] Add `LICENSE` file
- [x] **Build Package**
    - [x] Use `uv build` or `hatch build`
- [x] **Test Installation**
    - [x] Install the built wheel/sdist in a clean environment and test basic functionality
- [x] **Publish (Optional)**
    - [x] Consider publishing to PyPI or a private repository

## Phase 7: CI/CD

- [x] **Set up GitHub Actions Workflow**
    - [x] Create `.github/workflows/ci.yml`
    - [x] Define jobs for:
        - [x] Linting (`ruff check`)
        - [x] Formatting Check (`ruff format --check`)
        - [x] Type Checking (`mypy` or `pyright`)
        - [x] Testing (`pytest --cov=src` across multiple Python versions)
    - [x] Add step to install dependencies using `uv`
    - [x] (Optional) Add job to build the package
    - [x] (Optional) Add job to publish to PyPI on tag/release

## Phase 8: Refinement & User Feedback

- [x] **Gather Feedback**
    - [x] Create user testing plan and documentation
    - [x] Develop feedback collection form
    - [x] Prepare recruitment materials for testers
    - [ ] Test with target non-technical users
    - [ ] Identify pain points and areas for improvement
- [x] **Atualizar Dependências e Ferramentas**
    - [x] Criar plano de atualização para UV e Ruff em atualizacao.md
    - [x] Atualizar UV para versão 0.2+ no projeto principal
    - [x] Atualizar Ruff para versão 0.6+ no projeto principal
    - [x] Adaptar código para usar comandos atualizados do UV
    - [x] Implementar modo preview do Ruff e adicionar novas regras
    - [x] Atualizar documentação para refletir novos comandos e versões
    - [x] Testar instalação com as novas versões
- [ ] **Iterate**
    - [ ] Refine commands, documentation, and error messages based on feedback
