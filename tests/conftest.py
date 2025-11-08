"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def tmp_path(tmp_path_factory):
    """Create a temporary directory for tests."""
    return tmp_path_factory.mktemp("test")

