from flask import Flask, request, jsonify
import json
import io
import base64
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "design_agent"))

from core.styles import DesignStyle, TextStyle
from core.color import ColorPalette
from generator import text_to_design as ttd
from templates.base import list_templates, get_template
import templates.social  # registers templates via decorators

app = Flask(__name__)

_PALETTES = ttd._PRESET_PALETTES


@app.route("/api/generate", methods=["GET", "POST"])
def handle_generate():
    if request.method == "GET":
        return jsonify({"palettes": _PALETTES})

    params = request.get_json(silent=True) or {}
    mode = params.get("mode", "fill")
    template = params.get("template", "quote_card")
    platform = params.get("platform", "instagram_square")
    palette_name = params.get("palette", "minimal")
    title = params.get("title", "Your Design")
    subtitle = params.get("subtitle", "")
    quote = params.get("quote", title)
    author = params.get("author", subtitle)

    palette = ColorPalette.from_hex_list(
        _PALETTES.get(palette_name, _PALETTES["minimal"]), name=palette_name
    )

    if mode == "txt":
        gen = ttd.TextToDesignGenerator()
        result = gen.generate(title, platform)
        style = result["style"]
        content = result["content"]
        template = result["spec"].get("template", template)
        tpl = get_template(template)()
        tpl.setup(style, content)
    else:
        style = DesignStyle(
            name="web_generated",
            palette=palette,
            title_style=TextStyle(
                font_size=48, font_weight="bold", color=palette.get_text_color(0)
            ),
            subtitle_style=TextStyle(
                font_size=24, font_weight="normal", color=palette.get_accent(1)
            ),
        )
        content = {
            "title": title,
            "subtitle": subtitle,
            "body": params.get("body", ""),
            "quote": quote,
            "author": author,
        }
        tpl = get_template(template)()
        tpl.setup(style, content)

    img = tpl.render()
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    return jsonify({
        "image": b64,
        "format": "png",
        "width": img.width,
        "height": img.height,
    })


@app.route("/api/templates")
def handle_templates():
    return jsonify({"templates": list_templates()})
