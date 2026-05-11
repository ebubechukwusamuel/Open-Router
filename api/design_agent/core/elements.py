from dataclasses import dataclass, field
from typing import Tuple, Optional, Dict, Any, Callable
from enum import Enum
from PIL import Image, ImageDraw, ImageFont
from .styles import TextStyle, TextAlignment


class ElementType(Enum):
    TEXT = "text"
    IMAGE = "image"
    SHAPE = "shape"
    GROUP = "group"


@dataclass
class Box:
    x: float = 0
    y: float = 0
    width: float = 0
    height: float = 0

    @property
    def center_x(self):
        return self.x + self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2

    def to_tuple(self) -> Tuple[float, float, float, float]:
        return (self.x, self.y, self.x + self.width, self.y + self.height)


@dataclass
class DesignElement:
    element_type: ElementType = ElementType.TEXT
    box: Box = field(default_factory=Box)
    z_index: int = 0
    opacity: float = 1.0
    rotation: float = 0.0
    visible: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_bounds(self) -> Tuple[float, float, float, float]:
        return self.box.to_tuple()

    def contains_point(self, px: float, py: float) -> bool:
        x1, y1, x2, y2 = self.get_bounds()
        return x1 <= px <= x2 and y1 <= py <= y2


@dataclass
class TextElement(DesignElement):
    text: str = ""
    style: TextStyle = field(default_factory=TextStyle)
    max_width: Optional[float] = None
    max_lines: int = 0

    def __post_init__(self):
        self.element_type = ElementType.TEXT


@dataclass
class ImageElement(DesignElement):
    source: str = ""
    image: Optional[Image.Image] = None
    fit: str = "cover"
    opacity: float = 1.0
    border_radius: int = 0

    def __post_init__(self):
        self.element_type = ElementType.IMAGE

    def load(self) -> Optional[Image.Image]:
        if self.source and not self.image:
            try:
                self.image = Image.open(self.source).convert("RGBA")
            except Exception:
                return None
        return self.image


@dataclass
class ShapeElement(DesignElement):
    shape_type: str = "rectangle"
    color: Tuple[int, int, int, int] = (255, 255, 255, 255)
    border_color: Optional[Tuple[int, int, int, int]] = None
    border_width: int = 0
    corner_radius: int = 0

    def __post_init__(self):
        self.element_type = ElementType.SHAPE


def design_element(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper
