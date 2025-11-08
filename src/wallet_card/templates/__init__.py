"""Template system for different pass types."""

from .base_template import BaseTemplate
from .business_card import BusinessCardTemplate
from .classic_blue import ClassicBlueTemplate
from .modern_dark import ModernDarkTemplate
from .professional_green import ProfessionalGreenTemplate
from .elegant_purple import ElegantPurpleTemplate
from .bold_red import BoldRedTemplate
from .minimalist_light import MinimalistLightTemplate

__all__ = [
    "BaseTemplate",
    "BusinessCardTemplate",
    "ClassicBlueTemplate",
    "ModernDarkTemplate",
    "ProfessionalGreenTemplate",
    "ElegantPurpleTemplate",
    "BoldRedTemplate",
    "MinimalistLightTemplate",
]

