from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

from core.canvas import Canvas
from core.elements import TextElement, ImageElement, ShapeElement, Box
from core.styles import DesignStyle


_TEMPLATE_REGISTRY: Dict[str, type] = {}


def register_template(name: str):
    def decorator(cls):
        _TEMPLATE_REGISTRY[name] = cls
        cls.template_name = name
        return cls
    return decorator


def get_template(name: str):
    if name in _TEMPLATE_REGISTRY:
        return _TEMPLATE_REGISTRY[name]
    raise ValueError(f"Unknown template: {name}. Available: {list(_TEMPLATE_REGISTRY.keys())}")


def list_templates():
    return list(_TEMPLATE_REGISTRY.keys())


class Template(ABC):
    template_name: str = "base"

    def __init__(self, platform: str = "instagram_square"):
        self.platform = platform
        self.canvas = None
        self.style = None
        self.content: Dict[str, Any] = {}

    def setup(self, style: DesignStyle, content: Dict[str, Any]):
        self.style = style
        self.content = content
        size = Canvas.CANVAS_SIZES.get(self.platform, (1080, 1080))
        bg = style.palette.colors[0] if style.palette.colors else (255, 255, 255)
        self.canvas = Canvas(width=size[0], height=size[1], bg_color=bg)
        return self

    @abstractmethod
    def compose(self):
        pass

    def render(self):
        if not self.canvas:
            raise RuntimeError("Call setup() first")
        self.compose()
        if self.style.effects.gradient_overlay:
            colors = self.style.effects.gradient_colors or [self.style.palette.colors[0], self.style.palette.colors[-1]]
            self.canvas.apply_gradient_overlay(colors, self.style.effects.overlay_opacity)
        return self.canvas.render()

    def save(self, path: str):
        self.render().save(path)
