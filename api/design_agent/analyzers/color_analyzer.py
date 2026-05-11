from typing import List, Tuple, Dict, Optional
from PIL import Image
import numpy as np
import colorsys

from core.color import ColorPalette


class ColorAnalyzer:
    def __init__(self):
        pass

    def analyze(self, image_path: str) -> Dict:
        img = Image.open(image_path).convert("RGB")
        img = img.resize((200, 200), Image.LANCZOS)
        pixels = np.array(img).reshape(-1, 3)

        dominant = self._get_dominant_colors(pixels, 5)
        palette = ColorPalette(colors=dominant, name="analyzed")

        brightness = self._analyze_brightness(pixels)
        saturation = self._analyze_saturation(pixels)
        color_temp = self._analyze_temperature(pixels)
        contrast = self._analyze_contrast(dominant)

        return {
            "palette": palette,
            "brightness": brightness,
            "saturation": saturation,
            "temperature": color_temp,
            "contrast": contrast,
            "mood": self._detect_mood(brightness, saturation, color_temp),
        }

    def _get_dominant_colors(self, pixels: np.ndarray, n: int) -> List[Tuple[int, int, int]]:
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=n, random_state=42, n_init="auto")
        kmeans.fit(pixels)
        return [tuple(map(int, c)) for c in kmeans.cluster_centers_]

    def _analyze_brightness(self, pixels: np.ndarray) -> float:
        luminance = np.dot(pixels, [0.299, 0.587, 0.114]) / 255
        return float(np.mean(luminance))

    def _analyze_saturation(self, pixels: np.ndarray) -> float:
        hsv = np.array([colorsys.rgb_to_hsv(r/255, g/255, b/255) for r, g, b in pixels])
        return float(np.mean(hsv[:, 1]))

    def _analyze_temperature(self, pixels: np.ndarray) -> str:
        r_avg = np.mean(pixels[:, 0])
        b_avg = np.mean(pixels[:, 2])
        ratio = r_avg / (b_avg + 1)
        if ratio > 1.2:
            return "warm"
        elif ratio < 0.8:
            return "cool"
        return "neutral"

    def _analyze_contrast(self, colors: List[Tuple[int, int, int]]) -> float:
        if len(colors) < 2:
            return 0.0
        luminances = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in colors]
        return float(max(luminances) - min(luminances)) / 255

    def _detect_mood(self, brightness: float, saturation: float, temp: str) -> str:
        if brightness > 0.7 and saturation > 0.5:
            return "vibrant"
        elif brightness < 0.3:
            return "dark"
        elif saturation < 0.2:
            return "minimalist"
        elif temp == "warm":
            return "cozy"
        elif temp == "cool":
            return "calm"
        return "balanced"
