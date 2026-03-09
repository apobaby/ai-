import base64
import os
from pathlib import Path
from typing import Optional

from openai import OpenAI


class OpenAIService:
    """Single AI gateway: OpenAI ChatGPT (Responses API + image generation tool)."""

    def __init__(self) -> None:
        # ChatGPT multimodal model (can be overridden, e.g. gpt-4o)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1")
        api_key = os.getenv("OPENAI_API_KEY")
        self.client: Optional[OpenAI] = OpenAI(api_key=api_key) if api_key else None

    def generate_image_from_prompt(self, prompt: str, *image_base64_list: str) -> str:
        """
        Generate image with ChatGPT image_generation tool.
        Returns base64 PNG/JPEG payload.
        """
        if self.client is None:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        content = [{"type": "input_text", "text": prompt}]
        for image_base64 in image_base64_list:
            if image_base64:
                content.append(
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{image_base64}",
                    }
                )

        response = self.client.responses.create(
            model=self.model,
            input=[{"role": "user", "content": content}],
            tools=[{"type": "image_generation"}],
        )

        # SDK objects vary by version; parse robustly.
        for output in response.output:
            if getattr(output, "type", "") == "image_generation_call" and getattr(output, "result", None):
                return output.result

        raise RuntimeError("OpenAI did not return generated image data")

    @staticmethod
    def to_base64(file_bytes: bytes) -> str:
        return base64.b64encode(file_bytes).decode("utf-8")

    @staticmethod
    def local_image_url_to_base64(image_url: str) -> str:
        # image_url examples: /uploads/avatar_xxx.png
        normalized = image_url.lstrip("/")
        image_path = Path(normalized)
        if not image_path.exists() or not image_path.is_file():
            raise FileNotFoundError(f"Image not found: {image_url}")
        return base64.b64encode(image_path.read_bytes()).decode("utf-8")
