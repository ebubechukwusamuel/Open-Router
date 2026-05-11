from typing import Dict, Any, Optional
import os
import json


class LLMClient:
    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.provider = provider

    def interpret_design_prompt(self, prompt: str, platform: str) -> Dict[str, Any]:
        if not self.api_key:
            return self._fallback_spec(prompt, platform)

        try:
            if self.provider == "openai":
                return self._call_openai(prompt, platform)
            elif self.provider == "anthropic":
                return self._call_anthropic(prompt, platform)
            else:
                return self._fallback_spec(prompt, platform)
        except Exception:
            return self._fallback_spec(prompt, platform)

    def _call_openai(self, prompt: str, platform: str) -> Dict[str, Any]:
        import openai
        client = openai.OpenAI(api_key=self.api_key)

        system_prompt = """You are a design spec generator. Given a user's description of a graphic design,
output a JSON object with these fields:
- title: the main headline text
- subtitle: secondary text
- body: body text (if any)
- mood: one of [dark, vibrant, minimal, warm, calm, luxury, pastel, neon]
- template: one of [instagram_square, instagram_story, twitter_post, youtube_thumbnail, quote_card, pinterest]
- description: a short visual description of the design style
- font_size: an integer (24-72)

Output ONLY valid JSON, no markdown, no explanation."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Platform: {platform}\nPrompt: {prompt}"},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )

        content = response.choices[0].message.content
        return json.loads(content)

    def _call_anthropic(self, prompt: str, platform: str) -> Dict[str, Any]:
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            system="You generate design specs as JSON. Output ONLY valid JSON with fields: title, subtitle, body, mood, template, description, font_size.",
            messages=[{"role": "user", "content": f"Platform: {platform}\nPrompt: {prompt}"}],
        )
        content = response.content[0].text
        return json.loads(content)

    def _fallback_spec(self, prompt: str, platform: str) -> Dict[str, Any]:
        mood_map = {
            "dark": "dark", "moody": "dark",
            "bright": "vibrant", "vibrant": "vibrant",
            "clean": "minimal", "simple": "minimal",
            "warm": "warm", "sunset": "warm",
            "luxury": "luxury", "elegant": "luxury",
        }

        prompt_lower = prompt.lower()
        mood = "minimal"
        for kw, m in mood_map.items():
            if kw in prompt_lower:
                mood = m
                break

        lines = [l.strip() for l in prompt.split("\n") if l.strip()]
        title = lines[0][:80] if lines else "Your Design"
        subtitle = lines[1][:120] if len(lines) > 1 else ""

        template_map = {
            "quote": "quote_card", "story": "instagram_story",
            "thumbnail": "youtube_thumbnail", "pin": "pinterest",
            "twitter": "twitter_post", "post": "instagram_square",
        }
        template = "instagram_square"
        for kw, t in template_map.items():
            if kw in prompt_lower:
                template = t
                break

        return {
            "title": title,
            "subtitle": subtitle,
            "body": "",
            "mood": mood,
            "template": template,
            "description": prompt,
            "font_size": 48 if platform in ("instagram_story", "pinterest") else 36,
        }
