"""Vercel-compatible Flask application entrypoint."""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Set up paths for Vercel serverless environment
if not os.path.exists("output"):
    os.makedirs("output", exist_ok=True)
if not os.path.exists("assets/user"):
    os.makedirs("assets/user", exist_ok=True)

# Import the Flask app
from wallet_card.web.app import app

# Export for Vercel
__all__ = ["app"]

