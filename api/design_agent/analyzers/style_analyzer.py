import os
from typing import List, Dict, Optional
from PIL import Image
import numpy as np

from core.styles import DesignStyle, StyleProfile, TextStyle, LayoutStyle, EffectStyle
from core.color import ColorPalette
from .color_analyzer import ColorAnalyzer


class StyleAnalyzer:
    def __init__(self):
        self.color_analyzer = ColorAnalyzer()

    def analyze_designs(self, image_paths: List[str]) -> StyleProfile:
        profile = StyleProfile()
        all_palettes = []
        common_fonts = set()
        layout_patterns = []

        for path in image_paths:
            try:
                analysis = self.color_analyzer.analyze(path)
                all_palettes.append(analysis["palette"])

                style = self._extract_style_from_image(path, analysis)
                profile.add_style(style)

                layout_patterns.append(analysis.get("composition", "center"))
            except Exception as e:
                print(f"Warning: Could not analyze {path}: {e}")

        if all_palettes:
            avg_colors = self._average_palettes(all_palettes)
            profile.brand_colors = ColorPalette(colors=avg_colors, name="brand")

        profile.common_layouts = list(set(layout_patterns)) if layout_patterns else ["center"]

        return profile

    def _extract_style_from_image(self, image_path: str, analysis: Dict) -> DesignStyle:
        img = Image.open(image_path).convert("RGB")
        w, h = img.size

        palette = analysis["palette"]
        title_font_size = self._estimate_title_size(w, h)

        effects = EffectStyle(
            gradient_overlay=analysis.get("mood") in ("vibrant", "dark"),
            overlay_opacity=0.15 if analysis["brightness"] > 0.5 else 0.3,
        )

        text_color = palette.get_text_color(0)

        style = DesignStyle(
            name=os.path.basename(image_path),
            palette=palette,
            title_style=TextStyle(
                font_size=title_font_size,
                font_weight="bold",
                color=text_color,
            ),
            subtitle_style=TextStyle(
                font_size=max(title_font_size // 2, 20),
                font_weight="normal",
                color=text_color,
            ),
            effects=effects,
        )

        return style

    def _estimate_title_size(self, width: int, height: int) -> int:
        size = min(width, height) // 15
        return max(24, min(72, size))

    def _average_palettes(self, palettes: List[ColorPalette]) -> List[tuple]:
        if not palettes:
            return [(26, 26, 46), (22, 33, 62), (233, 69, 96)]

        min_len = min(len(p.colors) for p in palettes)
        if min_len == 0:
            return [(26, 26, 46), (22, 33, 62), (233, 69, 96)]

        avg_colors = []
        for i in range(min_len):
            avg = tuple(
                int(np.mean([p.colors[i][c] for p in palettes]))
                for c in range(3)
            )
            avg_colors.append(avg)

        return avg_colors

    def quick_style_from_image(self, image_path: str) -> DesignStyle:
        analysis = self.color_analyzer.analyze(image_path)
        return self._extract_style_from_image(image_path, analysis)
