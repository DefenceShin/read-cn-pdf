---
name: read-cn-pdf
description: Use for local PDF evidence on Windows when Chinese paths/output encoding, uncertain PDF runtimes, or unreliable text layers need diagnosis. Not for ordinary translation or all PDF tasks.
---

# Read Chinese PDFs

Reliably extract bounded text when Windows PowerShell path or output encoding is
unsafe.

## Default Workflow

Resolve the actual PDF with PowerShell, pass its path through `PDF_PATH`, and set `PYTHONIOENCODING=utf-8`. Use `scripts/run_pdf_extract.py` from this Skill's actual installation; it locates a PyMuPDF-capable interpreter. Keep page ranges and output bounded.

When constructing the command, read [Windows extraction example](references/windows-extraction.md). For options, use `scripts/extract_pdf_text.py --help`; this parses help without importing PyMuPDF, whereas the launcher probes runtimes first.

## Evidence Triage

Before treating extracted text as evidence:

1. Record the file identity and distinguish the extractor's 1-based physical
   page from any printed page number visible on the page.
2. Judge whether the text layer is adequate. Non-empty text can still be stale,
   duplicated, covered, or left behind on an illustration or replaced page.
3. If extraction is blank, implausibly short, contradictory, or visibly
   misaligned, render the bounded pages with the PDF workflow and inspect the
   visible page. Text extraction is not OCR and cannot prove absence.
4. For scanned/image-only pages, use rendering or OCR as evidence and label the
   method. Never infer mechanics from a translation merely because the
   authoritative scan has no text layer.
5. If the launcher reports that no PyMuPDF-capable interpreter exists, do not
   repeat the same command. Locate another installed interpreter or bundled PDF
   runtime; use bounded `pypdf` extraction when a usable text layer exists, and
   render when it does not. Do not install dependencies without authorization.
   A launcher error suggesting installation is not itself authorization. Check
   candidate executable paths before retrying; a stale `PYTHON` override or
   command wrapper may fail before the module probe can finish.

## Preferred Script

When extracting rule tables or multi-page named entries for implementation or
audit evidence, read [Entry boundaries and evidence](references/entry-evidence.md).
It covers continuation clauses, adjacent-entry contamination and currency glyphs.

Use `scripts/run_pdf_extract.py` for normal work. Read extractor help for page ranges,
literal substring filtering, bounded output, and verified UTF-8 file output.

## Rules

- Do not pass Chinese PDF paths as Python string literals unless they were already proven safe in the current shell.
- Do not trust mojibake in PowerShell output as evidence that the source file is corrupt. Re-run through UTF-8 output first.
- Treat every `--terms` value as a literal Unicode substring. Use regular expressions only after the pattern and its encoding are known-good.
- A `--terms` search with no matches is not evidence that the rule is absent. Retry with aliases or a bounded page range, then render the likely pages if the result matters.
- When the extracted text will be evidence, use `--output`. The extractor writes UTF-8, performs an explicit UTF-8 read back, and fails if the content differs.
- `--output` saves the same filtered, truncated report: `--max-chars` also limits saved text per physical page (0 means no text), and `--terms` excludes unmatched pages. UTF-8 readback proves encoding integrity, not completeness. For final evidence, use explicit narrow page ranges, `--raw-newlines`, no term filter, and a sufficient positive character limit; verify entry endings and continuation pages.
- Keep extraction bounded with page ranges, search terms, or `--max-chars`; avoid dumping entire large rulebooks into the conversation.
- For bilingual checks, extract or render the English source pages and Chinese reference pages separately. Compare entry identity, actors, timing, targets, costs, limits, outcomes, and exceptions rather than relying on exact line layout.

## Non-PDF Chinese summaries

The same output problem affects Chinese-heavy JS/JSON reports. Write a bounded
Markdown, TSV, or JSON file under `tmp/` with explicit UTF-8, read it back with
explicit UTF-8, and take quoted names from the source or verified file rather
than mojibake terminal output.
