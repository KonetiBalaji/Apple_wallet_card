"""Business card template implementation."""

from typing import Dict, Any
from .base_template import BaseTemplate


class BusinessCardTemplate(BaseTemplate):
    """Template for business card passes."""

    def get_template_config(self) -> Dict[str, Any]:
        """Get default business card template configuration.

        Returns:
            Template configuration dictionary
        """
        return {
            "pass": {
                "passTypeIdentifier": "pass.com.example.businesscard",
                "organizationName": "Business Card",
                "description": "Digital Business Card",
                "foregroundColor": "rgb(255,255,255)",
                "backgroundColor": "rgb(0,77,153)",
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

