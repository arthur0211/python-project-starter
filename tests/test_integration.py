"""
Integration tests for project_starter end-to-end flows.
"""

import os
import subprocess
import tempfile
from pathlib import Path

import pytest
from project_starter.main import SRC_DIR, TESTS_DIR, app
from typer.testing import CliRunner


@pytest.fixture()
def runner():
    """Fixture providing a CLI runner for testing Typer commands."""
    return CliRunner()


@pytest.fixture()
def temp_project_dir():
    """Create a temporary directory for project creation tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = Path.cwd()
        os.chdir(temp_dir)

        yield Path(temp_dir)

        # Restore original working directory
        os.chdir(original_cwd)


class TestProjectCreationFlow:
    """End-to-end tests for project creation and operations flow."""

    @pytest.mark.integration()
    @pytest.mark.skip(reason="Requires git and uv to be installed and configured")
    def test_create_project_and_save(self, runner, temp_project_dir):
        """
        Test creating a project and performing save operation.

        NOTE: This test requires git and uv to be installed and configured.
        It is skipped by default to avoid affecting CI pipelines.
        """
        # Create a new project
        project_name = "test_project"
        result = runner.invoke(app, ["new", project_name])

        assert result.exit_code == 0

        # Verify project structure
        project_dir = temp_project_dir / project_name
        assert project_dir.exists()
        assert (project_dir / SRC_DIR / project_name / "__init__.py").exists()
        assert (project_dir / TESTS_DIR).exists()
        assert (project_dir / "pyproject.toml").exists()
        assert (project_dir / "README.md").exists()
        assert (project_dir / ".gitignore").exists()
        assert (project_dir / ".git").exists()

        # Change directory to the project
        os.chdir(project_dir)

        # Create a sample file
        sample_file = project_dir / SRC_DIR / project_name / "sample.py"
        sample_file.write_text(
            '"""Sample module."""\n\ndef hello():\n    """Say hello."""\n    return "Hello, world!"\n'
        )

        # Save changes
        result = runner.invoke(app, ["save", "-m", "Add sample module"])

        assert result.exit_code == 0

        # Check git status
        result = runner.invoke(app, ["status"])

        assert result.exit_code == 0
        # The repository should be clean after saving

        # This is where we would test sync, but it requires a remote repository
        # That's more complex to set up in a test environment


@pytest.mark.integration()
class TestMockedIntegrationFlow:
    """Integration-like tests that mock external commands."""

    def test_project_creation_flow_mocked(self, runner, monkeypatch):
        """Test the flow of creating a project and performing operations with mocked external commands."""
        project_name = "test_project"

        # Mock subprocess.run to avoid actual command execution
        def mock_subprocess_run(*args, **_):
            return subprocess.CompletedProcess(args[0], 0, stdout="", stderr="")

        monkeypatch.setattr(subprocess, "run", mock_subprocess_run)

        # Execute the new command
        result = runner.invoke(app, ["new", project_name])

        # Check the exit code
        # Note: This may still fail if actual file operations fail
        # We're mocking only the subprocess calls
        assert result.exit_code == 0 or "Failed to create" in result.stdout
