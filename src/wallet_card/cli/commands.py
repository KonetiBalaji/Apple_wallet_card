"""CLI commands for wallet card generator."""

import sys
import click
from pathlib import Path
from typing import Optional
from ..templates.business_card import BusinessCardTemplate
from ..templates.classic_blue import ClassicBlueTemplate
from ..templates.modern_dark import ModernDarkTemplate
from ..templates.professional_green import ProfessionalGreenTemplate
from ..templates.elegant_purple import ElegantPurpleTemplate
from ..templates.bold_red import BoldRedTemplate
from ..templates.minimalist_light import MinimalistLightTemplate
from ..utils.config_loader import ConfigLoader
from ..core.validator import Validator, ValidationError


@click.group()
@click.version_option(version="1.0.0")
def main():
    """Apple Wallet Digital Business Card Generator."""
    pass


@main.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to configuration file (YAML or JSON)",
)
@click.option(
    "--output",
    "-o",
    type=str,
    help="Output filename (default: based on description)",
)
@click.option(
    "--template",
    "-t",
    type=click.Choice([
        "classic-blue",
        "modern-dark",
        "professional-green",
        "elegant-purple",
        "bold-red",
        "minimalist-light",
        "business-card"
    ], case_sensitive=False),
    default="classic-blue",
    help="Template style to use",
)
@click.option(
    "--cert",
    type=click.Path(exists=True),
    help="Certificate file for signing",
)
@click.option(
    "--key",
    type=click.Path(exists=True),
    help="Key file for signing",
)
def generate(config: Optional[str], output: Optional[str], template: str, cert: Optional[str], key: Optional[str]):
    """Generate a wallet card from configuration."""
    try:
        # Load configuration
        if config:
            user_config = ConfigLoader.load_config(config)
        else:
            # Try to find config in current directory
            config_paths = ["config.yaml", "config.yml", "config.json", "config/example.yaml"]
            found_config = None
            for path in config_paths:
                if Path(path).exists():
                    found_config = path
                    break

            if found_config:
                click.echo(f"Using configuration: {found_config}")
                user_config = ConfigLoader.load_config(found_config)
            else:
                click.echo("No configuration file found. Using defaults.", err=True)
                click.echo("Run 'wallet-card init-config' to create a configuration file.")
                user_config = ConfigLoader.load_config()

        # Create template based on selection
        template_classes = {
            "classic-blue": ClassicBlueTemplate,
            "modern-dark": ModernDarkTemplate,
            "professional-green": ProfessionalGreenTemplate,
            "elegant-purple": ElegantPurpleTemplate,
            "bold-red": BoldRedTemplate,
            "minimalist-light": MinimalistLightTemplate,
            "business-card": BusinessCardTemplate,  # Legacy support
        }
        
        template_class = template_classes.get(template)
        if not template_class:
            click.echo(f"Unknown template: {template}", err=True)
            sys.exit(1)
        
        template_instance = template_class(
            cert_file=cert,
            key_file=key,
        )

        # Validate configuration
        errors = template_instance.validate_config(user_config)
        if errors:
            click.echo("Configuration errors:", err=True)
            for error in errors:
                click.echo(f"  - {error}", err=True)
            sys.exit(1)

        # Generate pass
        click.echo("Generating wallet card...")
        output_path = template_instance.generate(user_config, output)

        click.echo(f"✅ Pass created: {output_path}")
        click.echo(f"   Share this file via AirDrop, email, or host it on a website.")

    except ValidationError as e:
        click.echo(f"Validation error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
def validate(config_file: str):
    """Validate a configuration file."""
    try:
        config = ConfigLoader.load_config(config_file)
        errors = Validator.validate_config(config)

        if errors:
            click.echo("❌ Configuration is invalid:", err=True)
            for error in errors:
                click.echo(f"  - {error}", err=True)
            sys.exit(1)
        else:
            click.echo("✅ Configuration is valid!")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
def list_templates():
    """List available templates."""
    templates = [
        ("classic-blue", "Classic Blue - Professional & Trustworthy"),
        ("modern-dark", "Modern Dark - Sleek & Contemporary"),
        ("professional-green", "Professional Green - Fresh & Growth-Oriented"),
        ("elegant-purple", "Elegant Purple - Creative & Sophisticated"),
        ("bold-red", "Bold Red - Energetic & Attention-Grabbing"),
        ("minimalist-light", "Minimalist Light - Clean & Simple"),
        ("business-card", "Business Card - Legacy template"),
    ]

    click.echo("Available templates:")
    for name, description in templates:
        click.echo(f"  {name:20} - {description}")


@main.command()
@click.option(
    "--output",
    "-o",
    type=str,
    default="config.yaml",
    help="Output configuration file path",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Configuration file format",
)
def init_config(output: str, format: str):
    """Initialize a new configuration file."""
    try:
        # Load default config
        config = ConfigLoader.load_config()

        # Save to file
        ConfigLoader.save_config(config, output, format)

        click.echo(f"✅ Configuration file created: {output}")
        click.echo(f"   Edit this file and run 'wallet-card generate -c {output}'")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

