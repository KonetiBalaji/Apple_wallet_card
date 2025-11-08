"""Configuration loader with YAML/JSON support and environment variables."""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


class ConfigLoader:
    """Loads and merges configuration from files and environment variables."""

    @staticmethod
    def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or use defaults.

        Args:
            config_path: Path to configuration file (YAML or JSON)

        Returns:
            Configuration dictionary
        """
        default_config = ConfigLoader._get_default_config()

        if config_path and Path(config_path).exists():
            file_config = ConfigLoader._load_file(config_path)
            config = ConfigLoader._merge_configs(default_config, file_config)
        else:
            config = default_config.copy()

        # Override with environment variables
        config = ConfigLoader._apply_env_overrides(config)

        return config

    @staticmethod
    def _load_file(config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML or JSON file.

        Args:
            config_path: Path to configuration file

        Returns:
            Configuration dictionary
        """
        path = Path(config_path)
        suffix = path.suffix.lower()

        with open(path, "r", encoding="utf-8") as f:
            if suffix in [".yaml", ".yml"]:
                return yaml.safe_load(f) or {}
            elif suffix == ".json":
                return json.load(f)
            else:
                raise ValueError(f"Unsupported config file format: {suffix}")

    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Get default configuration.

        Returns:
            Default configuration dictionary
        """
        return {
            "pass": {
                "passTypeIdentifier": "pass.com.example.generic",
                "serialNumber": "123456789",
                "teamIdentifier": "",
                "organizationName": "My Organization",
                "description": "Digital Business Card",
                "logoText": "",
                "foregroundColor": "rgb(255,255,255)",
                "backgroundColor": "rgb(0,77,153)",
                "labelColor": "rgb(255,255,255)",
                "fields": {
                    "primaryFields": [],
                    "secondaryFields": [],
                    "auxiliaryFields": [],
                    "backFields": [],
                },
            },
            "assets": {},
            "signing": {
                "enabled": False,
            },
        }

    @staticmethod
    def _merge_configs(default: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge two configuration dictionaries.

        Args:
            default: Default configuration
            override: Override configuration

        Returns:
            Merged configuration
        """
        result = default.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigLoader._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    @staticmethod
    def _apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides to configuration.

        Environment variables should be prefixed with WALLET_CARD_ and use
        underscore notation, e.g., WALLET_CARD_PASS_ORGANIZATION_NAME

        Args:
            config: Configuration dictionary

        Returns:
            Configuration with environment overrides applied
        """
        prefix = "WALLET_CARD_"

        for key, value in os.environ.items():
            if not key.startswith(prefix):
                continue

            # Remove prefix and convert to nested keys
            key_path = key[len(prefix) :].lower().split("_")

            # Navigate to the correct location in config
            current = config
            for k in key_path[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]

            # Set the value
            final_key = key_path[-1]
            current[final_key] = value

        return config

    @staticmethod
    def save_config(config: Dict[str, Any], output_path: str, format: str = "yaml") -> None:
        """Save configuration to file.

        Args:
            config: Configuration dictionary
            output_path: Path to output file
            format: File format ('yaml' or 'json')
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            if format.lower() == "yaml":
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            elif format.lower() == "json":
                json.dump(config, f, indent=2, sort_keys=False)
            else:
                raise ValueError(f"Unsupported format: {format}")

