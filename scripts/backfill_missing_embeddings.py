"""Generate embeddings for stored papers that do not have one yet."""

import argparse
import logging
import os

import psycopg2
from dotenv import load_dotenv

from backend.config_utils import load_config
from orchestrator.storage_util import EmbeddingClient, RDSConfig, RDSDBManager


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Backend config for the paper database")
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error("--batch-size must be positive")

    load_dotenv()
    config = load_config(args.config, set_env=False)
    db = config["aliyun_rds"]
    if not db.get("enabled"):
        parser.error("Paper database is disabled in the selected config")

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        parser.error("DASHSCOPE_API_KEY is required")
    embedding_config = config["dashscope"]
    embedding_client = EmbeddingClient(
        api_key=api_key,
        base_url=os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        model=embedding_config.get("embedding_model", "text-embedding-v4"),
        dimension=int(embedding_config.get("embedding_dimension", 1536)),
    )
    db_config = RDSConfig(
        host=db["db_host"],
        port=int(db["db_port"]),
        database=db["db_name_paper"],
        user=db["db_user"],
        password=db["db_password"],
        sslmode=db.get("sslmode", "prefer"),
    )
    manager = RDSDBManager(db_config, embedding_client)
    with psycopg2.connect(
        host=db_config.host,
        port=db_config.port,
        dbname=db_config.database,
        user=db_config.user,
        password=db_config.password,
        sslmode=db_config.sslmode,
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.doc_id, p.title, p.abstract
                FROM papers p
                LEFT JOIN paper_embeddings e ON e.doc_id = p.doc_id
                WHERE e.doc_id IS NULL
                ORDER BY p.doc_id
            """)
            missing = cursor.fetchall()

    print(f"Missing embeddings: {len(missing)}", flush=True)
    failed = 0
    for offset in range(0, len(missing), args.batch_size):
        chunk = missing[offset:offset + args.batch_size]
        vectors = embedding_client.get_embeddings([f"{title}. {abstract}" for _, title, abstract in chunk])
        papers = [{"doc_id": doc_id, "title": title, "abstract": abstract} for doc_id, title, abstract in chunk]
        succeeded, batch_failed = manager.batch_insert_embeddings(papers, vectors)
        failed += batch_failed
        print(f"Processed {offset + len(chunk)}/{len(missing)}; inserted {succeeded}, failed {batch_failed}", flush=True)

    manager.close()
    return 1 if failed else 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    raise SystemExit(main())
