---
name: read-cn-pdf
description: Stable workflow for reading and extracting text from PDFs or script-generated Chinese summaries on Windows PowerShell, especially when direct paths become ?????, terminal output hits GBK/UnicodeEncodeError, or Chinese/symbol output becomes mojibake. Use before inspecting local Chinese rule PDFs, bilingual rulebook comparisons, or Chinese data extraction where Windows encoding has failed or is likely to fail.
---

# Read Chinese PDFs

Use this skill when reading local PDFs with Chinese filenames, Chinese folder names, or special symbols from Windows PowerShell. The goal is to avoid the common failed first attempt caused by PowerShell 5.1 path/output encoding.

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

4. Extract with PyMuPDF (`fitz`) and keep output bounded:

```powershell
@'
import os, fitz
path = os.environ['PDF_PATH']
doc = fitz.open(path)
for i, page in enumerate(doc):
    text = page.get_text()
    print(f"\n=== PAGE {i + 1} ===")
    print(text.replace("\n", " | ")[:4000])
'@ | python -
```

## Preferred Script

Use `scripts/extract_pdf_text.py` when the task is more than a one-off snippet. It accepts a path through `PDF_PATH` or `--path`, supports page ranges, keyword filtering, and bounded output.

Examples:

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PDF_PATH=(Get-ChildItem -LiteralPath 'rules CN' | Where-Object { $_.Name -like '*探索*' } | Select-Object -First 1).FullName
python 'C:\Users\lrui6\.codex\skills\read-cn-pdf\scripts\extract_pdf_text.py' --terms 荣誉点 战役物品 --max-chars 2500
```

```powershell
$env:PYTHONIOENCODING='utf-8'
python 'C:\Users\lrui6\.codex\skills\read-cn-pdf\scripts\extract_pdf_text.py' --path 'rules/Trench-Crusade-Digital-Rulebook.pdf' --pages 113-125 --terms "Glory Item" Exploration --max-chars 3000
```

## Rules

- Do not pass Chinese PDF paths as Python string literals unless they were already proven safe in the current shell.
- Do not trust mojibake in PowerShell output as evidence that the source file is corrupt. Re-run through UTF-8 output first.
- If direct output still fails, write extracted text to `tmp/pdfs/<name>.txt` with `encoding='utf-8'`, then inspect it with a UTF-8-aware command or targeted search.
- Keep extraction bounded with page ranges, search terms, or `--max-chars`; avoid dumping entire large rulebooks into the conversation.
- For bilingual checks, extract the English source pages and the Chinese PDF pages separately, then compare concepts and rule effects rather than relying on exact line layout.

## Non-PDF Chinese summaries

The same Windows PowerShell output problem can appear when loading Chinese data from JS/JSON/Python scripts, even when no PDF is involved. If a script-generated Chinese summary will be used as evidence, do not rely on terminal direct output.

Preferred pattern:

1. Generate a bounded Markdown or JSON report under `tmp/` with explicit UTF-8 encoding.
2. Read or search that file instead of trusting the console rendering.
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
