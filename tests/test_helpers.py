"""
Unit tests for helper functions in project_starter.main.
"""

import os
import pathlib
import pytest
from unittest.mock import MagicMock, patch
from rich.console import Console

from project_starter.main import (
    _create_directory,
    _create_file,
    _read_template,
    _run_command,
)


class TestCreateDirectory:
    """Tests for the _create_directory function."""

    def test_create_new_directory(self, tmp_path):
        """Test creating a new directory."""
        # Arrange
        test_dir = tmp_path / "new_dir"
        console = MagicMock(spec=Console)
        
        # Act
        result = _create_directory(test_dir, console)
        
        # Assert
        assert result is True
        assert test_dir.exists()
        assert test_dir.is_dir()
        console.print.assert_called_with(f"[green]Created directory:[/green] {test_dir}")

    def test_directory_already_exists(self, tmp_path):
        """Test when directory already exists."""
        # Arrange
        test_dir = tmp_path / "existing_dir"
        test_dir.mkdir()
        console = MagicMock(spec=Console)
        
        # Act
        result = _create_directory(test_dir, console)
        
        # Assert
        assert result is True
        console.print.assert_called_with(f"[yellow]Directory already exists:[/yellow] {test_dir}")

    def test_path_exists_but_not_directory(self, tmp_path):
        """Test when path exists but is not a directory."""
        # Arrange
        test_file = tmp_path / "existing_file"
        test_file.write_text("test content")
        console = MagicMock(spec=Console)
        
        # Act
        result = _create_directory(test_file, console)
        
        # Assert
        assert result is False
        console.print.assert_called_with(f"[bold red]Error:[/bold red] Path '{test_file}' exists but is not a directory.")

    def test_permission_error(self, tmp_path):
        """Test when permission error occurs."""
        # Arrange
        console = MagicMock(spec=Console)
        test_dir = tmp_path / "no_perm_dir"
        
        # Act & Assert
        with patch('pathlib.Path.mkdir', side_effect=PermissionError("Permission denied")):
            result = _create_directory(test_dir, console)
            assert result is False
            console.print.assert_called_with(
                f"[bold red]Error:[/bold red] Failed to create directory '{test_dir}': Permission denied"
            )


class TestCreateFile:
    """Tests for the _create_file function."""

    def test_create_new_file(self, tmp_path):
        """Test creating a new file."""
        # Arrange
        test_file = tmp_path / "new_file.txt"
        content = "Test content"
        console = MagicMock(spec=Console)
        
        # Act
        result = _create_file(test_file, content, console)
        
        # Assert
        assert result is True
        assert test_file.exists()
        assert test_file.read_text() == content
        console.print.assert_called_with(f"[green]Created file:[/green] {test_file}")

    def test_file_already_exists(self, tmp_path):
        """Test when file already exists."""
        # Arrange
        test_file = tmp_path / "existing_file.txt"
        test_file.write_text("existing content")
        console = MagicMock(spec=Console)
        
        # Act
        result = _create_file(test_file, "new content", console)
        
        # Assert
        assert result is True
        assert test_file.read_text() == "existing content"  # Content should not be changed
        console.print.assert_called_with(f"[yellow]File already exists:[/yellow] {test_file}")

    def test_parent_directory_creation(self, tmp_path):
        """Test creating parent directories if they don't exist."""
        # Arrange
        nested_file = tmp_path / "nested" / "dir" / "new_file.txt"
        content = "Test content"
        console = MagicMock(spec=Console)
        
        # Act
        with patch('project_starter.main._create_directory') as mock_create_dir:
            mock_create_dir.return_value = True
            result = _create_file(nested_file, content, console)
        
        # Assert
        assert result is True
        mock_create_dir.assert_called_once()

    def test_parent_directory_creation_failure(self, tmp_path):
        """Test handling failure to create parent directory."""
        # Arrange
        nested_file = tmp_path / "nested" / "dir" / "new_file.txt"
        content = "Test content"
        console = MagicMock(spec=Console)
        
        # Act
        with patch('project_starter.main._create_directory') as mock_create_dir:
            mock_create_dir.return_value = False
            result = _create_file(nested_file, content, console)
        
        # Assert
        assert result is False
        mock_create_dir.assert_called_once()

    def test_permission_error(self, tmp_path):
        """Test when permission error occurs."""
        # Arrange
        test_file = tmp_path / "no_perm_file.txt"
        console = MagicMock(spec=Console)
        
        # Act & Assert
        with patch('pathlib.Path.write_text', side_effect=PermissionError("Permission denied")):
            result = _create_file(test_file, "content", console)
            assert result is False
            console.print.assert_called_with(
                f"[bold red]Error:[/bold red] Failed to create file '{test_file}': Permission denied"
            )


class TestReadTemplate:
    """Tests for the _read_template function."""

    def test_successful_template_read(self):
        """Test successfully reading a template file."""
        # Arrange
        template_name = "test_template.txt"
        template_content = "Template content"
        console = MagicMock(spec=Console)
        
        # Act
        with patch('importlib.resources.files') as mock_files:
            mock_path = MagicMock()
            mock_files.return_value = mock_path
            mock_path.__truediv__.return_value = mock_path
            mock_path.read_text.return_value = template_content
            
            result = _read_template(template_name, console)
        
        # Assert
        assert result == template_content
        mock_path.read_text.assert_called_once()

    def test_template_not_found(self):
        """Test handling case when template is not found."""
        # Arrange
        template_name = "missing_template.txt"
        console = MagicMock(spec=Console)
        
        # Act
        with patch('importlib.resources.files') as mock_files:
            mock_path = MagicMock()
            mock_files.return_value = mock_path
            mock_path.__truediv__.return_value = mock_path
            mock_path.read_text.side_effect = FileNotFoundError("Template not found")
            
            result = _read_template(template_name, console)
        
        # Assert
        assert result is None
        console.print.assert_called_with(
            f"[bold red]Error:[/bold red] Could not read template '{template_name}'. Template not found"
        )


class TestRunCommand:
    """Tests for the _run_command function."""

    def test_successful_command_with_capture(self, tmp_path):
        """Test running a command successfully with output capture."""
        # Arrange
        command = ["echo", "test"]
        cwd = tmp_path
        console = MagicMock(spec=Console)
        
        # Act
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = "test output"
            mock_run.return_value = mock_result
            
            success, output = _run_command(command, cwd, console)
        
        # Assert
        assert success is True
        assert output == "test output"
        mock_run.assert_called_with(
            command,
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True
        )

    def test_successful_command_without_capture(self, tmp_path):
        """Test running a command successfully without output capture."""
        # Arrange
        command = ["echo", "test"]
        cwd = tmp_path
        console = MagicMock(spec=Console)
        
        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock()
            
            success, output = _run_command(command, cwd, console, capture=False)
        
        # Assert
        assert success is True
        assert output is None
        mock_run.assert_called_with(
            command,
            cwd=cwd,
            check=True,
            text=True
        )

    def test_command_failure(self, tmp_path):
        """Test handling a command that fails."""
        # Arrange
        command = ["ls", "--invalid-option"]
        cwd = tmp_path
        console = MagicMock(spec=Console)
        
        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.SubprocessError("Command failed")
            
            success, output = _run_command(command, cwd, console)
        
        # Assert
        assert success is False
        assert output is None
        console.print.assert_called_with(
            "[bold red]Command Error:[/bold red] ls --invalid-option failed with Command failed"
        ) 