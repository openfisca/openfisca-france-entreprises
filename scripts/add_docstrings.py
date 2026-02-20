#!/usr/bin/env python3
"""Add minimal docstrings for D100, D101, D102. Run from repo root after: ruff check openfisca_france_entreprises --select D100,D101,D102 --output-format=json."""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PKG = REPO_ROOT / "openfisca_france_entreprises"


def get_indent(line: str) -> str:
    match = re.match(r"^(\s*)", line)
    return match.group(1) if match else ""


def main() -> None:
    result = subprocess.run(
        [
            "uv",
            "run",
            "ruff",
            "check",
            "openfisca_france_entreprises",
            "--select",
            "D100,D101,D102",
            "--output-format=json",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(result.stderr or result.stdout, file=sys.stderr)
        sys.exit(1)

    by_file: dict[str, list[tuple[int, str]]] = {}
    for item in data:
        path = item["filename"]
        if not path.startswith(str(REPO_ROOT)):
            path = str(REPO_ROOT / path) if not Path(path).is_absolute() else path
        rel = path.replace(str(REPO_ROOT) + "/", "")
        row = item["location"]["row"]
        code = item["code"]
        by_file.setdefault(rel, []).append((row, code))

    for rel, items in by_file.items():
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)
        if not lines:
            continue
        # Process from bottom to top so line numbers stay valid
        for row, code in sorted(set(items), key=lambda x: (-x[0], x[1])):
            idx = row - 1  # 1-based to 0-based (line of the class/def or module start)
            if code == "D100":
                # Insert module docstring at top (after shebang/encoding if present)
                insert_at = 0
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if stripped.startswith("#!") or (stripped.startswith("#") and "coding" in stripped):
                        insert_at = i + 1
                    else:
                        break
                doc = '"""Variables and formulas for this module."""\n'
                if insert_at < len(lines) and lines[insert_at].strip().startswith('"""'):
                    continue  # Already has module docstring
                lines.insert(insert_at, doc)
                continue
            if code == "D101":
                # Insert class docstring after the class line
                if idx + 1 >= len(lines):
                    indent = "    "
                else:
                    indent = get_indent(lines[idx + 1])
                doc = indent + '"""OpenFisca variable."""\n'
                if idx + 1 < len(lines) and lines[idx + 1].strip().startswith('"""'):
                    continue
                lines.insert(idx + 1, doc)
                continue
            if code == "D102":
                # Insert method docstring after the def line
                if idx + 1 >= len(lines):
                    indent = "        "
                else:
                    indent = get_indent(lines[idx + 1])
                doc = indent + '"""Compute value for the given period."""\n'
                if idx + 1 < len(lines) and lines[idx + 1].strip().startswith('"""'):
                    continue
                lines.insert(idx + 1, doc)

        path.write_text("".join(lines), encoding="utf-8")
        print("Updated:", rel)


if __name__ == "__main__":
    main()
