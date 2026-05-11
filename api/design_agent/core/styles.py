from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
from .color import ColorPalette


class TextAlignment(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class VerticalAlignment(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"


@dataclass
class TextStyle:
    font_family: str = "Arial"
    font_size: int = 48
    font_weight: str = "bold"
    color: Tuple[int, int, int] = (255, 255, 255)
    alignment: TextAlignment = TextAlignment.CENTER
    line_spacing: float = 1.2
    letter_spacing: float = 0.0
    shadow: Optional[Dict] = None
    outline: Optional[Dict] = None
    opacity: float = 1.0


@dataclass
class LayoutStyle:
    padding: Dict[str, int] = field(default_factory=lambda: {"top": 40, "bottom": 40, "left": 40, "right": 40})
    content_width_pct: float = 0.85
    content_height_pct: float = 0.80
    grid_type: str = "center"  # center, top-third, rule-of-thirds, split, split-diagonal


@dataclass
class EffectStyle:
    gradient_overlay: bool = False
    gradient_colors: Optional[List[Tuple[int,int,int]]] = None
    overlay_opacity: float = 0.0
    border_radius: int = 0
    shadow: bool = False
    shadow_offset: Tuple[int, int] = (0, 4)
    shadow_blur: int = 10
    shadow_color: Tuple[int, int, int, int] = (0, 0, 0, 80)


@dataclass
class DesignStyle:
    palette: ColorPalette = field(default_factory=ColorPalette)
    title_style: TextStyle = field(default_factory=TextStyle)
    subtitle_style: TextStyle = field(default_factory=lambda: TextStyle(font_size=28, font_weight="normal"))
    body_style: TextStyle = field(default_factory=lambda: TextStyle(font_size=22, font_weight="normal"))
    layout: LayoutStyle = field(default_factory=LayoutStyle)
    effects: EffectStyle = field(default_factory=EffectStyle)
    name: str = "custom_style"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "palette": self.palette.to_hex(),
            "title_font_size": self.title_style.font_size,
            "title_font_family": self.title_style.font_family,
            "title_font_weight": self.title_style.font_weight,
            "subtitle_font_size": self.subtitle_style.font_size,
            "body_font_size": self.body_style.font_size,
            "layout_grid": self.layout.grid_type,
            "effects_gradient": self.effects.gradient_overlay,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DesignStyle":
        palette = ColorPalette.from_hex_list(data.get("palette", ["#1a1a2e", "#16213e", "#e94560"]))
        return cls(
            palette=palette,
            title_style=TextStyle(
                font_family=data.get("title_font_family", "Arial"),
                font_size=data.get("title_font_size", 48),
                font_weight=data.get("title_font_weight", "bold"),
            ),
            subtitle_style=TextStyle(
                font_family=data.get("title_font_family", "Arial"),
                font_size=data.get("subtitle_font_size", 28),
                font_weight="normal",
            ),
            name=data.get("name", "imported"),
        )


@dataclass
class StyleProfile:
    styles: List[DesignStyle] = field(default_factory=list)
    brand_colors: ColorPalette = field(default_factory=ColorPalette)
    preferred_fonts: List[str] = field(default_factory=lambda: ["Arial", "Helvetica", "Montserrat", "Roboto"])
    common_layouts: List[str] = field(default_factory=list)
    signature_elements: List[str] = field(default_factory=list)

    def add_style(self, style: DesignStyle):
        self.styles.append(style)

    def get_favorite_style(self) -> Optional[DesignStyle]:
        return self.styles[0] if self.styles else None
