"""Bold Red business card template."""

from typing import Dict, Any
from .base_template import BaseTemplate


class BoldRedTemplate(BaseTemplate):
    """Bold red business card template - energetic and attention-grabbing."""

    def get_template_config(self) -> Dict[str, Any]:
        """Get bold red template configuration."""
        return {
            "pass": {
                "passTypeIdentifier": "pass.com.example.businesscard",
                "organizationName": "Business Card",
                "description": "Bold Red Business Card",
                "foregroundColor": "rgb(255,255,255)",
                "backgroundColor": "rgb(178,34,34)",
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

