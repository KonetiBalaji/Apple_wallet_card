"""Core pass generation logic."""

import os
import json
import zipfile
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from .pkpass_generator import PKPassGenerator
from .asset_manager import AssetManager
from .validator import Validator, ValidationError


class PassGenerator:
    """Generates Apple Wallet .pkpass files."""

    def __init__(
        self,
        assets_dir: str = "assets/user",
        output_dir: str = "output",
        cert_file: Optional[str] = None,
        key_file: Optional[str] = None,
    ):
        """Initialize pass generator.

        Args:
            assets_dir: Directory containing assets
            output_dir: Directory for output files
            cert_file: Optional path to certificate file for signing
            key_file: Optional path to key file for signing
        """
        self.assets_dir = Path(assets_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.asset_manager = AssetManager(str(self.assets_dir))
        self.cert_file = cert_file
        self.key_file = key_file

    def generate(
        self,
        config: Dict[str, Any],
        output_filename: Optional[str] = None,
    ) -> Path:
        """Generate a .pkpass file from configuration.

        Args:
            config: Configuration dictionary
            output_filename: Optional custom output filename

        Returns:
            Path to generated .pkpass file

        Raises:
            ValidationError: If configuration is invalid
        """
        # Validate configuration
        Validator.validate_and_raise(config)

        # Prepare assets
        assets = config.get("assets", {})
        icon_path = self.asset_manager.prepare_icon(assets.get("icon"))
        logo_path = self.asset_manager.prepare_logo(assets.get("logo"))
        photo_path = self.asset_manager.prepare_photo(assets.get("photo"))

        # Generate QR code if URL provided
        qr_path = None
        if "qr_data" in config:
            qr_path = self.asset_manager.generate_qr_code(config["qr_data"])

        # Build pass data structure
        pass_data = self._build_pass_data(config, icon_path, logo_path, photo_path, qr_path)

        # Generate pass
        try:
            # Use custom PKPassGenerator instead of wallet-passes library
            wp = PKPassGenerator(
                pass_data,
                cert_file=self.cert_file,
                key_file=self.key_file,
            )

            # Generate pass in temporary directory
            with tempfile.TemporaryDirectory() as tmpdir:
                pass_path = Path(tmpdir) / "pass"
                wp.create(pass_path)

                # Determine output filename
                if not output_filename:
                    description = config["pass"].get("description", "wallet_card")
                    # Sanitize filename
                    safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in description)
                    output_filename = f"{safe_name}.pkpass"

                output_path = self.output_dir / output_filename

                # Create zip file (.pkpass is a zip file)
                # Important: Exclude macOS metadata files and use proper compression
                with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(pass_path):
                        # Exclude __MACOSX and .DS_Store folders/files
                        dirs[:] = [d for d in dirs if d not in ('__MACOSX', '.DS_Store')]
                        for file in files:
                            # Skip macOS metadata files
                            if file.startswith('.') or file == '__MACOSX':
                                continue
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(pass_path)
                            # Ensure no leading slashes or macOS metadata
                            arcname_str = str(arcname).replace('\\', '/')
                            if not arcname_str.startswith('__MACOSX') and not arcname_str.startswith('.'):
                                zipf.write(file_path, arcname_str)

            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to generate pass: {str(e)}") from e

    def _build_pass_data(
        self,
        config: Dict[str, Any],
        icon_path: Path,
        logo_path: Path,
        photo_path: Path,
        qr_path: Optional[Path],
    ) -> Dict[str, Any]:
        """Build pass data structure for wallet-passes library.

        Args:
            config: Configuration dictionary
            icon_path: Path to icon image
            logo_path: Path to logo image
            photo_path: Path to photo image
            qr_path: Optional path to QR code image

        Returns:
            Pass data dictionary
        """
        pass_config = config["pass"]

        # Base pass structure
        # Use a valid teamIdentifier format (even if dummy) - some iOS versions require it
        team_id = pass_config.get("teamIdentifier", "")
        if not team_id:
            # Use a dummy team identifier format (10 uppercase letters)
            # This is required by some iOS versions even for unsigned passes
            team_id = "TEAMID1234"
        
        pass_data = {
            "formatVersion": 1,
            "passTypeIdentifier": pass_config.get("passTypeIdentifier", "pass.com.example.generic"),
            "serialNumber": pass_config.get("serialNumber", "123456789"),
            "teamIdentifier": team_id,
            "organizationName": pass_config.get("organizationName", "My Organization"),
            "description": pass_config.get("description", "Digital Business Card"),
            "logoText": pass_config.get("logoText", ""),
            "foregroundColor": pass_config.get("foregroundColor", "rgb(255,255,255)"),
            "backgroundColor": pass_config.get("backgroundColor", "rgb(0,77,153)"),
            "labelColor": pass_config.get("labelColor", "rgb(255,255,255)"),
        }

        # Note: Images are handled separately in pkpass_generator
        # We don't include image paths in pass.json - they're copied directly

        # Build fields
        fields = pass_config.get("fields", {})
        pass_data["generic"] = {
            "primaryFields": fields.get("primaryFields", []),
            "secondaryFields": fields.get("secondaryFields", []),
            "auxiliaryFields": fields.get("auxiliaryFields", []),
            "backFields": fields.get("backFields", []),
        }

        # Add header fields if photo exists
        if photo_path.exists():
            pass_data["generic"]["headerFields"] = [
                {
                    "key": "photo",
                    "label": "",
                    "value": str(photo_path),
                }
            ]

        # Add barcode/QR code
        if qr_path and qr_path.exists():
            qr_data = config.get("qr_data", "")
            pass_data["barcodes"] = [
                {
                    "message": qr_data,
                    "format": "PKBarcodeFormatQR",
                    "messageEncoding": "iso-8859-1",
                }
            ]

        # Add relevant date if provided
        if "relevantDate" in pass_config:
            pass_data["relevantDate"] = pass_config["relevantDate"]

        # Add locations if provided
        if "locations" in pass_config:
            pass_data["locations"] = pass_config["locations"]

        # Add beacons if provided
        if "beacons" in pass_config:
            pass_data["beacons"] = pass_config["beacons"]

        return pass_data

