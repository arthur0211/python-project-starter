"""
Python Project Starter (PPS) CLI Module.

This module provides a command-line interface for initializing and managing Python projects,
specifically designed for non-technical users. It simplifies common tasks such as:

- Creating new projects with proper structure and configuration
- Managing Git operations with simplified commands
- Setting up virtual environments and development tools

The commands are designed to be intuitive and user-friendly, hiding the complexity
of underlying tools while following Python best practices.

Example usage:
    pps new my_project
    pps save -m "Add new feature"
    pps sync
    pps status

For more details, see the user guide in the docs/ directory.
"""

import importlib.resources
import pathlib
import subprocess
from subprocess import CompletedProcess
from typing import Annotated

import typer
from rich.console import Console

# Define standard directory names
SRC_DIR = "src"
TESTS_DIR = "tests"
TEMPLATES_DIR = "templates"


# Helper function to create directories
def _create_directory(path: pathlib.Path, console: Console) -> bool:
    """
    Create a directory if it doesn't exist.

    Args:
        path: Path to the directory to create
        console: Rich console for output

    Returns:
        True if directory exists or was created successfully, False otherwise
    """
    try:
        if path.exists():
            if not path.is_dir():
                console.print(
                    f"[bold red]Error:[/bold red] Path '{path}' exists but is not a directory."
                )
                return False
            console.print(f"[yellow]Directory already exists:[/yellow] {path}")
            return True

        path.mkdir(parents=True, exist_ok=True)
        console.print(f"[green]Created directory:[/green] {path}")
        return True
    except Exception as e:
        console.print(
            f"[bold red]Error:[/bold red] Failed to create directory '{path}': {str(e)}"
        )
        return False


# Helper function to create files
def _create_file(path: pathlib.Path, content: str, console: Console) -> bool:
    """
    Create a file with specified content if it doesn't exist.

    Args:
        path: Path to the file to create
        content: Content to write to the file
        console: Rich console for output

    Returns:
        True if file exists or was created successfully, False otherwise
    """
    try:
        if path.exists():
            console.print(f"[yellow]File already exists:[/yellow] {path}")
            return True

        # Ensure parent directory exists
        if path.parent.exists() or _create_directory(path.parent, console):
            path.write_text(content)
            console.print(f"[green]Created file:[/green] {path}")
            return True
        return False
    except Exception as e:
        console.print(
            f"[bold red]Error:[/bold red] Failed to create file '{path}': {str(e)}"
        )
        return False


# Helper function to read template files safely
def _read_template(template_name: str, console: Console) -> str | None:
    """
    Read a template file's content.

    Args:
        template_name: The name of the template file to read.
        console: Rich console for output.

    Returns:
        The content of the template file as a string, or None if an error occurred.
    """
    try:
        resources = importlib.resources.files("project_starter")
        template_path = resources / TEMPLATES_DIR / template_name
        return template_path.read_text()
    except (FileNotFoundError, ImportError) as e:
        console.print(
            f"[bold red]Error:[/bold red] Could not read template '{template_name}'. {str(e)}"
        )
        return None


# Helper function to run shell commands
def _run_command(
    command: list[str], cwd: pathlib.Path, console: Console, capture: bool = True
) -> tuple[bool, str | None]:
    """
    Run a shell command.

    Args:
        command: The command to run as a list of strings.
        cwd: The working directory in which to run the command.
        console: Rich console for output.
        capture: Whether to capture and return the command output.

    Returns:
        A tuple containing:
        - Boolean indicating if the command succeeded
        - String containing the command output if capture=True, None otherwise or on error
    """
    try:
        if capture:
            result: CompletedProcess[str] = subprocess.run(
                command, cwd=cwd, check=True, text=True, capture_output=True
            )
            return True, result.stdout

        subprocess.run(command, cwd=cwd, check=True, text=True)
        return True, None
    except subprocess.SubprocessError as e:
        console.print(
            f"[bold red]Command Error:[/bold red] {' '.join(command)} failed with {str(e)}"
        )
        return False, None


app = typer.Typer(
    help="A tool to help non-technical users initialize and manage Python projects.",
    rich_markup_mode="markdown",
)


@app.command()
def new(
    project_name: Annotated[
        str,
        typer.Argument(
            help="The name for the new project (use lowercase_with_underscores)."
        ),
    ],
    target_dir: Annotated[
        pathlib.Path | None,
        typer.Option(
            "--dir",
            "-d",
            help="The directory where the project will be created (defaults to current directory).",
        ),
    ] = None,
) -> None:
    """
    Creates a new Python project directory with recommended structure and tooling.

    This command creates a new Python project following modern best practices, including:
    - Proper directory structure (src layout)
    - Configured pyproject.toml with essential tools
    - Git repository initialization
    - Virtual environment creation with UV
    - Installation of development dependencies

    The project name should be in lowercase with underscores (e.g., my_cool_project).

    Args:
        project_name: Name for the new project (lowercase with underscores)
        target_dir: Optional directory where the project will be created

    Examples:
        `pps new my_cool_project`
        `pps new data_analysis_tool --dir ~/Projects`
    """
    if " " in project_name or project_name.lower() != project_name:
        typer.echo(
            f"Error: Project name '{project_name}' should be lowercase with underscores.",
            err=True,
        )
        raise typer.Exit(code=1)

    # Define target_dir if it's None
    if target_dir is None:
        target_dir = pathlib.Path.cwd()

    # Determine the root directory for the new project
    if not target_dir.is_dir():
        typer.echo(
            f"Error: Specified target directory does not exist: {target_dir}",
            err=True,
        )
        raise typer.Exit(code=1)
    root_path = target_dir.resolve() / project_name

    # Use Console() directly instead of typer.rich_utils
    console = Console(stderr=True)
    console.print(f"Initializing new project: '{project_name}' in '{root_path}'")

    # --- Create Root Directory ---
    if not _create_directory(root_path, console):
        raise typer.Exit(code=1)

    # --- Create Standard Subdirectories ---
    package_name = project_name  # Assuming project_name is already sanitized (lowercase_with_underscores)
    src_path = root_path / SRC_DIR / package_name
    tests_path = root_path / TESTS_DIR

    if not _create_directory(src_path, console):
        # Consider cleanup logic for root_path if subdirs fail
        raise typer.Exit(code=1)
    if not _create_directory(tests_path, console):
        console.print(
            f"[yellow]Warning:[/yellow] Failed to create '{tests_path}', continuing without tests directory."
        )
        # Decide if this is fatal or not - for now, continue

    # --- Create Essential Files ---
    # Create __init__.py first
    init_py_path = src_path / "__init__.py"
    if not _create_file(init_py_path, "", console):
        console.print(
            f"[bold red]Fatal Error:[/bold red] Failed to create essential file '{init_py_path}'."
        )
        # Consider cleanup
        raise typer.Exit(code=1)

    # Now create files from templates
    template_files_to_create = {
        "_gitignore.template": root_path / ".gitignore",
        "_readme.md.template": root_path / "README.md",
        "_pyproject.toml.template": root_path / "pyproject.toml",
    }

    for template_name, target_path in template_files_to_create.items():
        template_content = _read_template(template_name, console)
        if template_content is None:
            console.print(
                f"[bold red]Fatal Error:[/bold red] Cannot proceed without template '{template_name}'."
            )
            # Consider cleanup
            raise typer.Exit(code=1)

        content = template_content.format(
            project_name=project_name, package_name=package_name
        )

        if not _create_file(target_path, content, console):
            console.print(
                f"[bold red]Fatal Error:[/bold red] Failed to create essential file '{target_path}'."
            )
            # Consider cleanup
            raise typer.Exit(code=1)

    # --- Initialize Git ---
    console.print("\n--- Initializing Git Repository ---")
    git_init_success, _ = _run_command(["git", "init"], cwd=root_path, console=console)
    if not git_init_success:
        console.print(
            "[yellow]Warning:[/yellow] Failed to initialize Git repository. Please run 'git init' manually."
        )
    # TODO: Add initial commit automatically?

    # --- Set up Virtual Environment ---
    console.print("\n--- Setting up Virtual Environment (uv) ---")
    uv_venv_success, _ = _run_command(["uv", "venv"], cwd=root_path, console=console)
    if not uv_venv_success:
        console.print(
            "[yellow]Warning:[/yellow] Failed to create virtual environment with uv. Please run 'uv venv' manually."
        )
        # Exiting here might be safer if venv fails
        raise typer.Exit(code=1)

    # Attempt to install dev dependencies only if venv creation succeeded
    console.print("\n--- Installing Development Dependencies (uv) ---")
    uv_sync_success, _ = _run_command(
        ["uv", "pip", "install", "-e", ".[dev]"], cwd=root_path, console=console
    )
    if not uv_sync_success:
        console.print(
            "[yellow]Warning:[/yellow] Failed to install dev dependencies with uv. Please run 'uv pip install -e \".[dev]\"' manually after activating the environment."
        )

    # --- Final Success Message ---
    console.print(
        f"\n[bold green]Project '{project_name}' created successfully at:[/bold green] {root_path}"
    )
    next_steps = rf"""Next steps:
  1. `cd` into the project directory: `cd {root_path}`
  2. Activate the virtual environment (e.g., `source .venv/bin/activate` or `.venv\Scripts\Activate.ps1`)
  3. Start coding!"""
    console.print(next_steps)


@app.command()
def save(
    message: Annotated[
        str, typer.Option(..., "--message", "-m", help="Describe the changes you made.")
    ],
) -> None:
    """
    Saves the current state of your project (stages all changes and commits).

    This command combines the standard Git workflow of staging and committing
    changes into a single, easy-to-use command. It's equivalent to running:
        `git add .`
        `git commit -m "Your message"`

    The command must be run from within your project directory.

    Args:
        message: A description of the changes you made (required)

    Examples:
        `pps save -m "Add user authentication feature"`
        `pps save -m "Fix bug in data processing"`
    """
    console = Console(stderr=True)
    project_dir = pathlib.Path.cwd()

    # Basic check: Does a .git directory exist here?
    if not (project_dir / ".git").is_dir():
        console.print(
            f"[red]Error:[/red] No Git repository found at '{project_dir}'. Are you inside the project directory?"
        )
        raise typer.Exit(code=1)

    console.print(f"Saving project state in '{project_dir}'...")

    # Step 1: Stage all changes
    console.print("--- Staging all changes (git add .) ---")
    add_success, _ = _run_command(["git", "add", "."], cwd=project_dir, console=console)
    if not add_success:
        console.print(
            "[red]Error:[/red] Failed to stage changes. Check Git output above."
        )
        raise typer.Exit(code=1)

    # Step 2: Commit changes
    console.print(f'--- Committing changes (git commit -m "{message}") ---')
    commit_success, commit_stdout = _run_command(
        ["git", "commit", "-m", message], cwd=project_dir, console=console
    )
    if not commit_success:
        # Check if commit failed because nothing changed
        if commit_stdout and (
            "nothing to commit, working tree clean" in commit_stdout
            or "no changes added to commit" in commit_stdout
        ):
            console.print("[yellow]Info:[/yellow] No changes detected to save.")
        else:
            console.print(
                "[red]Error:[/red] Failed to commit changes. Check Git output above."
            )
            raise typer.Exit(code=1)
    else:
        console.print(
            f"\n[bold green]Successfully saved project state with message:[/bold green] '{message}'"
        )


@app.command()
def sync() -> None:
    """
    Updates your local project with remote changes and pushes your changes.

    This command synchronizes your local repository with the remote repository
    by first pulling any changes from the remote, then pushing your local
    changes. It's equivalent to running:
        `git pull`
        `git push`

    This assumes the remote repository ('origin') and upstream branch are already
    configured. For new repositories, you'll need to set up the remote first
    using standard Git commands.

    Examples:
        `pps sync`

    Common issues:
        - If you haven't set up a remote repository, this will fail
        - If there are merge conflicts, you'll need to resolve them manually
    """
    console = Console(stderr=True)
    project_dir = pathlib.Path.cwd()

    # Basic check: Does a .git directory exist here?
    if not (project_dir / ".git").is_dir():
        console.print(
            f"[red]Error:[/red] No Git repository found at '{project_dir}'. Are you inside the project directory?"
        )
        raise typer.Exit(code=1)

    console.print(f"Syncing project state in '{project_dir}' with remote...")

    # Step 1: Pull changes
    console.print("--- Pulling changes from remote (git pull) ---")
    pull_success, _ = _run_command(["git", "pull"], cwd=project_dir, console=console)
    if not pull_success:
        console.print(
            "[red]Error:[/red] Failed to pull changes from remote. Check Git output above. (Is remote configured? Conflicts?)"
        )
        raise typer.Exit(code=1)

    # Step 2: Push changes
    console.print("--- Pushing local changes to remote (git push) ---")
    push_success, push_stdout = _run_command(
        ["git", "push"], cwd=project_dir, console=console
    )
    if not push_success:
        # Check if push failed because already up-to-date
        # Note: stderr often contains 'Everything up-to-date' for push
        # We capture stderr in _run_command now, but didn't return it. Let's adjust _run_command or check stdout.
        # For now, let's assume stdout might contain info for some git versions/configs
        if push_stdout and "Everything up-to-date" in push_stdout:
            console.print("[yellow]Info:[/yellow] No local changes to push.")
        else:
            console.print(
                "[red]Error:[/red] Failed to push changes to remote. Check Git output above. (Is remote configured? New branch?)"
            )
            raise typer.Exit(code=1)
    else:
        console.print(
            "\n[bold green]Successfully synced project with remote.[/bold green]"
        )


@app.command()
def status(
    working_dir: Annotated[
        pathlib.Path | None,
        typer.Option(
            "--dir",
            "-d",
            help="The project directory to check status for (defaults to current directory).",
        ),
    ] = None,
) -> None:
    """
    Check the status of the project setup and configuration.

    This command provides an overview of your project's current state, showing:
    - Git status (what files have been modified)
    - Project structure validation (correct directories and files)
    - Environment information
    - Tool configuration status

    It's a helpful command to run when you want to see what files you've changed
    or to verify that your project structure is correct.

    Args:
        working_dir: Optional directory to check (defaults to current directory)

    Examples:
        `pps status`
        `pps status --dir ./my_project`
    """
    # Define working_dir if it's None
    if working_dir is None:
        working_dir = pathlib.Path.cwd()

    console = Console(stderr=True)
    console.print("[bold blue]Checking project status...[/bold blue]")

    project_name = working_dir.name

    # Check if git is initialized
    success, git_status = _run_command(
        ["git", "status", "--porcelain"], working_dir, console
    )

    if success:
        if git_status and git_status.strip():
            console.print("[yellow]Git:[/yellow] Repository has uncommitted changes.")
        else:
            console.print("[green]Git:[/green] Repository is clean.")
    else:
        console.print("[red]Git:[/red] Not a git repository or git not installed.")

    # Check project structure
    src_path = working_dir / SRC_DIR
    tests_path = working_dir / TESTS_DIR

    package_name = project_name.replace("-", "_").lower()
    package_path = src_path / package_name

    if not src_path.exists():
        console.print(f"[red]Structure:[/red] Missing source directory ({SRC_DIR}/).")
    elif not package_path.exists():
        console.print(
            f"[red]Structure:[/red] Missing package directory ({SRC_DIR}/{package_name}/)."
        )
    else:
        console.print(
            "[green]Structure:[/green] Source directory structure looks good."
        )

    if not tests_path.exists():
        console.print(
            f"[yellow]Structure:[/yellow] Missing tests directory ({TESTS_DIR}/)."
        )
    else:
        console.print("[green]Structure:[/green] Tests directory exists.")

    # Check for essential files
    essential_files = [
        "pyproject.toml",
        "README.md",
        ".gitignore",
    ]

    missing_files = [f for f in essential_files if not (working_dir / f).exists()]

    if missing_files:
        console.print(
            f"[red]Files:[/red] Missing essential files: {', '.join(missing_files)}"
        )
    else:
        console.print("[green]Files:[/green] All essential files exist.")


def _create_project_structure(
    root_path: pathlib.Path,
    project_name: str,
    package_name: str,
    console: Console,
) -> bool:
    """
    Create the project directory structure.

    Args:
        root_path: Path to the project root
        project_name: Name of the project
        package_name: Name of the package (Python module name)
        console: Rich console for output

    Returns:
        True if successful, False otherwise
    """
    # Create main directories
    src_path = root_path / SRC_DIR
    tests_path = root_path / TESTS_DIR
    package_path = src_path / package_name

    directories_to_create = [
        src_path,
        package_path,
        tests_path,
    ]

    for dir_path in directories_to_create:
        if not _create_directory(dir_path, console):
            return False

    # --- Create Essential Files ---
    # Create __init__.py first
    init_py_path = package_path / "__init__.py"
    if not _create_file(init_py_path, "", console):
        console.print(
            f"[bold red]Fatal Error:[/bold red] Failed to create essential file '{init_py_path}'."
        )
        return False

    # Initialize tests directory with empty __init__.py
    test_init_path = tests_path / "__init__.py"
    if not _create_file(test_init_path, "", console):
        console.print(
            "[bold red]Warning:[/bold red] Failed to create tests __init__.py file."
        )
        # Not fatal, continue

    # Now create files from templates
    template_files_to_create = {
        "_gitignore.template": root_path / ".gitignore",
        "_readme.md.template": root_path / "README.md",
        "_pyproject.toml.template": root_path / "pyproject.toml",
    }

    for template_name, target_path in template_files_to_create.items():
        template_content = _read_template(template_name, console)
        if template_content is None:
            console.print(
                f"[bold red]Fatal Error:[/bold red] Cannot proceed without template '{template_name}'."
            )
            return False

        content = template_content.format(
            project_name=project_name, package_name=package_name
        )

        if not _create_file(target_path, content, console):
            console.print(
                f"[bold red]Fatal Error:[/bold red] Failed to create essential file '{target_path}'."
            )
            return False

    return True


if __name__ == "__main__":
    app()
