"""Decorative element generators for creative compositions."""
import math
import random
from typing import List, Tuple, Optional
from core.elements import ShapeElement, Box
from core.canvas import Canvas


def generate_circles(
    canvas: Canvas,
    palette_colors: List[Tuple[int, int, int]],
    count: int = 5,
    base_opacity: int = 30,
    size_range: Tuple[int, int] = (50, 300),
    z_start: int = 0,
) -> List[ShapeElement]:
    """Generate randomly placed decorative circles."""
    w, h = canvas.width, canvas.height
    elements = []
    for i in range(count):
        radius = random.randint(*size_range)
        x = random.randint(-radius // 2, w - radius // 2)
        y = random.randint(-radius // 2, h - radius // 2)
        color = random.choice(palette_colors)
        opacity = random.randint(base_opacity, base_opacity + 60)
        elements.append(ShapeElement(
            box=Box(x=x, y=y, width=radius, height=radius),
            shape_type="circle",
            color=(*color, opacity),
            z_index=z_start + i,
        ))
    return elements


def generate_diagonal_split(
    canvas: Canvas,
    top_color: Tuple[int, int, int],
    bottom_color: Tuple[int, int, int],
    top_opacity: int = 255,
    bottom_opacity: int = 255,
    angle_deg: float = 15,
    z_index: int = 0,
) -> List[ShapeElement]:
    """Create a diagonal split background using two large overlapping rects."""
    w, h = canvas.width, canvas.height
    import math
    rad = math.radians(angle_deg)
    offset = int(math.tan(rad) * w)

    top = ShapeElement(
        box=Box(x=0, y=0, width=w, height=h // 2 + offset),
        shape_type="rectangle",
        color=(*top_color, top_opacity),
        z_index=z_index,
    )
    bottom = ShapeElement(
        box=Box(x=0, y=h // 2 + offset, width=w, height=h // 2 - offset + 50),
        shape_type="rectangle",
        color=(*bottom_color, bottom_opacity),
        z_index=z_index,
    )
    return [top, bottom]


def generate_dots_grid(
    canvas: Canvas,
    color: Tuple[int, int, int],
    spacing: int = 60,
    dot_radius: int = 3,
    opacity: int = 40,
    z_index: int = 0,
) -> List[ShapeElement]:
    """Generate a subtle dot grid pattern."""
    w, h = canvas.width, canvas.height
    elements = []
    for x in range(spacing, w, spacing):
        for y in range(spacing, h, spacing):
            elements.append(ShapeElement(
                box=Box(x=x, y=y, width=dot_radius, height=dot_radius),
                shape_type="circle",
                color=(*color, opacity),
                z_index=z_index,
            ))
    return elements


def generate_corner_accent(
    canvas: Canvas,
    color: Tuple[int, int, int],
    corner: str = "top-right",
    size: int = 200,
    opacity: int = 60,
    z_index: int = 0,
) -> ShapeElement:
    """Add a decorative corner accent."""
    w, h = canvas.width, canvas.height
    positions = {
        "top-left": (0, 0, size, size),
        "top-right": (w - size, 0, w, size),
        "bottom-left": (0, h - size, size, h),
        "bottom-right": (w - size, h - size, w, h),
    }
    x1, y1, x2, y2 = positions.get(corner, positions["top-right"])
    return ShapeElement(
        box=Box(x=x1, y=y1, width=x2 - x1, height=y2 - y1),
        shape_type="rectangle",
        color=(*color, opacity),
        z_index=z_index,
    )


def generate_waves(
    canvas: Canvas,
    color: Tuple[int, int, int],
    count: int = 3,
    opacity: int = 40,
    z_index: int = 0,
) -> List[ShapeElement]:
    """Generate horizontal wave-like bars."""
    w, h = canvas.width, canvas.height
    elements = []
    bar_height = h // (count * 3)
    for i in range(count):
        y = random.randint(0, h - bar_height)
        width_offset = random.randint(50, 200)
        elements.append(ShapeElement(
            box=Box(x=-width_offset // 2, y=y, width=w + width_offset, height=bar_height),
            shape_type="rectangle",
            color=(*color, opacity - i * 10),
            z_index=z_index,
        ))
    return elements


def generate_frame_border(
    canvas: Canvas,
    color: Tuple[int, int, int],
    width_px: int = 2,
    margin: int = 30,
    opacity: int = 80,
    z_index: int = 0,
) -> List[ShapeElement]:
    """Create a clean frame border."""
    w, h = canvas.width, canvas.height
    c = (*color, opacity)
    return [
        ShapeElement(box=Box(x=margin, y=margin, width=w - 2 * margin, height=width_px), shape_type="rectangle", color=c, z_index=z_index),
        ShapeElement(box=Box(x=margin, y=h - margin - width_px, width=w - 2 * margin, height=width_px), shape_type="rectangle", color=c, z_index=z_index),
        ShapeElement(box=Box(x=margin, y=margin, width=width_px, height=h - 2 * margin), shape_type="rectangle", color=c, z_index=z_index),
        ShapeElement(box=Box(x=w - margin - width_px, y=margin, width=width_px, height=h - 2 * margin), shape_type="rectangle", color=c, z_index=z_index),
    ]


def generate_overlapping_shapes(
    canvas: Canvas,
    palette_colors: List[Tuple[int, int, int]],
    count: int = 4,
    base_opacity: int = 50,
    z_start: int = 0,
) -> List[ShapeElement]:
    """Generate overlapping geometric shapes at canvas edges."""
    w, h = canvas.width, canvas.height
    elements = []
    shapes = ["circle", "rounded_rectangle"]
    for i in range(count):
        shape_type = random.choice(shapes)
        size = random.randint(120, 400)
        # Place at edges
        edge = random.choice(["left", "right", "top", "bottom"])
        if edge == "left":
            x, y = -size // 3, random.randint(0, h - size)
        elif edge == "right":
            x, y = w - size * 2 // 3, random.randint(0, h - size)
        elif edge == "top":
            x, y = random.randint(0, w - size), -size // 3
        else:
            x, y = random.randint(0, w - size), h - size * 2 // 3

        color = random.choice(palette_colors)
        opacity = random.randint(base_opacity, base_opacity + 100)
        elements.append(ShapeElement(
            box=Box(x=x, y=y, width=size, height=size),
            shape_type=shape_type,
            color=(*color, opacity),
            corner_radius=size // 4,
            z_index=z_start + i,
        ))
    return elements
