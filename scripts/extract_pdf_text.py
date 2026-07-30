#!/usr/bin/env python
import argparse
import os
import re
import sys
from pathlib import Path


def parse_pages(spec, page_count):
    if not spec:
        return list(range(page_count))
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start = int(start_text) if start_text else 1
            end = int(end_text) if end_text else page_count
            pages.update(range(max(1, start) - 1, min(page_count, end)))
        else:
            page = int(part)
            if 1 <= page <= page_count:
                pages.add(page - 1)
    return sorted(pages)


def load_fitz():
    try:
        import fitz
    except ImportError as exc:
        raise SystemExit("PyMuPDF is required: python -m pip install pymupdf") from exc
    return fitz


def main():
    parser = argparse.ArgumentParser(description="Extract bounded UTF-8 text from a PDF.")
    parser.add_argument("--path", default=os.environ.get("PDF_PATH", ""), help="PDF path. Defaults to PDF_PATH.")
    parser.add_argument("--pages", default="", help="1-based pages/ranges, e.g. 1,3-5,10-.")
    parser.add_argument(
        "--terms",
        nargs="*",
        default=[],
        help="Only include pages containing any literal Unicode substring.",
    )
    parser.add_argument("--max-chars", type=int, default=4000, help="Maximum characters per printed page.")
    parser.add_argument("--raw-newlines", action="store_true", help="Keep newlines instead of replacing them with separators.")
    parser.add_argument(
        "--output",
        default="",
        help="Write the report as UTF-8, then read it back and verify it.",
    )
    args = parser.parse_args()

    if not args.path:
        raise SystemExit("Provide --path or set PDF_PATH.")

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"PDF not found: {path}")

    fitz = load_fitz()
    report_lines = []
    with fitz.open(str(path)) as doc:
        terms = [term.casefold() for term in args.terms]
        selected_pages = parse_pages(args.pages, doc.page_count)

        report_lines.append(f"FILE {path}")
        report_lines.append(f"PAGES {doc.page_count}")

        for page_index in selected_pages:
            text = doc[page_index].get_text()
            folded_text = text.casefold()
            if terms and not any(term in folded_text for term in terms):
                continue
            page_output = text if args.raw_newlines else re.sub(r"\s*\n\s*", " | ", text)
            report_lines.append(f"\n=== PAGE {page_index + 1} ===")
            report_lines.append(page_output[: max(0, args.max_chars)])

    report = "\n".join(report_lines) + "\n"
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        if output_path.read_text(encoding="utf-8") != report:
            raise SystemExit(f"UTF-8 output verification failed: {output_path}")
        print(f"UTF-8 output verified: {output_path}")
    else:
        print(report, end="")


if __name__ == "__main__":
    try:
        main()
    except UnicodeEncodeError:
        sys.stderr.write(
            "Unicode output failed. In PowerShell run: $env:PYTHONIOENCODING='utf-8'\n"
        )
        raise
