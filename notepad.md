# Project Notepad: Python Project Starter

This file contains notes, observations, design decisions, and potential improvements tracked during the development of the Python Project Starter library.

## Initial Thoughts & Setup

*   Project initialized following modern Python best practices (UV, Ruff, pyproject.toml, src layout).
*   Target audience: Non-technical users needing simplified project creation and Git workflow.
*   Pre-commit hook installation encountered issues in the integrated terminal (PowerShell environment complexity suspected). Needs verification/alternative setup later.

## Phase 2 - Core Development Notes

*   ~~**(Current)** Starting with CLI structure using Typer.~~ Basic CLI structure with Typer and placeholder commands (`new`, `save`, `sync`) is implemented and working.
*   ~~**(Current)** Starting implementation of the `new` command logic in `src/project_starter/main.py`.~~ Implemented directory creation.
*   Created template files (`_gitignore.template`, `_readme.md.template`, `_pyproject.toml.template`) within `src/project_starter/templates`.
*   Updated `pyproject.toml` (in the starter library project) to include templates in package data using `[tool.hatch.build.targets.wheel.force-include]`.
*   Updated `new` command in `main.py` to use `importlib.resources` to load templates, replace placeholders (`{project_name}`, `{package_name}`), and write files to the *new* project directory.
*   Added basic validation for project name format (lowercase_with_underscores).
*   Added `--dir` option to `new` command to specify target directory.
*   ~~**(Current)** Need to implement `git init` and `uv venv` steps within the `new` command, or guide the user to run them manually after creation.~~ Implemented automatic execution of `git init` and `uv venv && uv sync --dev` using `subprocess` within the `new` command. Added basic error handling/warnings for these steps.
*   ~~**(Current)** Need to implement simplified Git wrappers (`save`, `sync`).~~ Implemented the `save` command (`git add .` + `git commit -m msg`). Assumes running from project root.
*   ~~**(Current)** Need to implement the `sync` command.~~ Implemented the `sync` command (`git pull` + `git push`). Assumes running from project root and remote/upstream is configured.
*   ~~**(Current)** Consider adding a simple status check command.~~ Added `status` command (runs `git status -s`).
*   ~~**(Current)** Review error handling in Git commands (e.g., what if pull fails due to conflicts, what if push fails due to no upstream).~~ Added basic checks for 'nothing to commit' and 'already up-to-date'. More complex Git error states (merge conflicts, auth issues) are not handled gracefully yet.
*   ~~**(Current)** Phase 2 (Core commands) is mostly complete. Next steps involve Phase 3 (Tooling Integration - Ruff, Mypy, Pre-commit) or Phase 4 (Documentation) / Phase 5 (Testing).~~

## Phase 3 - Tooling Integration Notes

*   ~~**(Current)** Starting Phase 3. Running Ruff format and check.~~ Ran `ruff format .` and `ruff check --fix .`. Fixed one remaining `PTH123` error manually. Codebase now passes Ruff checks.
*   ~~**(Current)** Next: Integrate Type Checking (Pyright).~~ Added mypy configuration in pyproject.toml and fixed type errors in the codebase. Key change was properly typing the subprocess.run result with CompletedProcess[str] and fixing a variable redefinition.
*   ~~**(Current)** Next: Integrate Pre-commit hooks.~~ Updated `.pre-commit-config.yaml` to include mypy type checking and installed pre-commit hooks. Fixed some whitespace and file ending issues automatically detected by the hooks.
*   ~~**(Current)** Next: Move to Phase 4 - Documentation~~ Completed documentation phase with the following:
    * Created comprehensive user guide in docs/user_guide.md targeting non-technical users
    * Improved docstrings throughout the codebase using Google-style format
    * Enhanced the README.md with project description, installation instructions, and usage examples
*   ~~**(Current)** Next: Move to Phase 5 - Testing~~ Completed most of the testing phase:
    * Set up pytest configuration in pyproject.toml
    * Created unit tests for helper functions (_create_directory, _create_file, _read_template, _run_command)
    * Added CLI command tests using Typer's CliRunner
    * Implemented integration tests for the end-to-end flow
    * Note: There were some environment issues running the tests, but the test structure is in place
*   ~~**(Current)** Next: Move to Phase 6 - Packaging & Distribution~~ Completed Phase 6 - Packaging & Distribution:
    * Built the package successfully using Hatch (`hatch build`)
    * Successfully installed the package in a clean environment
    * Verified the `pps` command works as expected
    * Created a test project using `pps new test_project` in a clean environment
    * Confirmed all files and directories are created correctly (src layout, pyproject.toml, etc.)
    * The only remaining task in Phase 6 is publishing to PyPI (optional)
*   ~~**(Current)** Next: Move to Phase 7 - CI/CD and set up GitHub Actions for linting, testing, and building~~ Completed Phase 7 - CI/CD:
    * Created `.github/workflows/python-ci.yml` with jobs for:
      * Linting (ruff format check and ruff lint check)
      * Type checking (mypy)
      * Testing (pytest across Python 3.10, 3.11, and 3.12)
      * Building (hatch build)
      * Publishing to PyPI on tag release (conditional)
    * Each step uses proper dependency installation with pip/uv
    * Set up artifacts to store built packages between jobs
*   ~~**(Current)** Next: Move to Phase 8 - Refinement & User Feedback:~~
    * Plan and execute user testing with non-technical users
    * Create a feedback collection mechanism (e.g., GitHub issues)
    * Identify common pain points and usability issues
    * Plan for improvements based on feedback

## Phase 3 - Additional Features

*   ~~**(Current)** Starting implementation of the `save` command logic in `src/project_starter/main.py`.~~
*   ~~**(Current)** Starting implementation of the `sync` command logic in `src/project_starter/main.py`.~~
*   ~~**(Current)** Starting implementation of the `git init` command logic in `src/project_starter/main.py`.~~
*   ~~**(Current)** Starting implementation of the `uv venv` command logic in `src/project_starter/main.py`.~~
*   ~~**(Current)** Starting implementation of the `new` command logic in `src/project_starter/main.py`.~~
*   ~~**(Current)** Need to implement simplified Git wrappers (`save`, `sync`).~~
*   ~~**(Current)** Phase 2 (Core commands) is mostly complete. Next steps involve Phase 3 (Tooling Integration - Ruff, Mypy, Pre-commit) or Phase 4 (Documentation) / Phase 5 (Testing).~~

## Atualizações de Dependências e Ferramentas (Maio 2024)

*   ~~**(Current)** Identificada a necessidade de atualizar UV e Ruff para versões mais recentes:~~
    * UV: 0.1.18 → 0.2.24
    * Ruff: 0.3.0 → 0.6.0+

*   ~~**(Current)** Criado documento `atualizacao.md` detalhando os pontos de atualização necessários:~~
    * Atualização dos comandos UV no código (especialmente substituir `uv sync --dev` por `uv pip install -e ".[dev]"`)
    * Ativação do modo preview do Ruff para recurso experimentais
    * Adição de novas regras de lint no Ruff (RET, SLF, ARG, ERA, etc.)
    * Atualização do template _pyproject.toml.template para refletir as novas versões
    * Modificação do pipeline CI/CD para utilizar as versões mais recentes

*   ~~**(Current)** Próximos passos imediatos:~~
    * ~~Atualizar pyproject.toml do projeto principal~~ **Concluído:** Atualizados UV para 0.2.0+ e Ruff para 0.6.0+
    * ~~Modificar o código em main.py para utilizar os novos comandos UV~~ **Concluído:** Substituído `uv sync --dev` por `uv pip install -e ".[dev]"`
    * ~~Testar a instalação e uso com as novas versões~~ **Concluído:** Instalação e testes realizados com sucesso
    * ~~Verificar compatibilidade com projetos existentes~~ **Concluído:** Compatibilidade verificada

*   ~~**(Current)** Lista de arquivos que precisam ser atualizados:~~
    * ✓ pyproject.toml (principal) - Atualizado
    * ✓ src/project_starter/main.py (código) - Atualizado
    * ✓ src/project_starter/templates/_pyproject.toml.template (template) - Atualizado
    * ✓ .github/workflows/python-ci.yml (CI/CD) - Atualizado
    * ✓ README.md - Atualizado

*   **Próximas melhorias futuras:**
    * Considerar a adição de mais exemplos na documentação sobre os novos comandos UV
    * Monitorar atualizações de Ruff e UV para futuras melhorias
    * Implementar testes automatizados para verificar compatibilidade com novas versões

# Plano Detalhado para Fase 8 - Testes com Usuários

Após a publicação bem-sucedida do projeto no GitHub em https://github.com/arthur0211/python-project-starter, o foco agora deve ser na obtenção de feedback de usuários reais.
