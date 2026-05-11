from typing import Dict, Any, Optional, List, Tuple
from PIL import Image, ImageFilter
import os

from core.canvas import Canvas
from core.elements import TextElement, ImageElement, ShapeElement, Box
from core.styles import DesignStyle, TextStyle, TextAlignment, EffectStyle
from core.color import ColorPalette
from .base import Template, register_template


@register_template("instagram_square")
class InstagramSquareTemplate(Template):
    """Modern Instagram square post with title, optional image, and clean layout"""

    def __init__(self):
        super().__init__("instagram_square")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        bg_accent = s.palette.get_accent(1) if len(s.palette.colors) > 1 else s.palette.colors[0]
        bg_dark = s.palette.get_accent(-1) if len(s.palette.colors) > 2 else (0, 0, 0)

        accent_bar = ShapeElement(
            box=Box(x=0, y=0, width=w, height=h),
            shape_type="rectangle",
            color=(*bg_accent, 30),
            z_index=0,
        )
        c.add_element(accent_bar)

        deco_bar = ShapeElement(
            box=Box(x=60, y=0, width=6, height=h),
            shape_type="rectangle",
            color=(*bg_accent, 60),
            z_index=1,
        )
        c.add_element(deco_bar)

        title_text = ct.get("title", "Your Title Here")
        subtitle = ct.get("subtitle", "")
        body = ct.get("body", "")

        title_elem = TextElement(
            text=title_text,
            style=s.title_style,
            box=Box(x=80, y=120, width=w - 160, height=200),
            z_index=3,
        )
        c.add_element(title_elem)

        if subtitle:
            sub_elem = TextElement(
                text=subtitle,
                style=s.subtitle_style,
                box=Box(x=80, y=340, width=w - 160, height=80),
                z_index=2,
            )
            c.add_element(sub_elem)

        if body:
            body_elem = TextElement(
                text=body,
                style=s.body_style,
                box=Box(x=80, y=440, width=w - 160, height=200),
                z_index=2,
            )
            c.add_element(body_elem)

        bg_image_path = ct.get("background_image")
        if bg_image_path and os.path.exists(bg_image_path):
            bg_img = ImageElement(
                source=bg_image_path,
                box=Box(x=0, y=0, width=w, height=h),
                fit="cover",
                opacity=0.4,
                z_index=-1,
            )
            c.add_element(bg_img)

        overlay_color = s.palette.get_accent(0)
        overlay = ShapeElement(
            box=Box(x=0, y=0, width=w, height=h),
            shape_type="rectangle",
            color=(*overlay_color, 180),
            z_index=-1,
        )
        c.add_element(overlay)


@register_template("instagram_story")
class InstagramStoryTemplate(Template):
    """Full-vertical Instagram story with bold center typography"""

    def __init__(self):
        super().__init__("instagram_story")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        bg_image_path = ct.get("background_image")
        if bg_image_path and os.path.exists(bg_image_path):
            bg_img = ImageElement(
                source=bg_image_path,
                box=Box(x=0, y=-100, width=w, height=h + 200),
                fit="cover",
                opacity=0.35,
                z_index=-1,
            )
            c.add_element(bg_img)

        overlay_grad = ShapeElement(
            box=Box(x=0, y=0, width=w, height=h),
            shape_type="rectangle",
            color=(*s.palette.colors[0], 200),
            z_index=0,
        )
        c.add_element(overlay_grad)

        title = ct.get("title", "")
        title_style = TextStyle(
            font_size=72,
            font_weight="bold",
            color=s.palette.get_text_color(0),
            alignment=TextAlignment.CENTER,
            shadow={"offset_x": 0, "offset_y": 4, "color": (0, 0, 0, 80)},
        )
        title_elem = TextElement(
            text=title,
            style=title_style,
            box=Box(x=60, y=300, width=w - 120, height=300),
            z_index=3,
        )
        c.add_element(title_elem)

        subtitle = ct.get("subtitle", "")
        sub_style = TextStyle(
            font_size=36,
            font_weight="normal",
            color=s.palette.get_text_color(0),
            alignment=TextAlignment.CENTER,
        )
        sub_elem = TextElement(
            text=subtitle,
            style=sub_style,
            box=Box(x=80, y=620, width=w - 160, height=100),
            z_index=3,
        )
        c.add_element(sub_elem)

        accent_bar = ShapeElement(
            box=Box(x=w // 2 - 40, y=560, width=80, height=4),
            shape_type="rounded_rectangle",
            color=(*s.palette.get_accent(1), 255),
            corner_radius=2,
            z_index=2,
        )
        c.add_element(accent_bar)


@register_template("twitter_post")
class TwitterPostTemplate(Template):
    """Clean Twitter/X card with image and text"""

    def __init__(self):
        super().__init__("twitter_post")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        accent = s.palette.get_accent(1)

        title = ct.get("title", "")
        subtitle = ct.get("subtitle", "")

        title_elem = TextElement(
            text=title,
            style=s.title_style,
            box=Box(x=60, y=100, width=w - 120, height=180),
            z_index=2,
        )
        c.add_element(title_elem)

        if subtitle:
            sub_elem = TextElement(
                text=subtitle,
                style=s.subtitle_style,
                box=Box(x=60, y=300, width=w - 120, height=80),
                z_index=2,
            )
            c.add_element(sub_elem)

        bottom_accent = ShapeElement(
            box=Box(x=0, y=h - 6, width=w, height=6),
            shape_type="rectangle",
            color=(*accent, 255),
            z_index=3,
        )
        c.add_element(bottom_accent)


@register_template("youtube_thumbnail")
class YouTubeThumbnailTemplate(Template):
    """High-impact YouTube thumbnail with bold text and image"""

    def __init__(self):
        super().__init__("youtube_thumbnail")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        if ct.get("background_image"):
            bg = ImageElement(
                source=ct["background_image"],
                box=Box(x=0, y=0, width=w, height=h),
                fit="cover",
                opacity=0.5,
                z_index=0,
            )
            c.add_element(bg)

        dark_overlay = ShapeElement(
            box=Box(x=0, y=0, width=w, height=h),
            shape_type="rectangle",
            color=(*s.palette.colors[0], 200),
            z_index=1,
        )
        c.add_element(dark_overlay)

        title = ct.get("title", "")
        title_style = TextStyle(
            font_size=64,
            font_weight="bold",
            color=s.palette.get_text_color(0),
            alignment=TextAlignment.LEFT,
        )
        title_elem = TextElement(
            text=title,
            style=title_style,
            box=Box(x=60, y=80, width=w - 200, height=300),
            z_index=3,
        )
        c.add_element(title_elem)

        subtitle = ct.get("subtitle", "")
        if subtitle:
            sub_style = TextStyle(
                font_size=32,
                font_weight="medium",
                color=s.palette.get_accent(1),
                alignment=TextAlignment.LEFT,
            )
            sub_elem = TextElement(
                text=subtitle,
                style=sub_style,
                box=Box(x=60, y=400, width=w - 200, height=80),
                z_index=3,
            )
            c.add_element(sub_elem)

        cta_bg = ShapeElement(
            box=Box(x=w - 220, y=h - 120, width=180, height=60),
            shape_type="rounded_rectangle",
            color=(*s.palette.get_accent(1), 255),
            corner_radius=8,
            z_index=4,
        )
        c.add_element(cta_bg)

        cta_text = ct.get("cta", "WATCH")
        cta_style = TextStyle(
            font_size=28,
            font_weight="bold",
            color=s.palette.get_text_color(1),
            alignment=TextAlignment.CENTER,
        )
        cta_elem = TextElement(
            text=cta_text,
            style=cta_style,
            box=Box(x=w - 220, y=h - 120, width=180, height=60),
            z_index=5,
        )
        c.add_element(cta_elem)


@register_template("quote_card")
class QuoteCardTemplate(Template):
    """Aesthetic quote card — popular on Pinterest/Instagram"""

    def __init__(self):
        super().__init__("instagram_square")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        accent1 = s.palette.get_accent(0)
        accent2 = s.palette.get_accent(2) if len(s.palette.colors) > 2 else s.palette.get_accent(1)

        frame = ShapeElement(
            box=Box(x=30, y=30, width=w - 60, height=h - 60),
            shape_type="rounded_rectangle",
            color=(*accent2, 20),
            border_color=(*accent1, 60),
            border_width=1,
            corner_radius=20,
            z_index=1,
        )
        c.add_element(frame)

        quote = ct.get("quote", "")
        author = ct.get("author", "")

        quote_style = TextStyle(
            font_size=36,
            font_weight="medium",
            color=s.palette.get_text_color(0),
            alignment=TextAlignment.CENTER,
            line_spacing=1.5,
        )
        quote_elem = TextElement(
            text=quote,
            style=quote_style,
            box=Box(x=80, y=180, width=w - 160, height=500),
            z_index=3,
        )
        c.add_element(quote_elem)

        if author:
            line_divider = ShapeElement(
                box=Box(x=w // 2 - 30, y=700, width=60, height=2),
                shape_type="rectangle",
                color=(*accent1, 200),
                z_index=2,
            )
            c.add_element(line_divider)

            author_style = TextStyle(
                font_size=24,
                font_weight="normal",
                color=(*accent1, 255),
                alignment=TextAlignment.CENTER,
            )
            author_elem = TextElement(
                text=f"— {author}",
                style=author_style,
                box=Box(x=80, y=720, width=w - 160, height=50),
                z_index=3,
            )
            c.add_element(author_elem)


@register_template("pinterest")
class PinterestTemplate(Template):
    """Tall Pinterest-optimized pin with bold vertical layout"""

    def __init__(self):
        super().__init__("pinterest")

    def compose(self):
        c = self.canvas
        s = self.style
        ct = self.content
        w, h = c.width, c.height

        if ct.get("background_image"):
            bg = ImageElement(
                source=ct["background_image"],
                box=Box(x=0, y=0, width=w, height=int(h * 0.6)),
                fit="cover",
                opacity=0.6,
                z_index=0,
            )
            c.add_element(bg)

        dark_bottom = ShapeElement(
            box=Box(x=0, y=int(h * 0.55), width=w, height=int(h * 0.45)),
            shape_type="rectangle",
            color=(*s.palette.colors[0], 230),
            z_index=1,
        )
        c.add_element(dark_bottom)

        title = ct.get("title", "")
        title_style = TextStyle(
            font_size=48,
            font_weight="bold",
            color=s.palette.get_text_color(0),
            alignment=TextAlignment.CENTER,
            shadow={"offset_x": 0, "offset_y": 2, "color": (0, 0, 0, 60)},
        )
        title_elem = TextElement(
            text=title,
            style=title_style,
            box=Box(x=50, y=int(h * 0.6), width=w - 100, height=200),
            z_index=3,
        )
        c.add_element(title_elem)

        desc = ct.get("description", "")
        if desc:
            desc_style = TextStyle(
                font_size=24,
                font_weight="normal",
                color=s.palette.get_text_color(0),
                alignment=TextAlignment.CENTER,
            )
            desc_elem = TextElement(
                text=desc,
                style=desc_style,
                box=Box(x=60, y=int(h * 0.6) + 220, width=w - 120, height=200),
                z_index=3,
            )
            c.add_element(desc_elem)
