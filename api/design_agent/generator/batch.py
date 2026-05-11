import os
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.styles import DesignStyle
from templates.base import get_template


class BatchGenerator:
    def __init__(self, style: DesignStyle, platform: str = "instagram_square"):
        self.style = style
        self.platform = platform

    def generate_all(self, template_name: str, contents: List[Dict[str, Any]],
                     output_dir: str = "output", parallel: bool = True) -> List[str]:
        os.makedirs(output_dir, exist_ok=True)
        results = []

        if parallel and len(contents) > 1:
            with ThreadPoolExecutor(max_workers=min(8, len(contents))) as executor:
                futures = {}
                for i, content in enumerate(contents):
                    filename = os.path.join(output_dir, f"design_{i:04d}.png")
                    future = executor.submit(self._generate_one, template_name, content, filename)
                    futures[future] = filename

                for future in as_completed(futures):
                    results.append(future.result())
        else:
            for i, content in enumerate(contents):
                filename = os.path.join(output_dir, f"design_{i:04d}.png")
                results.append(self._generate_one(template_name, content, filename))

        return sorted(results)

    def _generate_one(self, template_name: str, content: Dict[str, Any], output_path: str) -> str:
        try:
            template_cls = get_template(template_name)
            template = template_cls()
            template.setup(self.style, content)
            template.save(output_path)
            return output_path
        except Exception as e:
            return f"ERROR: {e}"
