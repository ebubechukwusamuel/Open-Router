from typing import List, Tuple, Optional, Dict, Any, Callable
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import math
import os
from .elements import (
    DesignElement, TextElement, ImageElement, ShapeElement,
    Box, ElementType, TextAlignment
)
from .styles import DesignStyle, TextAlignment as TA, EffectStyle


class Canvas:
    CANVAS_SIZES = {
        "instagram_square": (1080, 1080),
        "instagram_portrait": (1080, 1350),
        "instagram_story": (1080, 1920),
        "twitter_post": (1200, 675),
        "twitter_header": (1500, 500),
        "facebook_post": (1200, 630),
        "linkedin_post": (1200, 627),
        "youtube_thumbnail": (1280, 720),
        "pinterest": (1000, 1500),
        "custom": (1080, 1080),
    }

    def __init__(self, width: int = 1080, height: int = 1080, bg_color: Tuple[int, int, int] = (255, 255, 255)):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.image = Image.new("RGBA", (width, height), (*bg_color, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.elements: List[DesignElement] = []
        self._fonts_cache: Dict[str, ImageFont.FreeTypeFont] = {}

    @classmethod
    def for_platform(cls, platform: str, bg_color: Tuple[int, int, int] = (255, 255, 255)) -> "Canvas":
        size = cls.CANVAS_SIZES.get(platform)
        if not size:
            raise ValueError(f"Unknown platform: {platform}. Options: {list(cls.CANVAS_SIZES.keys())}")
        return cls(width=size[0], height=size[1], bg_color=bg_color)

    def add_element(self, element: DesignElement):
        element.z_index = len(self.elements)
        self.elements.append(element)

    def _resolve_font(self, font_family: str, font_size: int, font_weight: str = "normal") -> ImageFont.FreeTypeFont:
        cache_key = f"{font_family}_{font_size}_{font_weight}"
        if cache_key in self._fonts_cache:
            return self._fonts_cache[cache_key]

        if os.name == "nt":
            base_dirs = [
                os.environ.get("WINDIR", "C:\\Windows") + "\\Fonts",
                os.environ.get("LOCALAPPDATA", "") + "\\Microsoft\\Windows\\Fonts",
            ]
        else:
            base_dirs = ["/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.fonts")]

        weight_map = {
            "thin": "Thin", "light": "Light", "regular": "Regular",
            "normal": "Regular", "medium": "Medium",
            "semibold": "SemiBold", "bold": "Bold",
            "extrabold": "ExtraBold", "black": "Black",
        }
        weight_suffix = weight_map.get(font_weight.lower(), "Regular")

        font_path = None
        family_variants = [
            f"{font_family}-{weight_suffix}.ttf",
            f"{font_family}-{weight_suffix}.otf",
            f"{font_family} {weight_suffix}.ttf",
            f"{font_family}{weight_suffix}.ttf",
            f"{font_family}.ttf",
        ]
        if " " in font_family:
            family_variants.extend([
                font_family.replace(" ", "") + f"-{weight_suffix}.ttf",
                font_family.replace(" ", "") + f"-{weight_suffix}.otf",
            ])

        for base_dir in base_dirs:
            if not base_dir or not os.path.isdir(base_dir):
                continue
            for variant in family_variants:
                candidate = os.path.join(base_dir, variant)
                if os.path.exists(candidate):
                    font_path = candidate
                    break
            if font_path:
                break

        try:
            font = ImageFont.truetype(font_path or "arial.ttf", font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()
        self._fonts_cache[cache_key] = font
        return font

    def _draw_text(self, element: TextElement):
        font = self._resolve_font(element.style.font_family, element.style.font_size, element.style.font_weight)
        style = element.style
        text = element.text
        box = element.box

        lines = self._wrap_text(text, font, box.width or self.width)
        line_height = int(element.style.font_size * element.style.line_spacing)

        total_height = len(lines) * line_height
        start_y = box.y

        if style.alignment == TA.CENTER:
            start_y = box.y + (box.height - total_height) / 2 if box.height > total_height else box.y
        elif style.alignment == TA.LEFT:
            pass

        for i, line in enumerate(lines):
            lw = self.draw.textlength(line, font=font)
            if style.alignment == TA.CENTER:
                x = box.x + (box.width - lw) / 2
            elif style.alignment == TA.RIGHT:
                x = box.x + box.width - lw
            else:
                x = box.x

            if style.shadow:
                sx = x + style.shadow.get("offset_x", 2)
                sy = start_y + i * line_height + style.shadow.get("offset_y", 2)
                sc = style.shadow.get("color", (0, 0, 0, 128))
                self.draw.text((sx, sy), line, fill=sc, font=font)

            if style.outline:
                oc = style.outline.get("color", (0, 0, 0, 255))
                ow = style.outline.get("width", 2)
                for dx in (-ow, 0, ow):
                    for dy in (-ow, 0, ow):
                        if dx or dy:
                            self.draw.text((x + dx, start_y + i * line_height + dy), line, fill=oc, font=font)

            self.draw.text((x, start_y + i * line_height), line, fill=style.color, font=font)

    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: float) -> List[str]:
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            w = self.draw.textlength(test_line, font=font)
            if w <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines if lines else [text]

    def _draw_image(self, element: ImageElement):
        img = element.load()
        if img is None:
            return

        box = element.box
        img = img.convert("RGBA")

        if element.fit == "cover":
            img = self._cover_fit(img, int(box.width), int(box.height))
        elif element.fit == "contain":
            img = self._contain_fit(img, int(box.width), int(box.height))
        else:
            img = img.resize((int(box.width), int(box.height)))

        if element.opacity < 1.0:
            r, g, b, a = img.split()
            a = a.point(lambda x: int(x * element.opacity))
            img = Image.merge("RGBA", (r, g, b, a))

        if element.border_radius > 0:
            img = self._round_corners(img, element.border_radius)

        self.image.paste(img, (int(box.x), int(box.y)), img)

    def _cover_fit(self, img: Image.Image, target_w: int, target_h: int) -> Image.Image:
        iw, ih = img.size
        ratio = max(target_w / iw, target_h / ih)
        new_size = (int(iw * ratio), int(ih * ratio))
        img = img.resize(new_size, Image.LANCZOS)
        left = (new_size[0] - target_w) // 2
        top = (new_size[1] - target_h) // 2
        return img.crop((left, top, left + target_w, top + target_h))

    def _contain_fit(self, img: Image.Image, target_w: int, target_h: int) -> Image.Image:
        iw, ih = img.size
        ratio = min(target_w / iw, target_h / ih)
        new_size = (int(iw * ratio), int(ih * ratio))
        img = img.resize(new_size, Image.LANCZOS)
        result = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        left = (target_w - new_size[0]) // 2
        top = (target_h - new_size[1]) // 2
        result.paste(img, (left, top))
        return result

    def _round_corners(self, img: Image.Image, radius: int) -> Image.Image:
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
        result = img.copy()
        result.putalpha(mask)
        return result

    def _draw_shape(self, element: ShapeElement):
        box = element.box
        coords = [box.x, box.y, box.x + box.width, box.y + box.height]

        if element.shape_type == "circle":
            self.draw.ellipse(coords, fill=element.color, outline=element.border_color or None, width=element.border_width)
        elif element.shape_type == "rounded_rectangle":
            self.draw.rounded_rectangle(coords, radius=element.corner_radius, fill=element.color,
                                        outline=element.border_color or None, width=element.border_width)
        elif element.shape_type == "line":
            self.draw.line([(box.x, box.y), (box.x + box.width, box.y + box.height)],
                           fill=element.color, width=max(1, element.border_width))
        else:
            self.draw.rectangle(coords, fill=element.color, outline=element.border_color or None, width=element.border_width)

    def apply_gradient_overlay(self, colors: List[Tuple[int, int, int]], opacity: float = 0.3, direction: str = "vertical"):
        gradient = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(gradient)
        steps = len(colors)
        if direction == "vertical":
            block_h = self.height / (steps - 1) if steps > 1 else self.height
            for i in range(steps - 1):
                for y in range(int(i * block_h), int((i + 1) * block_h)):
                    ratio = (y - i * block_h) / block_h
                    r = int(colors[i][0] * (1 - ratio) + colors[i + 1][0] * ratio)
                    g = int(colors[i][1] * (1 - ratio) + colors[i + 1][1] * ratio)
                    b = int(colors[i][2] * (1 - ratio) + colors[i + 1][2] * ratio)
                    gdraw.line([(0, y), (self.width, y)], fill=(r, g, b, int(255 * opacity)))
        else:
            block_w = self.width / (steps - 1) if steps > 1 else self.width
            for i in range(steps - 1):
                for x in range(int(i * block_w), int((i + 1) * block_w)):
                    ratio = (x - i * block_w) / block_w
                    r = int(colors[i][0] * (1 - ratio) + colors[i + 1][0] * ratio)
                    g = int(colors[i][1] * (1 - ratio) + colors[i + 1][1] * ratio)
                    b = int(colors[i][2] * (1 - ratio) + colors[i + 1][2] * ratio)
                    gdraw.line([(x, 0), (x, self.height)], fill=(r, g, b, int(255 * opacity)))
        self.image = Image.alpha_composite(self.image, gradient)

    def render(self) -> Image.Image:
        self.elements.sort(key=lambda e: e.z_index)

        for element in self.elements:
            if not element.visible:
                continue
            if element.element_type == ElementType.TEXT:
                self._draw_text(element)
            elif element.element_type == ElementType.IMAGE:
                self._draw_image(element)
            elif element.element_type == ElementType.SHAPE:
                self._draw_shape(element)

        return self.image

    def save(self, path: str, format: Optional[str] = None):
        self.render().save(path, format=format or path.split(".")[-1].upper())

    def show(self):
        self.render().show()
