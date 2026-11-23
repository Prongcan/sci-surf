"""Run manually: python tests/raw/check_gemini_api.py [model]"""

import os
from pathlib import Path
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main() -> int:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("失败：未设置 GEMINI_API_KEY")
        return 1

    base_url = os.getenv("GOOGLE_GEMINI_BASE_URL", "").strip()
    model = sys.argv[1] if len(sys.argv) > 1 else "gemini-2.5-flash"
    options = {"timeout": 30000, "retry_options": types.HttpRetryOptions(attempts=1)}
    if base_url:
        options.update(base_url=base_url.rstrip("/"), api_version="v1beta")
    try:
        with genai.Client(api_key=api_key, http_options=types.HttpOptions(**options)) as client:
            response = client.models.generate_content(model=model, contents="Reply only: OK")
        print(f"成功：API 调用通过（{model}）")
        print(response.text)
        return 0
    except Exception as exc:
        # Avoid printing credentials that might appear in an upstream error.
        message = str(exc).replace(api_key, "[REDACTED]")
        print(f"失败：{message}")
        print("认证失败通常为 401/403；模型不可用、额度不足或网络错误也会导致失败。")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
