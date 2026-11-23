"""Opt-in live PaddleOCR-VL test against a real paper PDF.

Run with: RUN_BAIDU_OCR_LIVE=1 pytest -s tests/test_baidu_vl_live.py
"""

import os
import shutil
from pathlib import Path

import pytest
from dotenv import load_dotenv

from core.arxiv.pdf_extractor import PDFExtractor_baidu_vl


@pytest.mark.skipif(os.getenv("RUN_BAIDU_OCR_LIVE") != "1", reason="requires live Baidu OCR quota")
def test_real_paper_pdf(tmp_path):
    load_dotenv(Path(__file__).parents[1] / ".env")
    api_key = os.getenv("BAIDU_OCR_API_KEY")
    secret_key = os.getenv("BAIDU_OCR_SECRET_KEY")
    if not api_key or not secret_key:
        pytest.skip("BAIDU_OCR_API_KEY and BAIDU_OCR_SECRET_KEY are required")

    source = os.getenv("BAIDU_OCR_TEST_PDF")
    if source:
        source_pdf = Path(source)
    else:
        pdf_dir = Path(__file__).parents[1] / "orchestrator/orchestrator/pdfs"
        source_pdf = pdf_dir / "2611.01900v1.pdf"
    if source_pdf is None or not source_pdf.is_file():
        pytest.skip("Set BAIDU_OCR_TEST_PDF to a real local PDF")

    pdf_path = tmp_path / source_pdf.name
    shutil.copy2(source_pdf, pdf_path)
    extractor = PDFExtractor_baidu_vl(api_key, secret_key, max_wait=120)
    text_chunks, figure_chunks, table_chunks = extractor.extract(
        pdf_path, source_pdf.stem, tmp_path / "imgs"
    )

    markdown = pdf_path.with_suffix(".md")
    assert markdown.is_file() and markdown.stat().st_size > 0
    assert text_chunks or table_chunks or figure_chunks
    assert all(Path(fig.image_path).is_file() for fig in figure_chunks)
    if not source:
        assert figure_chunks and table_chunks
    print(f"PDF: {source_pdf.name}; text={len(text_chunks)}, "
          f"figures={len(figure_chunks)}, tables={len(table_chunks)}")
