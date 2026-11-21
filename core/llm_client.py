"""OpenAI Responses transport shared by paper generation and recommendation."""

import base64
import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class PDFPart:
    data: bytes
    filename: str = "paper.pdf"


def pdf_part(data: bytes, filename: str = "paper.pdf") -> PDFPart:
    return PDFPart(data=data, filename=filename)


@dataclass
class UsageMetadata:
    prompt_token_count: int = 0
    candidates_token_count: int = 0
    thoughts_token_count: int = 0
    total_token_count: int = 0


@dataclass
class ContentResponse:
    text: str
    usage_metadata: UsageMetadata


class ResponsesModelAdapter:
    """Keep the existing generate_content call sites while using Responses."""

    def __init__(self, client: OpenAI):
        self.client = client

    def generate_content(self, *, model: str, contents: str | list) -> ContentResponse:
        parts = [contents] if isinstance(contents, str) else contents
        content = []
        for part in parts:
            if isinstance(part, PDFPart):
                encoded = base64.b64encode(part.data).decode("ascii")
                content.append({
                    "type": "input_file",
                    "filename": part.filename,
                    "file_data": f"data:application/pdf;base64,{encoded}",
                })
            elif isinstance(part, str):
                content.append({"type": "input_text", "text": part})
            else:
                raise TypeError(f"Unsupported model input: {type(part).__name__}")

        response = self.client.responses.create(
            model=model,
            input=[{"role": "user", "content": content}],
        )
        text = response.output_text or ""
        if not text.strip():
            raise ValueError(f"Model {model} returned no text (status={response.status})")
        usage = response.usage
        output_details = getattr(usage, "output_tokens_details", None)
        return ContentResponse(
            text=text,
            usage_metadata=UsageMetadata(
                prompt_token_count=getattr(usage, "input_tokens", 0) or 0,
                candidates_token_count=getattr(usage, "output_tokens", 0) or 0,
                thoughts_token_count=getattr(output_details, "reasoning_tokens", 0) or 0,
                total_token_count=getattr(usage, "total_tokens", 0) or 0,
            ),
        )


class LLMClient:
    def __init__(self, client: OpenAI):
        self.models = ResponsesModelAdapter(client)


def create_llm_client(api_key: str | None = None) -> LLMClient:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    base_url = os.getenv("BASE_URL", "https://api.openai.com/v1").strip()
    if not base_url:
        raise ValueError("BASE_URL must not be empty")
    headers = {}
    if "api.smilecodex.space" in base_url:
        headers["x-openai-actor-authorization"] = "local-image-extension"
    return LLMClient(OpenAI(api_key=api_key, base_url=base_url, default_headers=headers, timeout=60, max_retries=0))
