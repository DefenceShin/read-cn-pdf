#!/usr/bin/env python
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def parse_py_launcher_path(line):
    match = re.search(r"([A-Za-z]:\\.+?python(?:3)?\.exe)\s*$", line, re.IGNORECASE)
    return match.group(1) if match else ""


def candidate_interpreters():
    candidates = [sys.executable, os.environ.get("PYTHON", "")]

    if os.name == "nt":
        py_launcher = shutil.which("py")
        if py_launcher:
            result = subprocess.run(
                [py_launcher, "-0p"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            for line in result.stdout.splitlines():
                candidate = parse_py_launcher_path(line)
                if candidate:
                    candidates.append(candidate)

        where_exe = shutil.which("where")
        if where_exe:
            result = subprocess.run(
                [where_exe, "python"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            candidates.extend(result.stdout.splitlines())
    else:
        candidates.extend(shutil.which(name) or "" for name in ("python3", "python"))

    seen = set()
    for candidate in candidates:
        candidate = str(candidate).strip()
        if not candidate:
            continue
        normalized = os.path.normcase(os.path.abspath(candidate))
        if normalized not in seen:
            seen.add(normalized)
            yield candidate


def find_pymupdf_python():
    for candidate in candidate_interpreters():
        result = subprocess.run(
            [candidate, "-c", "import fitz"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0:
            return candidate
    return None


def main():
    interpreter = find_pymupdf_python()
    if not interpreter:
        raise SystemExit(
            "No PyMuPDF-capable Python interpreter was found. "
            "Install pymupdf into an existing interpreter, then retry."
        )

    script = Path(__file__).with_name("extract_pdf_text.py")
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    result = subprocess.run([interpreter, str(script), *sys.argv[1:]], env=env)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
