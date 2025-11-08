"""Tests for validator."""

import pytest
from wallet_card.core.validator import Validator, ValidationError


class TestValidator:
    """Test Validator class."""

    def test_validate_email(self):
        """Test email validation."""
        assert Validator.validate_email("test@example.com") is True
        assert Validator.validate_email("user.name@domain.co.uk") is True
        assert Validator.validate_email("invalid") is False
        assert Validator.validate_email("invalid@") is False
        assert Validator.validate_email("@domain.com") is False

    def test_validate_phone(self):
        """Test phone validation."""
        assert Validator.validate_phone("+1 (555) 123-4567") is True
        assert Validator.validate_phone("555-123-4567") is True
        assert Validator.validate_phone("1234567890") is True
        assert Validator.validate_phone("123") is False
        assert Validator.validate_phone("") is False

    def test_validate_url(self):
        """Test URL validation."""
        assert Validator.validate_url("https://example.com") is True
        assert Validator.validate_url("http://example.com/path") is True
        assert Validator.validate_url("not-a-url") is False
        assert Validator.validate_url("ftp://example.com") is False

    def test_validate_color(self):
        """Test color validation."""
        assert Validator.validate_color("rgb(255,255,255)") is True
        assert Validator.validate_color("rgb(0,77,153)") is True
        assert Validator.validate_color("rgb(256,0,0)") is False  # Out of range
        assert Validator.validate_color("rgb(255,255)") is False  # Invalid format
        assert Validator.validate_color("#ffffff") is False  # Wrong format

    def test_validate_file_exists(self, tmp_path):
        """Test file existence validation."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        assert Validator.validate_file_exists(str(test_file)) is True
        assert Validator.validate_file_exists(str(tmp_path / "nonexistent.txt")) is False
        assert Validator.validate_file_exists("", required=False) is True
        assert Validator.validate_file_exists("", required=True) is False

    def test_validate_config_minimal(self):
        """Test minimal valid configuration."""
        config = {
            "pass": {
                "description": "Test",
                "organizationName": "Test Org",
                "passTypeIdentifier": "pass.test",
            }
        }
        errors = Validator.validate_config(config)
        assert len(errors) == 0

    def test_validate_config_missing_required(self):
        """Test configuration with missing required fields."""
        config = {
            "pass": {}
        }
        errors = Validator.validate_config(config)
        assert len(errors) > 0
        assert any("description" in e for e in errors)

    def test_validate_config_invalid_color(self):
        """Test configuration with invalid colors."""
        config = {
            "pass": {
                "description": "Test",
                "organizationName": "Test Org",
                "passTypeIdentifier": "pass.test",
                "backgroundColor": "invalid",
            }
        }
        errors = Validator.validate_config(config)
        assert any("backgroundColor" in e for e in errors)

    def test_validate_config_invalid_email(self):
        """Test configuration with invalid email."""
        config = {
            "pass": {
                "description": "Test",
                "organizationName": "Test Org",
                "passTypeIdentifier": "pass.test",
                "fields": {
                    "secondaryFields": [
                        {"key": "email", "label": "Email", "value": "invalid-email"}
                    ]
                }
            }
        }
        errors = Validator.validate_config(config)
        assert any("email" in e.lower() for e in errors)

    def test_validate_and_raise(self):
        """Test validate_and_raise raises exception."""
        config = {
            "pass": {}
        }
        with pytest.raises(ValidationError):
            Validator.validate_and_raise(config)

