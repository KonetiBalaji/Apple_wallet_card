"""Vercel-compatible Flask application entrypoint."""

import os
import sys
from pathlib import Path

# Get the project root directory (where app.py is located)
PROJECT_ROOT = Path(__file__).parent.resolve()

# Add src to Python path (must be absolute for Vercel)
src_path = PROJECT_ROOT / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Detect if we are running inside a serverless environment (Vercel/AWS Lambda)
IS_SERVERLESS = bool(
    os.environ.get("VERCEL")
    or os.environ.get("VERCEL_ENV")
    or os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
)

# Set up paths for serverless vs. local environments
if IS_SERVERLESS:
    # Serverless environments have a read-only project directory.
    # /tmp is the only writable location and is reset on every invocation.
    output_dir = Path("/tmp") / "output"
    assets_dir = Path("/tmp") / "assets" / "user"
else:
    # Local development can write inside the project directory.
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
    # If import fails, create a minimal error handler with detailed error
    import traceback
    error_details = traceback.format_exc()
    
    from flask import Flask
    app = Flask(__name__)
    
    @app.route("/")
    def error():
        return f"Error loading app: {str(e)}\n\nDetails:\n{error_details}", 500
    
    __all__ = ["app"]

