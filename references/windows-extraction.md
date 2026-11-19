# Windows bounded extraction example

Read when constructing a Windows extraction command. Resolve the launcher relative to this Skill installation; the historical absolute path below is only an example.

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

