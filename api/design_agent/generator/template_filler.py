from typing import Dict, Any, Optional
import os

from core.styles import DesignStyle, StyleProfile
from templates.base import get_template, list_templates


class TemplateFiller:
    def __init__(self, style: Optional[DesignStyle] = None):
        self.style = style

    def fill(self, template_name: str, content: Dict[str, Any],
             platform: str = "instagram_square",
             style: Optional[DesignStyle] = None) -> "Image.Image":
        use_style = style or self.style
        if not use_style:
            raise ValueError("A DesignStyle is required. Pass one or set it in the constructor.")

        template_cls = get_template(template_name)
        template = template_cls()
        template.setup(use_style, content)
        return template.render()

    def fill_multi(self, template_name: str, contents: list,
                   platform: str = "instagram_square",
                   style: Optional[DesignStyle] = None) -> list:
        return [self.fill(template_name, c, platform, style) for c in contents]
