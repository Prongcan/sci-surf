"""Verify the Responses boundary used by the paper pipeline."""

import base64
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from core.llm_client import ResponsesModelAdapter, create_llm_client, pdf_part


def test_responses_adapter_sends_pdf_and_preserves_usage():
    raw = SimpleNamespace(
        output_text="<Documents>paper-1</Documents>",
        status="completed",
        usage=SimpleNamespace(
            input_tokens=40,
            output_tokens=12,
            total_tokens=52,
            output_tokens_details=SimpleNamespace(reasoning_tokens=3),
        ),
    )
    client = Mock()
    client.responses.create.return_value = raw

    result = ResponsesModelAdapter(client).generate_content(
        model="gpt-6-luna", contents=["Paper ID: paper-1", pdf_part(b"%PDF-test"), "Rank it"]
    )

    request = client.responses.create.call_args.kwargs
    assert request["model"] == "gpt-6-luna"
    parts = request["input"][0]["content"]
    assert parts[0] == {"type": "input_text", "text": "Paper ID: paper-1"}
    assert base64.b64decode(parts[1]["file_data"].split(",", 1)[1]) == b"%PDF-test"
    assert parts[2] == {"type": "input_text", "text": "Rank it"}
    assert result.text == "<Documents>paper-1</Documents>"
    assert result.usage_metadata.prompt_token_count == 40
    assert result.usage_metadata.candidates_token_count == 12
    assert result.usage_metadata.thoughts_token_count == 3


def test_empty_model_output_fails_instead_of_saving_blank_blog():
    client = Mock()
    client.responses.create.return_value = SimpleNamespace(output_text="", status="incomplete", usage=None)
    with pytest.raises(ValueError, match="returned no text"):
        ResponsesModelAdapter(client).generate_content(model="gpt-6-luna", contents="Summarize")


def test_client_uses_environment_gateway(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("BASE_URL", "https://api.smilecodex.space/v1")
    with patch("core.llm_client.OpenAI") as openai:
        create_llm_client()
    kwargs = openai.call_args.kwargs
    assert kwargs["base_url"] == "https://api.smilecodex.space/v1"
    assert kwargs["default_headers"]["x-openai-actor-authorization"] == "local-image-extension"
