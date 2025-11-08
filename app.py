"""Vercel-compatible Flask application entrypoint."""

import sys
import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.resolve()

# Add src to Python path (must be absolute)
src_path = PROJECT_ROOT / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Set up paths for Vercel serverless environment
output_dir = PROJECT_ROOT / "output"
assets_dir = PROJECT_ROOT / "assets" / "user"

output_dir.mkdir(parents=True, exist_ok=True)
assets_dir.mkdir(parents=True, exist_ok=True)

# Change to project root for relative paths to work
os.chdir(PROJECT_ROOT)

try:
    # Import the Flask app
    from wallet_card.web.app import app
    
    # Export for Vercel
    __all__ = ["app"]
except Exception as e:
    # If import fails, create a minimal error handler
    from flask import Flask
    app = Flask(__name__)
    
    @app.route("/")
    def error():
        return f"Error loading app: {str(e)}", 500
    
    __all__ = ["app"]

