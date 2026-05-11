from typing import Dict, Any, Optional, List, Tuple
import os
import json
import re

from core.styles import DesignStyle, TextStyle, LayoutStyle, EffectStyle, TextAlignment
from core.color import ColorPalette
from templates.base import get_template, list_templates
from llm.client import LLMClient


_PRESET_PALETTES = {
    "sunset": ["#2D1B69", "#E43A6F", "#F7A46C", "#F9D56E", "#FFFFFF"],
    "ocean": ["#0A192F", "#0F4C75", "#3282B8", "#BBE1FA", "#FFFFFF"],
    "forest": ["#1B4332", "#2D6A4F", "#40916C", "#95D5B2", "#FFFFFF"],
    "midnight": ["#0F0F0F", "#1A1A2E", "#16213E", "#E94560", "#FFFFFF"],
    "minimal": ["#FFFFFF", "#F5F5F5", "#333333", "#666666", "#000000"],
    "warm": ["#FFF3E0", "#FFE0B2", "#FFB74D", "#E65100", "#FFFFFF"],
    "neon": ["#0A0A0A", "#FF007F", "#00F5FF", "#7B2FFF", "#FFFFFF"],
    "pastel": ["#F8EDE3", "#DFD3C3", "#D0B8A8", "#7D6E83", "#FFFFFF"],
    "luxury": ["#1A1A1A", "#C9A84C", "#F5E6CC", "#8B7355", "#FFFFFF"],
    "dark_modern": ["#121212", "#1E1E1E", "#BB86FC", "#03DAC6", "#FFFFFF"],
}


class TextToDesignGenerator:
    def __init__(self, llm_api_key: Optional[str] = None):
        self.llm = LLMClient(api_key=llm_api_key) if llm_api_key else None

    def generate(self, prompt: str, platform: str = "instagram_square") -> Dict[str, Any]:
        if self.llm:
            design_spec = self.llm.interpret_design_prompt(prompt, platform)
        else:
            design_spec = self._rule_based_parse(prompt, platform)

        style = self._build_style(design_spec)
        content = self._build_content(design_spec)
        template_name = design_spec.get("template", self._suggest_template(platform, design_spec))

        template_cls = get_template(template_name)
        template = template_cls()
        template.setup(style, content)

        return {
            "template": template,
            "style": style,
            "content": content,
            "spec": design_spec,
        }

    def render(self, prompt: str, platform: str = "instagram_square", output_path: Optional[str] = None) -> str:
        result = self.generate(prompt, platform)
        img = result["template"].render()

        if output_path:
            img.save(output_path)
            return output_path

        safe_name = re.sub(r'[^\w\s-]', '', prompt)[:50].strip().replace(' ', '_')
        os.makedirs("output", exist_ok=True)
        path = f"output/{safe_name}.png"
        img.save(path)
        return path

    def _rule_based_parse(self, prompt: str, platform: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower()

        mood_keywords = {
            "dark": "dark", "moody": "dark", "night": "dark",
            "bright": "vibrant", "vibrant": "vibrant", "colorful": "vibrant",
            "minimal": "minimalist", "clean": "minimalist", "simple": "minimalist",
            "warm": "warm", "cozy": "warm", "sunset": "warm",
            "calm": "calm", "peaceful": "calm", "serene": "calm",
            "luxury": "luxury", "elegant": "luxury", "premium": "luxury",
        }

        palette_name = "minimal"
        for keyword, palette in mood_keywords.items():
            if keyword in prompt_lower:
                palette_name = palette
                break

        palette_colors = _PRESET_PALETTES.get(palette_name, _PRESET_PALETTES["minimal"])
        palette = ColorPalette.from_hex_list(palette_colors, name=palette_name)

        font_size = 48 if platform in ("instagram_story", "pinterest") else 36

        template_map = {
            "quote": "quote_card",
            "story": "instagram_story",
            "thumbnail": "youtube_thumbnail",
            "youtube": "youtube_thumbnail",
            "pin": "pinterest",
            "twitter": "twitter_post",
        }

        template = "instagram_square"
        for keyword, t in template_map.items():
            if keyword in prompt_lower:
                template = t
                break

        title = self._extract_title(prompt)
        subtitle = self._extract_subtitle(prompt)

        return {
            "palette": palette_name,
            "palette_colors": palette_colors,
            "template": template,
            "title": title,
            "subtitle": subtitle,
            "mood": palette_name,
            "font_size": font_size,
            "platform": platform,
        }

    def _extract_title(self, prompt: str) -> str:
        lines = [l.strip() for l in prompt.split("\n") if l.strip()]
        if lines:
            return lines[0]
        return prompt[:80]

    def _extract_subtitle(self, prompt: str) -> str:
        lines = [l.strip() for l in prompt.split("\n") if l.strip()]
        if len(lines) > 1:
            return lines[1]
        return ""

    def _build_style(self, spec: Dict[str, Any]) -> DesignStyle:
        palette = ColorPalette.from_hex_list(spec.get("palette_colors", _PRESET_PALETTES["minimal"]))
        text_color = palette.get_text_color(0)

        return DesignStyle(
            name=f"generated_{spec.get('mood', 'custom')}",
            palette=palette,
            title_style=TextStyle(
                font_size=spec.get("font_size", 48),
                font_weight="bold",
                color=text_color,
            ),
            subtitle_style=TextStyle(
                font_size=max(int(spec.get("font_size", 48) * 0.5), 20),
                font_weight="normal",
                color=text_color,
            ),
            layout=LayoutStyle(grid_type="center"),
            effects=EffectStyle(
                gradient_overlay=spec.get("mood") in ("vibrant", "dark", "luxury"),
                overlay_opacity=0.2,
            ),
        )

    def _build_content(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": spec.get("title", "Your Design"),
            "subtitle": spec.get("subtitle", ""),
            "body": spec.get("body", ""),
            "quote": spec.get("title", ""),
            "author": spec.get("subtitle", ""),
            "background_image": spec.get("background_image", ""),
        }

    def _suggest_template(self, platform: str, spec: Dict) -> str:
        if spec.get("template") != "instagram_square":
            return spec["template"]

        platform_map = {
            "instagram_square": "instagram_square",
            "instagram_story": "instagram_story",
            "twitter_post": "twitter_post",
            "youtube_thumbnail": "youtube_thumbnail",
            "pinterest": "pinterest",
        }
        return platform_map.get(platform, "instagram_square")
