"""Modern Dark business card template."""

from typing import Dict, Any
from .base_template import BaseTemplate


class ModernDarkTemplate(BaseTemplate):
    """Modern dark business card template - sleek and contemporary."""

    def get_template_config(self) -> Dict[str, Any]:
        """Get modern dark template configuration."""
        return {
            "pass": {
                "passTypeIdentifier": "pass.com.example.businesscard",
                "organizationName": "Business Card",
                "description": "Modern Dark Business Card",
                "foregroundColor": "rgb(255,255,255)",
                "backgroundColor": "rgb(30,30,30)",
                "labelColor": "rgb(200,200,200)",
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

