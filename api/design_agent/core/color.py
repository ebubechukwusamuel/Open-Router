import colorsys
import random
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from PIL import Image
import numpy as np


@dataclass
class ColorPalette:
    colors: List[Tuple[int, int, int]] = field(default_factory=list)
    name: str = ""

    @classmethod
    def from_hex_list(cls, hex_colors: List[str], name: str = ""):
        rgb = []
        for h in hex_colors:
            h = h.lstrip("#")
            rgb.append(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
        return cls(colors=rgb, name=name)

    @classmethod
    def from_image(cls, image_path: str, n_colors: int = 5):
        return extract_colors_from_image(image_path, n_colors)

    def to_hex(self) -> List[str]:
        return [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in self.colors]

    def to_rgb(self) -> List[Tuple[int, int, int]]:
        return self.colors

    def analogous(self, n: int = 3) -> "ColorPalette":
        hsv_colors = [colorsys.rgb_to_hsv(r/255, g/255, b/255) for r, g, b in self.colors]
        base = hsv_colors[0]
        results = []
        for i in range(n):
            h = (base[0] + (i - n//2) * 0.03) % 1.0
            r, g, b = colorsys.hsv_to_rgb(h, base[1], base[2])
            results.append((int(r*255), int(g*255), int(b*255)))
        return ColorPalette(colors=results, name=f"{self.name}_analogous")

    def complementary(self) -> "ColorPalette":
        h, s, v = colorsys.rgb_to_hsv(self.colors[0][0]/255, self.colors[0][1]/255, self.colors[0][2]/255)
        h = (h + 0.5) % 1.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return ColorPalette(colors=[(int(r*255), int(g*255), int(b*255))], name=f"{self.name}_complementary")

    def generate_variant(self, style: str = "vibrant") -> "ColorPalette":
        new_colors = []
        for r, g, b in self.colors:
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            if style == "vibrant":
                s = min(1.0, s * 1.3)
                v = min(1.0, v * 1.2)
            elif style == "muted":
                s = max(0.1, s * 0.6)
                v = max(0.3, v * 0.8)
            elif style == "dark":
                v = max(0.1, v * 0.4)
            elif style == "pastel":
                s = max(0.1, s * 0.4)
                v = min(1.0, v * 0.7 + 0.3)
            nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
            new_colors.append((int(nr*255), int(ng*255), int(nb*255)))
        return ColorPalette(colors=new_colors, name=f"{self.name}_{style}")

    def get_text_color(self, bg_index: int = 0) -> Tuple[int, int, int]:
        bg = self.colors[bg_index]
        luminance = (0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]) / 255
        return (255, 255, 255) if luminance < 0.5 else (0, 0, 0)

    def get_accent(self, index: int = 1) -> Tuple[int, int, int]:
        return self.colors[min(index, len(self.colors) - 1)]

    def get_gradient(self, start_index: int = 0, end_index: int = 1) -> Tuple[Tuple[int,int,int], Tuple[int,int,int]]:
        return self.colors[start_index], self.colors[min(end_index, len(self.colors)-1)]


def extract_colors_from_image(image_path: str, n_colors: int = 5) -> ColorPalette:
    img = Image.open(image_path).convert("RGB")
    img = img.resize((150, 150))
    pixels = np.array(img).reshape(-1, 3)

    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init="auto")
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int).tolist()
    colors = sorted([(int(r), int(g), int(b)) for r, g, b in colors],
                    key=lambda c: np.sum((c - np.mean(colors, axis=0))**2), reverse=True)
    return ColorPalette(colors=colors, name="extracted")
