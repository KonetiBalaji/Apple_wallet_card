"""Elegant Purple business card template."""

from typing import Dict, Any
from .base_template import BaseTemplate


class ElegantPurpleTemplate(BaseTemplate):
    """Elegant purple business card template - creative and sophisticated."""

    def get_template_config(self) -> Dict[str, Any]:
        """Get elegant purple template configuration."""
        return {
            "pass": {
                "passTypeIdentifier": "pass.com.example.businesscard",
                "organizationName": "Business Card",
                "description": "Elegant Purple Business Card",
                "foregroundColor": "rgb(255,255,255)",
                "backgroundColor": "rgb(138,43,226)",
                "labelColor": "rgb(255,255,255)",
                "fields": {
                    "primaryFields": [
                        {"key": "name", "label": "Name", "value": ""}
                    ],
                    "secondaryFields": [
                        {"key": "title", "label": "Title", "value": ""},
                        {"key": "email", "label": "Email", "value": ""}
                    ],
                    "auxiliaryFields": [
                        {"key": "phone", "label": "Phone", "value": ""}
                    ],
                    "backFields": [
                        {"key": "linkedin", "label": "LinkedIn", "value": ""},
                        {"key": "github", "label": "GitHub", "value": ""},
                        {"key": "website", "label": "Website", "value": ""}
                    ],
                },
            },
            "assets": {},
            "qr_data": "",
            "signing": {
                "enabled": False,
            },
        }

