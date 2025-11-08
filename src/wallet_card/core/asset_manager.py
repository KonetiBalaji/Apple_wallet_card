"""Asset management for images and QR codes."""

import os
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.image.pil import PilImage


class AssetManager:
    """Manages image assets and QR code generation."""

    # Required image sizes for Apple Wallet
    ICON_SIZE = (180, 180)
    LOGO_SIZE = (320, 100)
    PHOTO_SIZE = (320, 320)

    def __init__(self, assets_dir: str = "assets/user"):
        """Initialize asset manager.

        Args:
            assets_dir: Directory containing user assets
        """
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(parents=True, exist_ok=True)

    def ensure_image_exists(
        self, filename: str, size: Tuple[int, int], default_color: str = "#4A90E2"
    ) -> Path:
        """Ensure an image exists, creating a placeholder if missing.

        Args:
            filename: Name of the image file
            size: Required size (width, height)
            default_color: Color for placeholder

        Returns:
            Path to the image file
        """
        image_path = self.assets_dir / filename

        if not image_path.exists():
            self._create_placeholder_image(image_path, size, default_color)

        return image_path

    def _create_placeholder_image(
        self, path: Path, size: Tuple[int, int], color: str
    ) -> None:
        """Create a placeholder image.

        Args:
            path: Path where to save the image
            size: Image dimensions
            color: Background color
        """
        img = Image.new("RGB", size, color)
        draw = ImageDraw.Draw(img)

        # Try to use a font, fallback to default if not available
        try:
            font_size = min(size) // 4
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except (OSError, AttributeError):
            font = ImageFont.load_default()

        text = path.stem.upper()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = (
            (size[0] - text_width) // 2,
            (size[1] - text_height) // 2,
        )

        draw.text(position, text, fill="white", font=font)
        img.save(path, "PNG")

    def prepare_icon(self, icon_path: Optional[str] = None) -> Path:
        """Prepare icon image (180x180).

        Args:
            icon_path: Optional path to custom icon

        Returns:
            Path to prepared icon
        """
        if icon_path and Path(icon_path).exists():
            return self._resize_image(Path(icon_path), self.ICON_SIZE, "icon.png")

        return self.ensure_image_exists("icon.png", self.ICON_SIZE)

    def prepare_logo(self, logo_path: Optional[str] = None) -> Path:
        """Prepare logo image (320x100).

        Args:
            logo_path: Optional path to custom logo

        Returns:
            Path to prepared logo
        """
        if logo_path and Path(logo_path).exists():
            return self._resize_image(Path(logo_path), self.LOGO_SIZE, "logo.png")

        return self.ensure_image_exists("logo.png", self.LOGO_SIZE)

    def prepare_photo(self, photo_path: Optional[str] = None) -> Path:
        """Prepare photo image (320x320).

        Args:
            photo_path: Optional path to custom photo

        Returns:
            Path to prepared photo
        """
        if photo_path and Path(photo_path).exists():
            return self._resize_image(Path(photo_path), self.PHOTO_SIZE, "photo.png")

        return self.ensure_image_exists("photo.png", self.PHOTO_SIZE)

    def _resize_image(
        self, source_path: Path, target_size: Tuple[int, int], output_name: str
    ) -> Path:
        """Resize an image to target size.

        Args:
            source_path: Path to source image
            target_size: Target dimensions
            output_name: Name for output file

        Returns:
            Path to resized image
        """
        output_path = self.assets_dir / output_name

        with Image.open(source_path) as img:
            # Convert to RGB if necessary
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Resize maintaining aspect ratio, then crop to exact size
            img.thumbnail(target_size, Image.Resampling.LANCZOS)

            # Create new image with target size and paste resized image
            new_img = Image.new("RGB", target_size, (255, 255, 255))
            paste_x = (target_size[0] - img.size[0]) // 2
            paste_y = (target_size[1] - img.size[1]) // 2
            new_img.paste(img, (paste_x, paste_y))

            new_img.save(output_path, "PNG")

        return output_path

    def generate_qr_code(
        self, data: str, output_name: str = "qr.png", size: int = 200
    ) -> Path:
        """Generate a QR code image.

        Args:
            data: Data to encode in QR code
            output_name: Name for output file
            size: Size of QR code image

        Returns:
            Path to generated QR code
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((size, size), Image.Resampling.LANCZOS)

        output_path = self.assets_dir / output_name
        img.save(output_path, "PNG")

        return output_path

    def get_asset_path(self, filename: str) -> Optional[Path]:
        """Get path to an asset file.

        Args:
            filename: Name of the asset file

        Returns:
            Path to asset or None if not found
        """
        path = self.assets_dir / filename
        return path if path.exists() else None

