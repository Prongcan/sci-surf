"""Run: OPENAI_API_KEY=... python tests/raw/check_openai_api.py"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def main() -> int:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("失败：未设置 OPENAI_API_KEY")
        return 1
    try:
        with OpenAI(
            api_key=api_key,
            base_url="https://api.smilecodex.space/v1",
            default_headers={"x-openai-actor-authorization": "local-image-extension"},
            timeout=60,
            max_retries=0,
        ) as client:
            response = client.responses.create(model="gpt-6-luna", input="Reply only: OK")
        print(f"成功：{response.model}，status={response.status}")
        print(response.output_text)
        return 0
    except Exception as exc:
        print(f"失败：{str(exc).replace(api_key, '[REDACTED]')}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
