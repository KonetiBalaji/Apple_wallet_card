"""Minimalist Light business card template."""

from typing import Dict, Any
from .base_template import BaseTemplate


class MinimalistLightTemplate(BaseTemplate):
    """Minimalist light business card template - clean and simple."""

    def get_template_config(self) -> Dict[str, Any]:
        """Get minimalist light template configuration."""
        return {
            "pass": {
                "passTypeIdentifier": "pass.com.example.businesscard",
                "organizationName": "Business Card",
                "description": "Minimalist Light Business Card",
                "foregroundColor": "rgb(0,0,0)",
                "backgroundColor": "rgb(255,255,255)",
                "labelColor": "rgb(100,100,100)",
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

