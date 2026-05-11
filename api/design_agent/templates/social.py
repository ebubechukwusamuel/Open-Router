"""Premium social media templates with creative, non-generic designs."""
import math
import random
from typing import Dict, Any, Optional, List, Tuple
from PIL import Image, ImageFilter
import os

from core.canvas import Canvas
from core.elements import TextElement, ImageElement, ShapeElement, Box
from core.styles import DesignStyle, TextStyle, TextAlignment, EffectStyle
from core.color import ColorPalette
from .base import Template, register_template


def _soft_color(c: Tuple[int, int, int], factor: float = 0.3) -> Tuple[int, int, int]:
    return (min(255, int(c[0] + (255 - c[0]) * factor)),
            min(255, int(c[1] + (255 - c[1]) * factor)),
            min(255, int(c[2] + (255 - c[2]) * factor)))


def _darken(c: Tuple[int, int, int], factor: float = 0.3) -> Tuple[int, int, int]:
    return (int(c[0] * (1 - factor)), int(c[1] * (1 - factor)), int(c[2] * (1 - factor)))


def _lerp_color(a: Tuple[int, int, int], b: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    return (int(a[0] + (b[0] - a[0]) * t),
            int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t))


_POP_FONTS = [
    "Montserrat", "Poppins", "Playfair Display", "Inter",
    "Roboto", "Raleway", "Merriweather", "Lato",
    "Oswald", "Open Sans", "Nunito", "Dancing Script",
]


def _pick_font(weight: str = "bold") -> str:
    bold_fonts = ["Montserrat", "Poppins", "Inter", "Oswald", "Raleway"]
    elegant_fonts = ["Playfair Display", "Merriweather", "Lato", "Nunito"]
    return random.choice(bold_fonts if weight == "bold" else elegant_fonts)


@register_template("instagram_square")
class InstagramSquareTemplate(Template):
    """Bento-grid inspired Instagram square with asymmetric layout."""

    def __init__(self):
        super().__init__("instagram_square")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        palette = s.palette.colors
        c1, c2, c3, c4, c5 = palette[0], palette[1 % len(palette)], palette[2 % len(palette)], palette[3 % len(palette)], palette[4 % len(palette)]
        tc = s.palette.get_text_color(0)
        accent = s.palette.get_accent(1)

        # Background with soft gradient blocks
        bg_layer = ShapeElement(box=Box(x=0, y=0, width=w, height=h), shape_type="rectangle",
                                color=(*c1, 255), z_index=0)
        c.add_element(bg_layer)

        # Large decorative circle top-right
        c.add_element(ShapeElement(box=Box(x=int(w * 0.55), y=-120, width=600, height=600),
                                   shape_type="circle", color=(*c2, 50), z_index=0))

        # Smaller circle bottom-left
        c.add_element(ShapeElement(box=Box(x=-80, y=int(h * 0.6), width=350, height=350),
                                   shape_type="circle", color=(*c3, 60), z_index=0))

        # Bento accent block — colored rectangle bottom-right corner
        c.add_element(ShapeElement(box=Box(x=int(w * 0.6), y=int(h * 0.7), width=int(w * 0.35), height=int(h * 0.25)),
                                   shape_type="rounded_rectangle", color=(*accent, 180),
                                   corner_radius=24, z_index=1))

        # Thin horizontal line accent
        c.add_element(ShapeElement(box=Box(x=60, y=200, width=120, height=3),
                                   shape_type="rectangle", color=(*accent, 180), z_index=2))

        # Title — large, bold, left-aligned
        title = ct.get("title", "Your Title")
        title_font = _pick_font("bold")
        title_elem = TextElement(
            text=title,
            style=TextStyle(font_family=title_font, font_size=64, font_weight="bold", color=tc,
                           alignment=TextAlignment.LEFT),
            box=Box(x=60, y=220, width=int(w * 0.55), height=200), z_index=3)
        c.add_element(title_elem)

        # Subtitle
        subtitle = ct.get("subtitle", "")
        if subtitle:
            c.add_element(TextElement(
                text=subtitle,
                style=TextStyle(font_family=_pick_font("normal"), font_size=28, font_weight="normal",
                               color=_soft_color(tc, 0.3), alignment=TextAlignment.LEFT),
                box=Box(x=60, y=430, width=int(w * 0.5), height=60), z_index=3))

        # Body text — smaller, in the lower-left area
        body = ct.get("body", "")
        if body:
            c.add_element(TextElement(
                text=body,
                style=TextStyle(font_family=_pick_font("normal"), font_size=22, font_weight="normal",
                               color=_soft_color(tc, 0.4), alignment=TextAlignment.LEFT, line_spacing=1.6),
                box=Box(x=60, y=500, width=int(w * 0.5), height=200), z_index=3))

        # Background image treatment (optional)
        bg_image_path = ct.get("background_image")
        if bg_image_path and os.path.exists(bg_image_path):
            c.add_element(ImageElement(source=bg_image_path, box=Box(x=0, y=0, width=w, height=h),
                                       fit="cover", opacity=0.25, z_index=-1))

        # Decorative dot: small circle as an accent
        c.add_element(ShapeElement(box=Box(x=60, y=180, width=10, height=10),
                                   shape_type="circle", color=(*accent, 220), z_index=2))

        # Bottom decorative bar
        c.add_element(ShapeElement(box=Box(x=0, y=h - 6, width=w, height=6),
                                   shape_type="rectangle", color=(*accent, 200), z_index=4))


@register_template("instagram_story")
class InstagramStoryTemplate(Template):
    """Full-vertical story with cinematic typography and atmospheric geometry."""

    def __init__(self):
        super().__init__("instagram_story")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        palette = s.palette.colors
        core = palette[0]
        accent = s.palette.get_accent(1)
        tc = s.palette.get_text_color(0)

        # Background image
        bg_image_path = ct.get("background_image")
        if bg_image_path and os.path.exists(bg_image_path):
            c.add_element(ImageElement(source=bg_image_path, box=Box(x=-50, y=-50, width=w + 100, height=h + 100),
                                       fit="cover", opacity=0.3, z_index=-1))

        # Full background color
        c.add_element(ShapeElement(box=Box(x=0, y=0, width=w, height=h),
                                   shape_type="rectangle", color=(*core, 220), z_index=0))

        # Large atmospheric circle behind text
        c.add_element(ShapeElement(box=Box(x=w // 2 - 250, y=200, width=500, height=500),
                                   shape_type="circle", color=(*accent, 30), z_index=1))

        # Decorative diagonal band using rotated rect (simulated with offset)
        band_y = int(h * 0.35)
        c.add_element(ShapeElement(box=Box(x=-100, y=band_y, width=w + 200, height=8),
                                   shape_type="rectangle", color=(*accent, 80), z_index=2))

        # Giant outline text as background element
        title = ct.get("title", "")
        if title:
            # Large faded text behind
            c.add_element(TextElement(
                text=title.upper(),
                style=TextStyle(font_family=_pick_font("bold"), font_size=180, font_weight="bold",
                               color=(*tc, 30), alignment=TextAlignment.CENTER,
                               letter_spacing=8),
                box=Box(x=40, y=250, width=w - 80, height=400), z_index=1))

            # Main title in foreground
            c.add_element(TextElement(
                text=title,
                style=TextStyle(font_family=_pick_font("bold"), font_size=72, font_weight="bold",
                               color=tc, alignment=TextAlignment.CENTER,
                               shadow={"offset_x": 0, "offset_y": 6, "color": (0, 0, 0, 100)}),
                box=Box(x=60, y=480, width=w - 120, height=250), z_index=3))

        # Subtitle
        subtitle = ct.get("subtitle", "")
        if subtitle:
            c.add_element(TextElement(
                text=subtitle,
                style=TextStyle(font_family=_pick_font("normal"), font_size=32, font_weight="normal",
                               color=(*tc, 220), alignment=TextAlignment.CENTER, letter_spacing=2),
                box=Box(x=80, y=720, width=w - 160, height=80), z_index=3))

        # Decorative small dots
        for i in range(3):
            c.add_element(ShapeElement(
                box=Box(x=w // 2 - 30 + i * 30, y=840, width=6, height=6),
                shape_type="circle", color=(*accent, 180), z_index=2))

        # Bottom gradient overlay
        c.add_element(ShapeElement(
            box=Box(x=0, y=int(h * 0.8), width=w, height=int(h * 0.2)),
            shape_type="rectangle", color=(*core, 0), z_index=2))


@register_template("twitter_post")
class TwitterPostTemplate(Template):
    """Asymmetric split-layout Twitter card with bold composition."""

    def __init__(self):
        super().__init__("twitter_post")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        palette = s.palette.colors
        c1, c2 = palette[0], palette[1 % len(palette)]
        accent = s.palette.get_accent(2) if len(palette) > 2 else palette[1 % len(palette)]
        tc = s.palette.get_text_color(0)

        # Split background: left portion colored, right portion light
        split_x = int(w * 0.45)
        c.add_element(ShapeElement(box=Box(x=0, y=0, width=split_x, height=h),
                                   shape_type="rectangle", color=(*c1, 255), z_index=0))
        c.add_element(ShapeElement(box=Box(x=split_x, y=0, width=w - split_x, height=h),
                                   shape_type="rectangle", color=(*_soft_color(c2, 0.6), 255), z_index=0))

        # Diagonal connecting accent (angled rectangle)
        c.add_element(ShapeElement(box=Box(x=split_x - 60, y=-50, width=80, height=h + 100),
                                   shape_type="rectangle", color=(*accent, 60), z_index=1))

        # Decorative circle on right side
        c.add_element(ShapeElement(box=Box(x=int(w * 0.6), y=80, width=300, height=300),
                                   shape_type="circle", color=(*accent, 30), z_index=1))

        # Title in left panel
        title = ct.get("title", "")
        body = ct.get("body", "")
        c.add_element(TextElement(
            text=title,
            style=TextStyle(font_family=_pick_font("bold"), font_size=44, font_weight="bold",
                           color=tc, alignment=TextAlignment.LEFT, line_spacing=1.3),
            box=Box(x=50, y=80, width=split_x - 80, height=260), z_index=3))

        # Body in left panel below title
        if body:
            c.add_element(TextElement(
                text=body,
                style=TextStyle(font_family=_pick_font("normal"), font_size=22, font_weight="normal",
                               color=_soft_color(tc, 0.3), alignment=TextAlignment.LEFT, line_spacing=1.5),
                box=Box(x=50, y=340, width=split_x - 80, height=200), z_index=3))

        # Right panel: large accent number or letter
        subtitle = ct.get("subtitle", "")
        display_text = subtitle[:3].upper() if subtitle else "—"
        c.add_element(TextElement(
            text=display_text,
            style=TextStyle(font_family=_pick_font("bold"), font_size=120, font_weight="bold",
                           color=(*accent, 50), alignment=TextAlignment.CENTER),
            box=Box(x=split_x, y=100, width=w - split_x, height=300), z_index=2))

        # Small accent dots on right
        for i in range(5):
            y_pos = 440 + i * 30
            c.add_element(ShapeElement(
                box=Box(x=split_x + 80, y=y_pos, width=4, height=4),
                shape_type="circle", color=(*accent, 120 - i * 15), z_index=2))

        # Bottom border accent
        c.add_element(ShapeElement(box=Box(x=30, y=h - 30, width=w - 60, height=2),
                                   shape_type="rectangle", color=(*accent, 100), z_index=4))


@register_template("youtube_thumbnail")
class YouTubeThumbnailTemplate(Template):
    """High-impact YouTube thumbnail with layered depth and bold typography."""

    def __init__(self):
        super().__init__("youtube_thumbnail")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        palette = s.palette.colors
        core = palette[0]
        accent = s.palette.get_accent(1)
        accent2 = s.palette.get_accent(2) if len(palette) > 2 else _lerp_color(accent, (0,0,0), 0.3)
        tc = s.palette.get_text_color(0)

        # Background image or dark base
        bg_image_path = ct.get("background_image")
        if bg_image_path and os.path.exists(bg_image_path):
            c.add_element(ImageElement(source=bg_image_path, box=Box(x=0, y=0, width=w, height=h),
                                       fit="cover", opacity=0.6, z_index=-1))

        # Dark gradient base
        c.add_element(ShapeElement(box=Box(x=0, y=0, width=w, height=h),
                                   shape_type="rectangle", color=(*core, 200), z_index=0))

        # Diagonal accent bar top-left
        c.add_element(ShapeElement(box=Box(x=0, y=0, width=int(w * 0.6), height=h),
                                   shape_type="rectangle", color=(*accent, 60), z_index=0))

        # Bottom accent shape
        c.add_element(ShapeElement(box=Box(x=0, y=int(h * 0.7), width=w, height=int(h * 0.3)),
                                   shape_type="rectangle", color=(*_darken(core, 0.5), 200), z_index=1))

        # Decorative large circle on right
        c.add_element(ShapeElement(box=Box(x=int(w * 0.55), y=-100, width=500, height=500),
                                   shape_type="circle", color=(*accent, 40), z_index=1))

        # Main title with outline + shadow
        title_text = ct.get("title", "")
        c.add_element(TextElement(
            text=title_text,
            style=TextStyle(font_family=_pick_font("bold"), font_size=68, font_weight="bold",
                           color=(255, 255, 255), alignment=TextAlignment.LEFT,
                           outline={"color": (0, 0, 0, 200), "width": 3},
                           shadow={"offset_x": 4, "offset_y": 4, "color": (0, 0, 0, 180)}),
            box=Box(x=60, y=120, width=int(w * 0.6), height=280), z_index=3))

        # Subtitle line
        subtitle = ct.get("subtitle", "")
        if subtitle:
            c.add_element(TextElement(
                text=subtitle,
                style=TextStyle(font_family=_pick_font("normal"), font_size=32, font_weight="medium",
                               color=(*accent, 255), alignment=TextAlignment.LEFT),
                box=Box(x=60, y=410, width=int(w * 0.55), height=60), z_index=3))

        # CTA button shape
        cta_text = ct.get("cta", "▶ WATCH")
        btn_w, btn_h = 220, 65
        btn_x = w - btn_w - 50
        btn_y = h - btn_h - 50
        c.add_element(ShapeElement(
            box=Box(x=btn_x, y=btn_y, width=btn_w, height=btn_h),
            shape_type="rounded_rectangle",
            color=(*accent, 240), corner_radius=12, z_index=4))

        # CTA button inner accent (subtle shine line)
        c.add_element(ShapeElement(
            box=Box(x=btn_x + 20, y=btn_y + 10, width=btn_w - 40, height=2),
            shape_type="rectangle", color=(*_soft_color(accent, 0.7), 100), z_index=5))

        # CTA text
        c.add_element(TextElement(
            text=cta_text,
            style=TextStyle(font_family=_pick_font("bold"), font_size=28, font_weight="bold",
                           color=(255, 255, 255), alignment=TextAlignment.CENTER),
            box=Box(x=btn_x, y=btn_y, width=btn_w, height=btn_h), z_index=5))

        # Top accent line
        c.add_element(ShapeElement(box=Box(x=60, y=60, width=100, height=4),
                                   shape_type="rectangle", color=(*accent, 200), z_index=3))


@register_template("quote_card")
class QuoteCardTemplate(Template):
    """Elegant quote card with decorative typography and soft geometry."""

    def __init__(self):
        super().__init__("instagram_square")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        palette = s.palette.colors
        c1, c2 = palette[0], palette[1 % len(palette)]
        accent = s.palette.get_accent(2) if len(palette) > 2 else palette[1 % len(palette)]
        tc = s.palette.get_text_color(0)
        accent_tc = s.palette.get_text_color(2) if len(palette) > 2 else (255, 255, 255)

        # Background
        c.add_element(ShapeElement(box=Box(x=0, y=0, width=w, height=h),
                                   shape_type="rectangle", color=(*c1, 255), z_index=0))

        # Soft inner background — creates a card feel
        margin = 50
        c.add_element(ShapeElement(
            box=Box(x=margin, y=margin, width=w - 2 * margin, height=h - 2 * margin),
            shape_type="rounded_rectangle", color=(*_soft_color(c1, 0.2), 40),
            corner_radius=24, border_color=(*accent, 60), border_width=1, z_index=1))

        # Decorative circles in corners
        c.add_element(ShapeElement(box=Box(x=-80, y=-80, width=200, height=200),
                                   shape_type="circle", color=(*accent, 25), z_index=0))
        c.add_element(ShapeElement(box=Box(x=w - 120, y=h - 120, width=200, height=200),
                                   shape_type="circle", color=(*accent, 25), z_index=0))

        # Large decorative opening quote mark
        quote = ct.get("quote", "")
        if quote:
            c.add_element(TextElement(
                text="\"",
                style=TextStyle(font_family="Playfair Display", font_size=200, font_weight="bold",
                               color=(*accent, 60), alignment=TextAlignment.LEFT),
                box=Box(x=100, y=80, width=160, height=180), z_index=2))

            # Quote text
            c.add_element(TextElement(
                text=quote,
                style=TextStyle(font_family="Playfair Display", font_size=38, font_weight="medium",
                               color=tc, alignment=TextAlignment.CENTER, line_spacing=1.6),
                box=Box(x=100, y=250, width=w - 200, height=400), z_index=3))

        # Decorative divider
        divider_y = 680
        c.add_element(ShapeElement(box=Box(x=w // 2 - 80, y=divider_y, width=160, height=1),
                                   shape_type="rectangle", color=(*accent, 120), z_index=2))
        c.add_element(ShapeElement(box=Box(x=w // 2 - 25, y=divider_y - 4, width=50, height=9),
                                   shape_type="rounded_rectangle", color=(*accent, 180),
                                   corner_radius=4, z_index=2))

        # Author
        author = ct.get("author", "")
        if author:
            c.add_element(TextElement(
                text=f"— {author}",
                style=TextStyle(font_family=_pick_font("normal"), font_size=26, font_weight="normal",
                               color=(*accent, 220), alignment=TextAlignment.CENTER, letter_spacing=1),
                box=Box(x=100, y=720, width=w - 200, height=60), z_index=3))


@register_template("pinterest")
class PinterestTemplate(Template):
    """Tall Pinterest pin with layered imagery and sophisticated composition."""

    def __init__(self):
        super().__init__("pinterest")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        palette = s.palette.colors
        c1 = palette[0]
        accent = s.palette.get_accent(1)
        accent2 = s.palette.get_accent(2) if len(palette) > 2 else s.palette.get_accent(1)
        tc = s.palette.get_text_color(0)

        # Full background
        c.add_element(ShapeElement(box=Box(x=0, y=0, width=w, height=h),
                                   shape_type="rectangle", color=(*c1, 255), z_index=0))

        # Top image area (0-60%)
        img_h = int(h * 0.58)
        bg_image_path = ct.get("background_image")
        if bg_image_path and os.path.exists(bg_image_path):
            c.add_element(ImageElement(
                source=bg_image_path, box=Box(x=0, y=0, width=w, height=img_h),
                fit="cover", opacity=0.85, z_index=0))

        # Gradient transition overlay between image and text
        c.add_element(ShapeElement(
            box=Box(x=0, y=img_h - 80, width=w, height=80),
            shape_type="rectangle", color=(*c1, 0), z_index=1))

        # Decorative shape overlapping image area
        c.add_element(ShapeElement(
            box=Box(x=-40, y=img_h - 60, width=250, height=120),
            shape_type="rounded_rectangle", color=(*accent, 160),
            corner_radius=20, z_index=2))

        # Decorative dots grid in lower area
        for row in range(6):
            for col in range(4):
                dx = 80 + col * 60
                dy = int(h * 0.78) + row * 25
                c.add_element(ShapeElement(
                    box=Box(x=dx, y=dy, width=3, height=3),
                    shape_type="circle", color=(*accent, 30 + row * 5), z_index=1))

        # Title
        title = ct.get("title", "")
        c.add_element(TextElement(
            text=title,
            style=TextStyle(font_family=_pick_font("bold"), font_size=46, font_weight="bold",
                           color=tc, alignment=TextAlignment.LEFT,
                           shadow={"offset_x": 0, "offset_y": 2, "color": (0, 0, 0, 50)}),
            box=Box(x=50, y=img_h + 20, width=w - 100, height=140), z_index=3))

        # Description
        desc = ct.get("description", "")
        if desc:
            c.add_element(TextElement(
                text=desc,
                style=TextStyle(font_family=_pick_font("normal"), font_size=24, font_weight="normal",
                               color=_soft_color(tc, 0.3), alignment=TextAlignment.LEFT, line_spacing=1.5),
                box=Box(x=50, y=img_h + 160, width=w - 100, height=180), z_index=3))

        # Small accent label / category tag
        subtitle = ct.get("subtitle", "")
        if subtitle:
            tag_text = subtitle.upper()[:20]
            tag_w = 180
            c.add_element(ShapeElement(
                box=Box(x=50, y=img_h - 50, width=tag_w, height=36),
                shape_type="rounded_rectangle", color=(*_darken(c1, 0.5), 180),
                corner_radius=18, z_index=3))
            c.add_element(TextElement(
                text=tag_text,
                style=TextStyle(font_family=_pick_font("normal"), font_size=18, font_weight="medium",
                               color=(*accent, 230), alignment=TextAlignment.CENTER, letter_spacing=1),
                box=Box(x=50, y=img_h - 50, width=tag_w, height=36), z_index=4))

        # Bottom accent bar
        c.add_element(ShapeElement(box=Box(x=50, y=h - 30, width=w - 100, height=2),
                                   shape_type="rectangle", color=(*accent, 100), z_index=4))


@register_template("facebook_post")
class FacebookPostTemplate(Template):
    """Clean Facebook post with engaging visual hierarchy."""

    def __init__(self):
        super().__init__("facebook_post")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        palette = s.palette.colors
        c1 = palette[0]
        accent = s.palette.get_accent(1)
        tc = s.palette.get_text_color(0)

        # Background
        c.add_element(ShapeElement(box=Box(x=0, y=0, width=w, height=h),
                                   shape_type="rectangle", color=(*c1, 255), z_index=0))

        # Top accent band
        c.add_element(ShapeElement(box=Box(x=0, y=0, width=w, height=8),
                                   shape_type="rectangle", color=(*accent, 200), z_index=1))

        # Decorative vertical bar left
        c.add_element(ShapeElement(box=Box(x=60, y=80, width=4, height=200),
                                   shape_type="rectangle", color=(*accent, 100), z_index=1))

        # Title
        title = ct.get("title", "")
        c.add_element(TextElement(
            text=title,
            style=TextStyle(font_family=_pick_font("bold"), font_size=52, font_weight="bold",
                           color=tc, alignment=TextAlignment.LEFT, line_spacing=1.3),
            box=Box(x=90, y=100, width=w - 160, height=200), z_index=3))

        # Body
        body = ct.get("body", "")
        if body:
            c.add_element(TextElement(
                text=body,
                style=TextStyle(font_family=_pick_font("normal"), font_size=24, font_weight="normal",
                               color=_soft_color(tc, 0.35), alignment=TextAlignment.LEFT, line_spacing=1.5),
                box=Box(x=90, y=320, width=w - 160, height=200), z_index=3))

        # Bottom-right decorative circle
        c.add_element(ShapeElement(box=Box(x=w - 180, y=h - 180, width=250, height=250),
                                   shape_type="circle", color=(*accent, 25), z_index=0))

        # CTA / subtitle at bottom
        subtitle = ct.get("subtitle", "")
        if subtitle:
            c.add_element(TextElement(
                text=subtitle,
                style=TextStyle(font_family=_pick_font("bold"), font_size=22, font_weight="bold",
                               color=(*accent, 220), alignment=TextAlignment.LEFT, letter_spacing=1),
                box=Box(x=90, y=540, width=w - 160, height=50), z_index=3))

        # Bottom accent
        c.add_element(ShapeElement(box=Box(x=90, y=h - 40, width=80, height=3),
                                   shape_type="rectangle", color=(*accent, 150), z_index=4))
