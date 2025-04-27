"""
Unit tests for CLI commands in project_starter.main.
"""

import os
import pathlib
from unittest.mock import MagicMock, patch
import pytest
from typer.testing import CliRunner

from project_starter.main import app, SRC_DIR, TESTS_DIR


@pytest.fixture
def runner():
    """Fixture providing a CLI runner for testing Typer commands."""
    return CliRunner()


class TestNewCommand:
    """Tests for the 'new' command."""

    def test_invalid_project_name(self, runner):
        """Test validation of project name with uppercase characters."""
        # Act
        result = runner.invoke(app, ["new", "Invalid_Name"])
        
        # Assert
        assert result.exit_code == 1
        assert "Error: Project name 'Invalid_Name' should be lowercase with underscores" in result.stdout

    def test_invalid_target_directory(self, runner):
        """Test validation of non-existent target directory."""
        # Act
        with patch('pathlib.Path.is_dir', return_value=False):
            result = runner.invoke(app, ["new", "valid_name", "--dir", "/nonexistent/dir"])
        
        # Assert
        assert result.exit_code == 1
        assert "Error: Specified target directory does not exist" in result.stdout

    def test_successful_project_creation(self, runner, tmp_path):
        """Test successful project creation with all the expected steps."""
        # Arrange
        project_name = "test_project"
        
        # Mock all the helper functions to avoid actual file system operations
        with patch('project_starter.main._create_directory', return_value=True) as mock_create_dir, \
             patch('project_starter.main._create_file', return_value=True) as mock_create_file, \
             patch('project_starter.main._read_template', return_value="template content") as mock_read_template, \
             patch('project_starter.main._run_command', return_value=(True, "")) as mock_run_command, \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["new", project_name, "--dir", str(tmp_path)])
        
        # Assert
        assert result.exit_code == 0
        
        # Verify the expected directory creation calls
        assert mock_create_dir.call_count >= 3  # root, src/package, tests
        
        # Verify template reading
        assert mock_read_template.call_count == 3  # gitignore, readme, pyproject.toml
        
        # Verify file creation
        assert mock_create_file.call_count >= 4  # __init__.py + 3 template files
        
        # Verify git init and UV commands
        assert mock_run_command.call_count >= 3  # git init, uv venv, uv sync

    def test_directory_creation_failure(self, runner, tmp_path):
        """Test handling of directory creation failure."""
        # Arrange
        project_name = "test_project"
        
        # Mock directory creation to fail
        with patch('project_starter.main._create_directory', return_value=False), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["new", project_name, "--dir", str(tmp_path)])
        
        # Assert
        assert result.exit_code == 1


class TestSaveCommand:
    """Tests for the 'save' command."""

    def test_not_a_git_repository(self, runner):
        """Test error when not in a git repository."""
        # Arrange
        with patch('pathlib.Path.is_dir', return_value=False), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["save", "-m", "Test commit"])
        
        # Assert
        assert result.exit_code == 1
        # Error message is shown by console.print which is mocked

    def test_git_add_failure(self, runner):
        """Test handling of git add failure."""
        # Arrange
        with patch('pathlib.Path.is_dir', return_value=True), \
             patch('project_starter.main._run_command', return_value=(False, None)), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["save", "-m", "Test commit"])
        
        # Assert
        assert result.exit_code == 1

    def test_git_commit_failure(self, runner):
        """Test handling of git commit failure."""
        # Arrange
        with patch('pathlib.Path.is_dir', return_value=True), \
             patch('project_starter.main._run_command', side_effect=[
                 (True, None),  # git add succeeds
                 (False, None)  # git commit fails
             ]), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["save", "-m", "Test commit"])
        
        # Assert
        assert result.exit_code == 1

    def test_nothing_to_commit(self, runner):
        """Test handling of 'nothing to commit' case."""
        # Arrange
        with patch('pathlib.Path.is_dir', return_value=True), \
             patch('project_starter.main._run_command', side_effect=[
                 (True, None),  # git add succeeds
                 (False, "nothing to commit, working tree clean")  # git commit indicates nothing to commit
             ]), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["save", "-m", "Test commit"])
        
        # Assert
        assert result.exit_code == 0  # This is not treated as an error

    def test_successful_save(self, runner):
        """Test successful save operation."""
        # Arrange
        with patch('pathlib.Path.is_dir', return_value=True), \
             patch('project_starter.main._run_command', side_effect=[
                 (True, None),  # git add succeeds
                 (True, "1 file changed")  # git commit succeeds
             ]), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["save", "-m", "Test commit"])
        
        # Assert
        assert result.exit_code == 0


class TestSyncCommand:
    """Tests for the 'sync' command."""

    def test_not_a_git_repository(self, runner):
        """Test error when not in a git repository."""
        # Arrange
        with patch('pathlib.Path.is_dir', return_value=False), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["sync"])
        
        # Assert
        assert result.exit_code == 1

    def test_git_pull_failure(self, runner):
        """Test handling of git pull failure."""
        # Arrange
        with patch('pathlib.Path.is_dir', return_value=True), \
             patch('project_starter.main._run_command', return_value=(False, None)), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["sync"])
        
        # Assert
        assert result.exit_code == 1

    def test_git_push_failure(self, runner):
        """Test handling of git push failure."""
        # Arrange
        with patch('pathlib.Path.is_dir', return_value=True), \
             patch('project_starter.main._run_command', side_effect=[
                 (True, None),  # git pull succeeds
                 (False, None)  # git push fails
             ]), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["sync"])
        
        # Assert
        assert result.exit_code == 1

    def test_successful_sync(self, runner):
        """Test successful sync operation."""
        # Arrange
        with patch('pathlib.Path.is_dir', return_value=True), \
             patch('project_starter.main._run_command', side_effect=[
                 (True, None),  # git pull succeeds
                 (True, None)   # git push succeeds
             ]), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["sync"])
        
        # Assert
        assert result.exit_code == 0


class TestStatusCommand:
    """Tests for the 'status' command."""

    def test_git_status_check(self, runner, tmp_path):
        """Test checking git status."""
        # Arrange
        with patch('project_starter.main._run_command', return_value=(True, "M file.txt")), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_dir', return_value=True), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["status", "--dir", str(tmp_path)])
        
        # Assert
        assert result.exit_code == 0

    def test_structure_validation(self, runner, tmp_path):
        """Test project structure validation."""
        # Arrange
        with patch('project_starter.main._run_command', return_value=(True, "")), \
             patch('pathlib.Path.exists', side_effect=lambda p: str(p).endswith('src')), \
             patch('pathlib.Path.is_dir', return_value=True), \
             patch('rich.console.Console'):
            
            # Act
            result = runner.invoke(app, ["status", "--dir", str(tmp_path)])
        
        # Assert
        assert result.exit_code == 0 