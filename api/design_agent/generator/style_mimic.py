from typing import List, Dict, Any, Optional
import os

from core.styles import DesignStyle, StyleProfile
from core.color import ColorPalette
from analyzers.style_analyzer import StyleAnalyzer
from templates.base import get_template
from .template_filler import TemplateFiller


class StyleMimicGenerator:
    def __init__(self):
        self.analyzer = StyleAnalyzer()
        self.profile: Optional[StyleProfile] = None

    def learn(self, example_images: List[str]) -> StyleProfile:
        self.profile = self.analyzer.analyze_designs(example_images)
        return self.profile

    def learn_from_directory(self, directory: str, extensions: tuple = (".png", ".jpg", ".jpeg")) -> StyleProfile:
        images = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.lower().endswith(extensions)
        ]
        return self.learn(images)

    def generate(self, template_name: str, content: Dict[str, Any],
                 platform: str = "instagram_square",
                 style_index: int = 0) -> "Image.Image":
        if not self.profile or not self.profile.styles:
            raise RuntimeError("No style learned yet. Call learn() or learn_from_directory() first.")

        style = self.profile.styles[min(style_index, len(self.profile.styles) - 1)]
        filler = TemplateFiller(style=style)
        return filler.fill(template_name, content, platform)

    def generate_with_new_palette(self, template_name: str, content: Dict[str, Any],
                                   new_palette: ColorPalette,
                                   platform: str = "instagram_square",
                                   style_index: int = 0) -> "Image.Image":
        if not self.profile or not self.profile.styles:
            raise RuntimeError("No style learned yet.")

        base_style = self.profile.styles[min(style_index, len(self.profile.styles) - 1)]
        base_style.palette = new_palette
        base_style.name = f"{base_style.name}_remixed"

        filler = TemplateFiller(style=base_style)
        return filler.fill(template_name, content, platform)
