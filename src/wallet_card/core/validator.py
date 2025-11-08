"""Validation utilities for configuration and inputs."""

import re
from typing import Dict, List, Optional, Any
from pathlib import Path


class ValidationError(Exception):
    """Raised when validation fails."""

    pass


class Validator:
    """Validates configuration and input data."""

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    PHONE_REGEX = re.compile(r"^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$")
    URL_REGEX = re.compile(
        r"^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$"
    )
    COLOR_REGEX = re.compile(r"^rgb\(\d{1,3},\d{1,3},\d{1,3}\)$")

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format.

        Args:
            email: Email address to validate

        Returns:
            True if valid
        """
        return bool(Validator.EMAIL_REGEX.match(email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format.

        Args:
            phone: Phone number to validate

        Returns:
            True if valid
        """
        # Remove common formatting characters
        cleaned = re.sub(r"[\s\-\(\)\.]", "", phone)
        return bool(Validator.PHONE_REGEX.match(phone)) and len(cleaned) >= 10

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format.

        Args:
            url: URL to validate

        Returns:
            True if valid
        """
        return bool(Validator.URL_REGEX.match(url))

    @staticmethod
    def validate_color(color: str) -> bool:
        """Validate RGB color format.

        Args:
            color: Color string in format rgb(r,g,b)

        Returns:
            True if valid
        """
        if not Validator.COLOR_REGEX.match(color):
            return False

        # Extract RGB values
        match = re.search(r"rgb\((\d+),(\d+),(\d+)\)", color)
        if match:
            r, g, b = map(int, match.groups())
            return all(0 <= val <= 255 for val in [r, g, b])
        return False

    @staticmethod
    def validate_file_exists(filepath: str, required: bool = False) -> bool:
        """Validate that a file exists.

        Args:
            filepath: Path to file
            required: Whether file is required

        Returns:
            True if file exists or not required
        """
        if not filepath:
            return not required
        return Path(filepath).exists()

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> List[str]:
        """Validate configuration dictionary.

        Args:
            config: Configuration dictionary

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Validate pass data
        if "pass" not in config:
            errors.append("Missing 'pass' section in configuration")
            return errors

        pass_data = config["pass"]

        # Validate required fields
        required_fields = ["description", "organizationName", "passTypeIdentifier"]
        for field in required_fields:
            if field not in pass_data:
                errors.append(f"Missing required field: pass.{field}")

        # Validate colors if provided
        if "backgroundColor" in pass_data:
            if not Validator.validate_color(pass_data["backgroundColor"]):
                errors.append("Invalid backgroundColor format (use rgb(r,g,b))")

        if "foregroundColor" in pass_data:
            if not Validator.validate_color(pass_data["foregroundColor"]):
                errors.append("Invalid foregroundColor format (use rgb(r,g,b))")

        # Validate fields
        if "fields" in pass_data:
            fields = pass_data["fields"]
            Validator._validate_fields(fields, errors)

        # Validate assets if provided
        if "assets" in config:
            assets = config["assets"]
            for asset_type in ["icon", "logo", "photo"]:
                if asset_type in assets and assets[asset_type]:
                    if not Validator.validate_file_exists(assets[asset_type]):
                        errors.append(f"Asset file not found: {assets[asset_type]}")

        # Validate signing if provided
        if "signing" in config:
            signing = config["signing"]
            if signing.get("enabled", False):
                if "cert_file" not in signing or "key_file" not in signing:
                    errors.append("Signing enabled but cert_file or key_file missing")
                else:
                    if not Validator.validate_file_exists(signing["cert_file"], required=True):
                        errors.append(f"Certificate file not found: {signing['cert_file']}")
                    if not Validator.validate_file_exists(signing["key_file"], required=True):
                        errors.append(f"Key file not found: {signing['key_file']}")

        return errors

    @staticmethod
    def _validate_fields(fields: Dict[str, Any], errors: List[str]) -> None:
        """Validate field definitions.

        Args:
            fields: Fields dictionary
            errors: List to append errors to
        """
        field_types = ["primaryFields", "secondaryFields", "auxiliaryFields", "backFields"]

        for field_type in field_types:
            if field_type in fields:
                if not isinstance(fields[field_type], list):
                    errors.append(f"{field_type} must be a list")
                    continue

                for i, field in enumerate(fields[field_type]):
                    if not isinstance(field, dict):
                        errors.append(f"{field_type}[{i}] must be a dictionary")
                        continue

                    if "key" not in field:
                        errors.append(f"{field_type}[{i}] missing 'key'")
                    if "label" not in field:
                        errors.append(f"{field_type}[{i}] missing 'label'")
                    if "value" not in field:
                        errors.append(f"{field_type}[{i}] missing 'value'")

                    # Validate email/phone/url if applicable
                    if "value" in field:
                        value = str(field["value"])
                        key = field.get("key", "").lower()

                        if "email" in key and value:
                            if not Validator.validate_email(value):
                                errors.append(f"{field_type}[{i}]: Invalid email format")
                        elif "phone" in key and value:
                            if not Validator.validate_phone(value):
                                errors.append(f"{field_type}[{i}]: Invalid phone format")
                        elif "url" in key or "website" in key or "linkedin" in key or "github" in key:
                            if value:
                                # For social media fields (linkedin, github), be very lenient
                                # They're just display values, not actual clickable URLs
                                if "linkedin" in key or "github" in key:
                                    # Allow any format for social media - it's just text
                                    pass
                                elif "website" in key:
                                    # For website, if it starts with http, validate it
                                    # Otherwise, allow it (might be a display value)
                                    if value.startswith("http") and not Validator.validate_url(value):
                                        errors.append(f"{field_type}[{i}]: Invalid URL format")
                                else:
                                    # For other URL fields, validate if it's a full URL
                                    if value.startswith("http") and not Validator.validate_url(value):
                                        errors.append(f"{field_type}[{i}]: Invalid URL format")

    @staticmethod
    def validate_and_raise(config: Dict[str, Any]) -> None:
        """Validate configuration and raise exception if invalid.

        Args:
            config: Configuration dictionary

        Raises:
            ValidationError: If validation fails
        """
        errors = Validator.validate_config(config)
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ValidationError(error_msg)

