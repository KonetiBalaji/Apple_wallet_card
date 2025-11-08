"""File utility functions."""

import os
import shutil
from pathlib import Path
from typing import Optional


class FileUtils:
    """Utility functions for file operations."""

    @staticmethod
    def ensure_directory(path: str) -> Path:
        """Ensure a directory exists, creating it if necessary.

        Args:
            path: Directory path

        Returns:
            Path object
        """
        dir_path = Path(path)
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    @staticmethod
    def copy_file(source: str, destination: str) -> Path:
        """Copy a file from source to destination.

        Args:
            source: Source file path
            destination: Destination file path

        Returns:
            Path to copied file
        """
        dest_path = Path(destination)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return dest_path

    @staticmethod
    def safe_filename(filename: str) -> str:
        """Create a safe filename by removing invalid characters.

        Args:
            filename: Original filename

        Returns:
            Safe filename
        """
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        safe = "".join(c if c not in invalid_chars else "_" for c in filename)
        # Remove leading/trailing spaces and dots
        safe = safe.strip(" .")
        return safe or "file"

    @staticmethod
    def find_file_in_paths(filename: str, search_paths: list) -> Optional[Path]:
        """Find a file in multiple search paths.

        Args:
            filename: Name of file to find
            search_paths: List of directories to search

        Returns:
            Path to file if found, None otherwise
        """
        for search_path in search_paths:
            path = Path(search_path) / filename
            if path.exists():
                return path
        return None

