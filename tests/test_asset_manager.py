"""Tests for asset manager."""

import pytest
from pathlib import Path
from wallet_card.core.asset_manager import AssetManager


class TestAssetManager:
    """Test AssetManager class."""

    def test_init(self, tmp_path):
        """Test AssetManager initialization."""
        assets_dir = tmp_path / "assets"
        manager = AssetManager(str(assets_dir))
        assert manager.assets_dir == assets_dir
        assert assets_dir.exists()

    def test_ensure_image_exists_creates_placeholder(self, tmp_path):
        """Test that placeholder images are created when missing."""
        manager = AssetManager(str(tmp_path))
        icon_path = manager.ensure_image_exists("test_icon.png", (180, 180))

        assert icon_path.exists()
        assert icon_path.name == "test_icon.png"

        # Verify it's a valid image
        from PIL import Image
        img = Image.open(icon_path)
        assert img.size == (180, 180)

    def test_prepare_icon(self, tmp_path):
        """Test icon preparation."""
        manager = AssetManager(str(tmp_path))
        icon_path = manager.prepare_icon()

        assert icon_path.exists()
        assert icon_path.name == "icon.png"

    def test_prepare_logo(self, tmp_path):
        """Test logo preparation."""
        manager = AssetManager(str(tmp_path))
        logo_path = manager.prepare_logo()

        assert logo_path.exists()
        assert logo_path.name == "logo.png"

    def test_prepare_photo(self, tmp_path):
        """Test photo preparation."""
        manager = AssetManager(str(tmp_path))
        photo_path = manager.prepare_photo()

        assert photo_path.exists()
        assert photo_path.name == "photo.png"

    def test_generate_qr_code(self, tmp_path):
        """Test QR code generation."""
        manager = AssetManager(str(tmp_path))
        qr_path = manager.generate_qr_code("https://example.com", "test_qr.png")

        assert qr_path.exists()
        assert qr_path.name == "test_qr.png"

        # Verify it's a valid image
        from PIL import Image
        img = Image.open(qr_path)
        assert img.size == (200, 200)

    def test_get_asset_path(self, tmp_path):
        """Test getting asset path."""
        manager = AssetManager(str(tmp_path))

        # Non-existent file
        assert manager.get_asset_path("nonexistent.png") is None

        # Create a file and test
        test_file = tmp_path / "test.png"
        test_file.touch()
        assert manager.get_asset_path("test.png") == test_file

