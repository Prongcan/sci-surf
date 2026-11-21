# OpenAI Responses migration plan

## Repository baseline

- Starting branch: `main`; starting HEAD: `4226e74240082fb0640e6444498166388d454373`.
- At the start of this work, `pyproject.toml`, `core/generators.py`, `core/rerankers.py`, `core/profile_pool.py`, `backend/app/utils/index_utils.py`, and `.env.example` had local modifications; `core/gemini_client.py` and `tests/raw/check_openai_api.py` were untracked.
- `.env` is gitignored. `.env.example` contains a plaintext credential in a user modification and is deliberately excluded from commits.
- The independent smoke test `tests/raw/check_openai_api.py` succeeded with `OPENAI_API_KEY`, `BASE_URL=https://api.smilecodex.space/v1`, the custom request header, and `gpt-6-luna` via Responses.

## Implementation

1. Add a shared Responses adapter that loads `OPENAI_API_KEY` and `BASE_URL`, preserves the tested request header, converts text/PDF parts into Responses input, and normalizes text and token usage.
2. Migrate blog generation, text/PDF reranking, profile extraction and pool optimization, and backend query translation to the adapter. Keep public class contracts and output parsing stable where possible.
3. Update orchestrator and backend model configuration to a verified model, while leaving DashScope embeddings and PostgreSQL vector dimensions unchanged.
4. Update environment documentation and remove obsolete Gemini transport code.
5. Run unit/integration tests, a live text smoke test, and a small PDF capability test. If the gateway rejects PDF input, use extracted PDF text for this deployment and document the limitation.

## Validation and risks

- The working text model is `gpt-6-luna`; PDF input and model-specific generation parameters need separate validation.
- A text-only fallback must retain paper IDs, ordering, and parser output expected by recommendation and profile code.
- Do not commit credentials or print them in logs. Recheck Git status and diff before committing migration changes.

## Result

- Added `core/llm_client.py` as the common Responses transport. All generation, reranking, profile, and query-translation calls now use it. The existing public `Gemini*` class names remain as compatibility names for callers.
- Both development and production orchestrator configs now use the verified `gpt-6-luna` model. DashScope embedding and PostgreSQL vector configuration are unchanged.
- Live smoke requests through the adapter returned `OK` for text and `ORBIT-42` from a generated PDF. The gateway accepted `input_file` for the tested single-page PDF, so no text-only fallback was needed.
- `PAPERIGNITION_LOCAL_MODE=true pytest tests/unit tests/integration -q`: 149 passed. Ruff passed for modified Python files.
- The adapter does not expose Gemini thought summaries; the PDF reranker continues returning an empty summary in the existing tuple shape. Larger production PDFs have not been exercised through the gateway.
