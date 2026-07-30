---
name: read-cn-pdf
description: Use when reading local PDFs or generated summaries with Chinese paths, Chinese text, special symbols, PowerShell mojibake, GBK output failures, UnicodeEncodeError, or an uncertain Python/PyMuPDF environment on Windows.
---

# Read Chinese PDFs

Reliably extract bounded text when Windows PowerShell path or output encoding is
unsafe.

## Default Workflow

1. Locate the PDF path with PowerShell, not a hard-coded Python string:

```powershell
$pdf = (Get-ChildItem -LiteralPath 'rules CN' | Where-Object { $_.Name -like '*探索*' } | Select-Object -First 1).FullName
```

2. Pass the path to Python through an environment variable:

```powershell
$env:PDF_PATH = $pdf
```

3. Force UTF-8 Python output before printing extracted text:

```powershell
$env:PYTHONIOENCODING = 'utf-8'
```

4. Use the launcher. It selects a PyMuPDF-capable Python from the current
   interpreter, Windows `py` launcher, or `PATH`.

```powershell
python 'C:\Users\lrui6\.codex\skills\read-cn-pdf\scripts\run_pdf_extract.py' --pages 1-5 --max-chars 2500
```

## Preferred Script

Use `scripts/run_pdf_extract.py` for normal work. Run `--help` for page ranges,
literal keyword filtering, bounded output, and verified UTF-8 file output.

Examples:

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PDF_PATH=(Get-ChildItem -LiteralPath 'rules CN' | Where-Object { $_.Name -like '*探索*' } | Select-Object -First 1).FullName
python 'C:\Users\lrui6\.codex\skills\read-cn-pdf\scripts\run_pdf_extract.py' --terms 荣誉点 战役物品 --max-chars 2500 --output 'tmp/pdfs/exploration.txt'
```

## Rules

- Do not pass Chinese PDF paths as Python string literals unless they were already proven safe in the current shell.
- Do not trust mojibake in PowerShell output as evidence that the source file is corrupt. Re-run through UTF-8 output first.
- Treat every `--terms` value as a literal Unicode substring. Use regular expressions only after the pattern and its encoding are known-good.
- When the extracted text will be evidence, use `--output`. The extractor writes UTF-8, performs an explicit UTF-8 read back, and fails if the content differs.
- If no capable Python is found, install `pymupdf` into a known interpreter; do not assume the first `python` command is the only environment.
- Keep extraction bounded with page ranges, search terms, or `--max-chars`; avoid dumping entire large rulebooks into the conversation.
- For bilingual checks, extract the English source pages and the Chinese PDF pages separately, then compare concepts and rule effects rather than relying on exact line layout.

## Non-PDF Chinese summaries

The same Windows PowerShell output problem can appear when loading Chinese data from JS/JSON/Python scripts, even when no PDF is involved. If a script-generated Chinese summary will be used as evidence, do not rely on terminal direct output.

Preferred pattern:

1. Generate a bounded Markdown or JSON report under `tmp/` with explicit UTF-8 encoding.
2. Read the file back with explicit UTF-8, then search that verified content instead of trusting the console rendering.
3. If a final answer needs Chinese names, take them from the source data or the UTF-8 report, not from mojibake terminal text.

Example for Node-based data inspection:

```powershell
@'
const fs = require('fs');
const rows = [
  ['name', 'effect'],
  ['失眠症', '移除渗透者关键词']
];
const text = rows.map((row) => row.join('\t')).join('\n');
fs.mkdirSync('tmp', { recursive: true });
fs.writeFileSync('tmp/chinese-summary.tsv', text, 'utf8');
'@ | node -
Get-Content -LiteralPath 'tmp/chinese-summary.tsv' -Encoding UTF8
```
