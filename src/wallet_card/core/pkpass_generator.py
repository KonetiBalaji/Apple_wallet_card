"""Custom pkpass file generator (replacement for wallet-passes library)."""

import json
import hashlib
import zipfile
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import x509


class PKPassGenerator:
    """Generates Apple Wallet .pkpass files without external library."""

    def __init__(
        self,
        pass_data: Dict[str, Any],
        cert_file: Optional[str] = None,
        key_file: Optional[str] = None,
    ):
        """Initialize pkpass generator.

        Args:
            pass_data: Pass data dictionary
            cert_file: Optional path to certificate file
            key_file: Optional path to key file
        """
        self.pass_data = pass_data
        self.cert_file = cert_file
        self.key_file = key_file

    def create(self, output_dir: Path) -> None:
        """Create pkpass structure in output directory.

        Args:
            output_dir: Directory to create pass files in
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Clean pass_data - remove image paths from JSON (images are separate files)
        import copy
        clean_pass_data = copy.deepcopy(self.pass_data)
        if "images" in clean_pass_data:
            # Remove image paths from JSON - they're handled as separate files
            del clean_pass_data["images"]
        
        # Clean headerFields - remove file paths
        if "generic" in clean_pass_data and "headerFields" in clean_pass_data["generic"]:
            for field in clean_pass_data["generic"]["headerFields"]:
                if "value" in field and isinstance(field["value"], str) and ("/" in field["value"] or "\\" in field["value"]):
                    # It's a file path, remove it
                    field["value"] = ""
        
        # Write pass.json
        pass_json_path = output_dir / "pass.json"
        with open(pass_json_path, "w", encoding="utf-8") as f:
            json.dump(clean_pass_data, f, indent=2, ensure_ascii=False)

        # Copy images if they exist in pass_data
        import shutil
        if "images" in self.pass_data:
            for image_type, image_path in self.pass_data["images"].items():
                if image_path and Path(image_path).exists():
                    dest_path = output_dir / f"{image_type}.png"
                    shutil.copy2(image_path, dest_path)

        # Handle headerFields with photo (strip image)
        if "generic" in self.pass_data:
            generic = self.pass_data["generic"]
            if "headerFields" in generic:
                # Clean headerFields - remove file paths, keep only structure
                for field in generic["headerFields"]:
                    if field.get("key") == "photo" and "value" in field:
                        photo_path = Path(field["value"])
                        if photo_path.exists():
                            # For generic passes, photo goes in strip.png
                            dest_path = output_dir / "strip.png"
                            shutil.copy2(photo_path, dest_path)
                        # Remove the file path from the field - just keep the structure
                        field["value"] = ""  # Empty value, image is in strip.png

        # Create manifest.json
        manifest = self._create_manifest(output_dir)
        manifest_path = output_dir / "manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        # Create signature - Apple Wallet requires this file
        signature_path = output_dir / "signature"
        if self.cert_file and self.key_file:
            signature = self._create_signature(manifest_path)
            with open(signature_path, "wb") as f:
                f.write(signature)
        else:
            # For unsigned passes, create a minimal signature placeholder
            # Some iOS versions require at least some content in signature file
            # This is a workaround - not cryptographically valid but may work for personal use
            with open(signature_path, "wb") as f:
                # Write a minimal placeholder (some systems check for non-empty file)
                f.write(b"UNSIGNED")

    def _create_manifest(self, pass_dir: Path) -> Dict[str, str]:
        """Create manifest.json with SHA1 hashes of all files.

        Args:
            pass_dir: Directory containing pass files

        Returns:
            Manifest dictionary mapping filenames to SHA1 hashes
        """
        manifest = {}
        # Create manifest BEFORE creating signature file
        for file_path in pass_dir.iterdir():
            if file_path.is_file() and file_path.name != "manifest.json" and file_path.name != "signature":
                with open(file_path, "rb") as f:
                    content = f.read()
                    sha1_hash = hashlib.sha1(content).hexdigest()
                    manifest[file_path.name] = sha1_hash
        return manifest

    def _create_signature(self, manifest_path: Path) -> bytes:
        """Create signature for manifest.json.

        Args:
            manifest_path: Path to manifest.json

        Returns:
            Signature bytes
        """
        try:
            # Read certificate and key
            with open(self.cert_file, "rb") as f:
                cert_data = f.read()
            with open(self.key_file, "rb") as f:
                key_data = f.read()

            # Try to load as PEM
            try:
                cert = x509.load_pem_x509_certificate(cert_data)
                private_key = serialization.load_pem_private_key(
                    key_data, password=None
                )
            except Exception as e:
                raise ValueError(f"Failed to load certificate/key: {e}")

            # Read manifest content
            with open(manifest_path, "rb") as f:
                manifest_content = f.read()

            # Sign manifest using SHA1 with PKCS1v15 padding (required by Apple Wallet)
            # Apple Wallet expects PKCS1v15 padding with SHA1
            signature = private_key.sign(
                manifest_content,
                padding.PKCS1v15(),
                hashes.SHA1()
            )

            return signature

        except Exception as e:
            raise RuntimeError(f"Failed to create signature: {e}") from e

