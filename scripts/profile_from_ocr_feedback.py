"""Generate a preview profile from explicit feedback and stored OCR first pages.

Run from the project root:
    python scripts/profile_from_ocr_feedback.py --user "Demo User"
    python scripts/profile_from_ocr_feedback.py --user "Demo User" --output /tmp/demo-profile.json
"""

import argparse
import json
import logging
import sys
from collections import Counter
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.config_utils import load_config
from core.rerankers import GeminiProfileExtractor
from orchestrator.orchestrator import load_orchestrator_config

logger = logging.getLogger(__name__)


def connect(db_config: dict, *, paper_db: bool = False):
    name_key = "db_name_paper" if paper_db else "db_name"
    return psycopg2.connect(
        host=db_config["db_host"],
        port=db_config["db_port"],
        user=db_config["db_user"],
        password=db_config["db_password"],
        dbname=db_config[name_key],
        connect_timeout=10,
    )


def load_explicit_feedback(db_config: dict, username: str) -> list[dict]:
    """Use the latest recommendation row for each paper, then filter its rating."""
    with connect(db_config) as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                WITH latest AS (
                    SELECT DISTINCT ON (paper_id)
                        paper_id, title, blog_liked, recommendation_date
                    FROM paper_recommendations
                    WHERE username = %s
                    ORDER BY paper_id, recommendation_date DESC NULLS LAST, id DESC
                )
                SELECT paper_id, title, blog_liked, recommendation_date
                FROM latest
                WHERE blog_liked IS NOT NULL
                ORDER BY recommendation_date, paper_id
                """,
                (username,),
            )
            return [dict(row) for row in cursor.fetchall()]


def load_ocr_first_pages(db_config: dict, paper_ids: list[str]) -> dict[str, str]:
    with connect(db_config, paper_db=True) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT doc_id, text_content
                FROM text_chunks
                WHERE doc_id = ANY(%s)
                  AND chunk_order = 0
                  AND NULLIF(btrim(text_content), '') IS NOT NULL
                """,
                (paper_ids,),
            )
            return dict(cursor.fetchall())


def build_training_examples(feedback: list[dict], first_pages: dict[str, str]) -> str:
    examples = []
    for paper in feedback:
        label = "LIKED" if paper["blog_liked"] is True else "DISLIKED"
        date = paper["recommendation_date"]
        day = date.date().isoformat() if date else "unknown"
        examples.append(
            f"Paper ID: {paper['paper_id']}\n"
            f"Recommendation date: {day}\n"
            f"Explicit feedback: {label}\n"
            f"Title: {paper['title'] or ''}\n"
            f"OCR first page:\n{first_pages[paper['paper_id']]}"
        )
    return "\n\n--- NEXT PAPER ---\n\n".join(examples)


def validate_profile(profile: dict) -> dict:
    keys = ("persona_definition", "negative_constraints", "ranking_heuristics")
    if not isinstance(profile, dict) or any(key not in profile for key in keys):
        raise ValueError("Model response is missing required profile fields")
    persona = profile["persona_definition"]
    if not isinstance(persona, str) or not persona.strip():
        raise ValueError("Model response has an invalid persona_definition")
    for key in keys[1:]:
        values = profile[key]
        if not isinstance(values, list) or len(values) > 5 or any(
            not isinstance(value, str) or not value.strip() for value in values
        ):
            raise ValueError(f"Model response has invalid {key}")
    return {key: profile[key] for key in keys}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", required=True, help="Exact username in the user database")
    parser.add_argument("--model", help="Override the production profile extraction model")
    parser.add_argument("--output", type=Path, help="Also save the preview as JSON")
    args = parser.parse_args()

    config = load_config(set_env=False)
    model = args.model or load_orchestrator_config("configs/production.yaml")["models"]["profile_extraction"]["model_id"]
    feedback = load_explicit_feedback(config["USER_DB"], args.user)
    if not feedback:
        logger.error("No explicit likes or dislikes for %s", args.user)
        return 1

    paper_ids = [paper["paper_id"] for paper in feedback]
    first_pages = load_ocr_first_pages(config["aliyun_rds"], paper_ids)
    missing = [paper_id for paper_id in paper_ids if paper_id not in first_pages]
    if missing:
        logger.error("OCR first page missing for: %s", ", ".join(missing))
        return 1

    counts = Counter(paper["blog_liked"] for paper in feedback)
    logger.info("%s: %d likes, %d dislikes, %d OCR first pages", args.user, counts[True], counts[False], len(first_pages))

    extractor = GeminiProfileExtractor(model_name=model, prompt_key="explicit_feedback_ocr_profile_prompt")
    prompt = extractor.prompt_template.format(
        training_examples=build_training_examples(feedback, first_pages)
    )
    response = extractor.client.models.generate_content(model=model, contents=prompt)
    profile = validate_profile(extractor._parse_json_response(response.text))
    output = json.dumps(profile, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        logger.info("Saved profile preview to %s", args.output)
    print(output, end="")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    sys.exit(main())
