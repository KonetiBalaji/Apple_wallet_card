"""Base template class for pass generation."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path
from ..core.pass_generator import PassGenerator
from ..core.asset_manager import AssetManager


class BaseTemplate(ABC):
    """Base class for all pass templates."""

    def __init__(
        self,
        assets_dir: str = "assets/user",
        output_dir: str = "output",
        cert_file: str = None,
        key_file: str = None,
    ):
        """Initialize template.

        Args:
            assets_dir: Directory containing assets
            output_dir: Directory for output files
            cert_file: Optional certificate file for signing
            key_file: Optional key file for signing
        """
        self.assets_dir = assets_dir
        self.output_dir = output_dir
        self.generator = PassGenerator(assets_dir, output_dir, cert_file, key_file)
        self.asset_manager = AssetManager(assets_dir)

    @abstractmethod
    def get_template_config(self) -> Dict[str, Any]:
        """Get default template configuration.

        Returns:
            Template configuration dictionary
        """
        pass

    def generate(self, config: Dict[str, Any], output_filename: str = None) -> Path:
        """Generate pass from configuration.

        Args:
            config: Configuration dictionary (merged with template defaults)
            output_filename: Optional output filename

        Returns:
            Path to generated .pkpass file
        """
        # Merge template defaults with provided config
        template_config = self.get_template_config()
        merged_config = self._merge_configs(template_config, config)

        return self.generator.generate(merged_config, output_filename)

    def _merge_configs(self, template: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Merge template config with user config.

        Args:
            template: Template configuration
            user: User configuration

        Returns:
            Merged configuration
        """
        result = template.copy()

        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def validate_config(self, config: Dict[str, Any]) -> list:
        """Validate configuration.

        Args:
            config: Configuration to validate

        Returns:
            List of validation errors
        """
        from ..core.validator import Validator

        return Validator.validate_config(config)

