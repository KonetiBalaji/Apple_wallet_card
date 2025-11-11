"""Flask web application for wallet card generator."""

import os
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename

from ..core.validator import Validator, ValidationError
from ..templates.bold_red import BoldRedTemplate
from ..templates.business_card import BusinessCardTemplate
from ..templates.classic_blue import ClassicBlueTemplate
from ..templates.elegant_purple import ElegantPurpleTemplate
from ..templates.minimalist_light import MinimalistLightTemplate
from ..templates.modern_dark import ModernDarkTemplate
from ..templates.professional_green import ProfessionalGreenTemplate
from ..utils.config_loader import ConfigLoader

# Get the directory where this file is located
BASE_DIR = Path(__file__).parent
# Use absolute path for templates
template_path = BASE_DIR / "templates"
app = Flask(__name__, template_folder=str(template_path.resolve()))
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Absolute paths & environment detection for serverless
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
IS_SERVERLESS = bool(
    os.environ.get("VERCEL")
    or os.environ.get("VERCEL_ENV")
    or os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
)

if IS_SERVERLESS:
    # Vercel (and other serverless environments) expose /tmp as the only writable location.
    UPLOAD_FOLDER = Path("/tmp") / "assets" / "user"
    OUTPUT_FOLDER = Path("/tmp") / "output"
else:
    # Local development can safely use the project directory.
    UPLOAD_FOLDER = PROJECT_ROOT / "assets" / "user"
    OUTPUT_FOLDER = PROJECT_ROOT / "output"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Ensure upload directory exists
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Render main page."""
    return render_template("index.html")


@app.route("/test")
def test_link():
    """Test page for direct pass link."""
    return render_template("test_direct_link.html")


@app.route("/api/generate", methods=["POST"])
def generate():
    """Generate wallet card from form data."""
    try:
        # Get form data
        data = request.form.to_dict()

        # Handle file uploads
        assets = {}
        for asset_type in ["icon", "logo", "photo"]:
            if asset_type in request.files:
                file = request.files[asset_type]
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(f"{asset_type}.{file.filename.rsplit('.', 1)[1].lower()}")
                    filepath = UPLOAD_FOLDER / filename
                    file.save(str(filepath))
                    assets[asset_type] = str(filepath)

        # Build configuration
        config = {
            "pass": {
                "passTypeIdentifier": data.get("passTypeIdentifier", "pass.com.example.businesscard"),
                "serialNumber": data.get("serialNumber", "123456789"),
                "organizationName": data.get("organizationName", "My Organization"),
                "description": data.get("description", "Digital Business Card"),
                "logoText": data.get("logoText", ""),
                "foregroundColor": data.get("foregroundColor", "rgb(255,255,255)"),
                "backgroundColor": data.get("backgroundColor", "rgb(0,77,153)"),
                "labelColor": data.get("labelColor", "rgb(255,255,255)"),
                "fields": {
                    "primaryFields": [
                        {"key": "name", "label": "Name", "value": data.get("name", "")}
                    ],
                    "secondaryFields": [
                        {"key": "title", "label": "Title", "value": data.get("title", "")},
                        {"key": "email", "label": "Email", "value": data.get("email", "")}
                    ],
                    "auxiliaryFields": [
                        {"key": "phone", "label": "Phone", "value": data.get("phone", "")}
                    ],
                    "backFields": [
                        {"key": "linkedin", "label": "LinkedIn", "value": data.get("linkedin", "")},
                        {"key": "github", "label": "GitHub", "value": data.get("github", "")},
                        {"key": "website", "label": "Website", "value": data.get("website", "")}
                    ],
                },
            },
            "assets": assets,
            "qr_data": data.get("qr_data", data.get("website", "")),
            "signing": {
                "enabled": False,
            },
        }
        
        # Auto-detect and use certificate if available (use absolute paths)
        cert_file = None
        key_file = None
        cert_path = PROJECT_ROOT / "signer.pem"
        key_path = PROJECT_ROOT / "signer.key"

        # For serverless environments, also allow /tmp for runtime-provided certs
        if IS_SERVERLESS:
            tmp_cert = Path("/tmp") / "signer.pem"
            tmp_key = Path("/tmp") / "signer.key"
            if tmp_cert.exists() and tmp_key.exists():
                cert_path = tmp_cert
                key_path = tmp_key
        if cert_path.exists() and key_path.exists():
            cert_file = str(cert_path)
            key_file = str(key_path)
            config["signing"]["enabled"] = True
            config["signing"]["cert_file"] = cert_file
            config["signing"]["key_file"] = key_file

        # Validate
        errors = Validator.validate_config(config)
        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        # Get template style from form
        template_style = data.get("template_style", "classic-blue")
        
        # Select template based on style
        template_classes = {
            "classic-blue": ClassicBlueTemplate,
            "modern-dark": ModernDarkTemplate,
            "professional-green": ProfessionalGreenTemplate,
            "elegant-purple": ElegantPurpleTemplate,
            "bold-red": BoldRedTemplate,
            "minimalist-light": MinimalistLightTemplate,
        }
        
        template_class = template_classes.get(template_style, ClassicBlueTemplate)
        # Pass absolute paths to template for Vercel compatibility
        template = template_class(
            assets_dir=str(UPLOAD_FOLDER),
            output_dir=str(OUTPUT_FOLDER),
            cert_file=cert_file,
            key_file=key_file,
        )
        output_path = template.generate(config)
        
        # Verify the file exists before generating QR code
        if not output_path.exists():
            return jsonify({"success": False, "errors": [f"Generated file not found: {output_path}"]}), 500
        
        # Check if user wants QR code instead
        output_type = data.get("output_type", "wallet")

        if output_type == "qr":
            # Generate QR code that links to the Wallet pass file
            # This way scanning the QR code opens the .pkpass file
            # For local testing: use network IP so iPhone can access
            # For production: recommend hosting .pkpass on public server

            import socket
            try:
                # Get network IP for local access
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                network_ip = s.getsockname()[0]
                s.close()

                # For development: use network IP
                # For production: recommend hosting on public server
                host = f"{network_ip}:5000"
                production_note = "⚠️ For sharing: Host .pkpass on public server (Vercel/Netlify) and update QR code URL"

            except Exception as e:
                host = request.host
                production_note = "⚠️ Network detection failed - host .pkpass publicly for sharing"

            # Use the actual filename from the generated pass
            pass_filename = output_path.name
            if not output_path.exists():
                return jsonify({"success": False, "errors": [f"Generated pass file not found: {output_path}"]}), 500

            pass_url = f"http://{host}/api/download/{pass_filename}"
            qr_path = _generate_qr_code_for_wallet(pass_url, data, OUTPUT_FOLDER)
            return jsonify({
                "success": True,
                "filename": qr_path.name,
                "download_url": f"/api/download/{qr_path.name}",
                "type": "qr",
                "pass_url": pass_url,
                "production_note": production_note if 'production_note' in locals() else ""
            })
        
        return jsonify({
            "success": True,
            "filename": output_path.name,
            "download_url": f"/api/download/{output_path.name}",
            "type": "wallet"
        })

    except ValidationError as e:
        return jsonify({"success": False, "errors": [str(e)]}), 400
    except Exception as e:
        return jsonify({"success": False, "errors": [str(e)]}), 500


@app.route("/api/download/<filename>")
def download(filename: str):
    """Download generated .pkpass or QR code file."""
    # Use absolute path from project root
    filepath = OUTPUT_FOLDER / secure_filename(filename)
    
    # Debug: log the request
    import logging
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO)
    logger.info(f"Download request: filename={filename}, path={filepath}, exists={filepath.exists()}, suffix={filepath.suffix}")
    
    if not filepath.exists():
        # Try to find the file without secure_filename (in case it was already sanitized)
        alt_filepath = OUTPUT_FOLDER / filename
        if alt_filepath.exists():
            filepath = alt_filepath
        else:
            # List available files for debugging
            available_files = list(OUTPUT_FOLDER.glob("*.pkpass")) if OUTPUT_FOLDER.exists() else []
            return jsonify({
                "error": "File not found",
                "searched_path": str(filepath),
                "alt_path": str(alt_filepath),
                "requested_filename": filename,
                "available_files": [f.name for f in available_files]
            }), 404
    
    # Handle .pkpass files
    if filepath.suffix.lower() == ".pkpass" or filename.endswith(".pkpass"):
        # For Safari on iPhone: don't force download, let Safari handle it
        # Safari will automatically prompt "Add to Wallet" when it detects .pkpass
        from flask import Response
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            response = Response(
                data,
                mimetype="application/vnd.apple.pkpass",
                headers={
                    "Content-Disposition": f'inline; filename="{filename}"',
                    "Content-Type": "application/vnd.apple.pkpass",
                }
            )
            return response
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return jsonify({"error": f"Error reading file: {str(e)}"}), 500
    
    # Handle image files (QR code)
    if filepath.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif"]:
        return send_file(
            str(filepath),
            mimetype=f"image/{filepath.suffix[1:].lower()}",
            as_attachment=True,
            download_name=filename
        )
    
    # If we get here, log what we're trying to serve
    logger.warning(f"Unsupported file type: {filepath.suffix}, filename: {filename}, path: {filepath}")
    return jsonify({
        "error": "Unsupported file type",
        "filename": filename,
        "extension": filepath.suffix,
        "path": str(filepath)
    }), 400


def _generate_qr_code_for_wallet(pass_url: str, data: dict, output_dir: Path) -> Path:
    """Generate QR code that links to Wallet pass file."""
    name = data.get("name", "")
    title = data.get("title", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    website = data.get("website", "")
    
    # Generate QR code with the Wallet pass URL
    # When scanned, iPhone will open the .pkpass file
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(pass_url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Create business card image
    card_width = 800
    card_height = 500
    card = Image.new('RGB', (card_width, card_height), color='white')
    draw = ImageDraw.Draw(card)
    
    # Try to use a nice font
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        font_tiny = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
    
    # Add QR code (left side)
    qr_size = 300
    qr_resized = qr_img.resize((qr_size, qr_size))
    card.paste(qr_resized, (50, 100))
    
    # Add text (right side)
    y_pos = 100
    draw.text((400, y_pos), name, fill='black', font=font_large)
    y_pos += 50
    if title:
        draw.text((400, y_pos), title, fill='gray', font=font_medium)
        y_pos += 60
    if email:
        draw.text((400, y_pos), f"📧 {email}", fill='black', font=font_small)
        y_pos += 40
    if phone:
        draw.text((400, y_pos), f"📱 {phone}", fill='black', font=font_small)
        y_pos += 40
    if website:
        draw.text((400, y_pos), f"🌐 {website}", fill='blue', font=font_small)
        y_pos += 40
    
    # Add instruction text
    y_pos += 20
    draw.text((400, y_pos), "📱 Scan to add to Wallet", fill='green', font=font_small)
    y_pos += 30
    draw.text((400, y_pos), "Open in Safari on iPhone", fill='gray', font=font_tiny)
    
    # Save
    safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name) if name else "business_card"
    output_file = output_dir / f"{safe_name}_qr.png"
    card.save(output_file)
    
    return output_file


@app.route("/api/files", methods=["GET"])
def list_files():
    """List available .pkpass files for debugging."""
    output_dir = OUTPUT_FOLDER
    
    if not output_dir.exists():
        return jsonify({"files": [], "error": "Output directory not found"})
    
    files = list(output_dir.glob("*.pkpass"))
    return jsonify({
        "files": [f.name for f in files],
        "count": len(files)
    })


@app.route("/api/validate", methods=["POST"])
def validate():
    """Validate configuration."""
    try:
        config = request.get_json()
        errors = Validator.validate_config(config)

        if errors:
            return jsonify({"valid": False, "errors": errors}), 400
        return jsonify({"valid": True})

    except Exception as e:
        return jsonify({"valid": False, "errors": [str(e)]}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

