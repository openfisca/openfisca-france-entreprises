#!/usr/bin/env python3
"""Generate a single coefficient.yaml for TCCFE with all years (2011–2022) and notes.

Reads:
- coefficient_2011.yaml for 2011 values (or leave empty if missing)
- taux_2012.py .. taux_2022.py for values and (from one file) commune names as notes.

Verifies that every key has a note (commune name). Output: coefficient.yaml only.

Run from repo root:
  uv run python scripts/generate_tccfe_coefficient_yaml.py
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TCCFE_DIR = REPO_ROOT / "openfisca_france_entreprises/variables/taxes/taxation_energies/tccfe"
PARAMS_DIR = REPO_ROOT / "openfisca_france_entreprises/parameters/energies/electricite/tcfe/tccfe"
COEFF_2011_YAML = PARAMS_DIR / "coefficient_2011.yaml"
OUT_YAML = PARAMS_DIR / "coefficient.yaml"
YEARS = list(range(2011, 2023))  # 2011..2022
NOTE_SOURCE_PY = TCCFE_DIR / "taux_2018.py"  # same keys, commune names in comments


def extract_taux_from_py(content: str) -> dict[tuple[str, str], float]:
    """Extract taux dict as (dep, com) -> value from Python source."""
    result = {}
    tuple_re = re.compile(r'\s*\(["\']([^"\']*)["\'],\s*["\']([^"\']*)["\']\)\s*:\s*([\d.]+)')
    manquant_re = re.compile(r'\s*["\']manquant["\']\s*:\s*([\d.]+)')
    in_dict = False
    brace_count = 0
    for line in content.splitlines():
        if "taux = {" in line:
            in_dict = True
            brace_count = 1
            continue
        if not in_dict:
            continue
        brace_count += line.count("{") - line.count("}")
        m = tuple_re.search(line)
        if m:
            dep, com, val = m.groups()
            result[(dep, com)] = float(val)
            continue
        m = manquant_re.search(line)
        if m:
            result["manquant"] = float(m.group(1))  # type: ignore[assignment]
        if brace_count <= 0:
            break
    return result  # type: ignore[return-value]


def parse_notes_from_yaml(path: Path) -> dict[str, str]:
    """Parse coefficient YAML and return key -> metadata.note."""
    key_re = re.compile(r'^("([^"]+)"):\s*$')
    note_re = re.compile(r'^\s+note:\s*(.+)$')
    result = {}
    current_key = None
    in_metadata = False
    for line in path.read_text(encoding="utf-8").splitlines():
        m = key_re.match(line)
        if m:
            current_key = m.group(2)
            in_metadata = False
            continue
        if current_key is None:
            continue
        if line.strip() == "metadata:":
            in_metadata = True
            continue
        if in_metadata:
            nm = note_re.match(line)
            if nm:
                note_val = nm.group(1).strip().strip('"').replace('\\"', '"').replace("\\\\", "\\")
                result[current_key] = note_val
            in_metadata = False
    return result


def extract_notes(content: str) -> dict[str, str]:
    """Extract key -> commune name from Python source (comments after #)."""
    result = {}
    tuple_re = re.compile(
        r'\s*\(["\']([^"\']*)["\'],\s*["\']([^"\']*)["\']\)\s*:\s*[\d.]+\s*,?\s*#\s*(.+)'
    )
    in_dict = False
    brace_count = 0
    for line in content.splitlines():
        if "taux = {" in line:
            in_dict = True
            brace_count = 1
            continue
        if not in_dict:
            continue
        brace_count += line.count("{") - line.count("}")
        m = tuple_re.search(line)
        if m:
            dep, com, note = m.groups()
            result[f"{dep}_{com}"] = note.strip()
            continue
        if '"manquant"' in line or "'manquant'" in line:
            result["manquant"] = "Clé par défaut si (département, commune) absent"
        if brace_count <= 0:
            break
    return result


def parse_coefficient_2011_yaml(path: Path) -> dict[str, float]:
    """Parse coefficient YAML and return key -> value for 2011-01-01."""
    return _parse_coefficient_yaml_at_date(path, "2011-01-01")


def _parse_coefficient_yaml_at_date(path: Path, date: str) -> dict[str, float]:
    """Parse coefficient YAML and return key -> value for the given date (e.g. 2012-01-01)."""
    key_re = re.compile(r'^("([^"]+)"):\s*$')
    value_re = re.compile(r"^\s+value:\s+([\d.]+)\s*$")
    result = {}
    current_key = None
    in_values = False
    in_date = False
    for line in path.read_text(encoding="utf-8").splitlines():
        m = key_re.match(line)
        if m:
            current_key = m.group(2)
            in_values = False
            in_date = False
            continue
        if current_key is None:
            continue
        if line.strip() == "values:":
            in_values = True
            continue
        if in_values and f'"{date}"' in line:
            in_date = True
            continue
        if in_date:
            vm = value_re.match(line)
            if vm:
                result[current_key] = float(vm.group(1))
            in_date = False
            in_values = False
    return result


def to_key(dep: str, com: str) -> str:
    return f"{dep}_{com}"


def yaml_quote(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{s}"'


def main() -> None:
    # Notes: from Python source if still has dict, else from existing coefficient.yaml
    notes: dict[str, str] = {}
    if NOTE_SOURCE_PY.exists():
        notes_content = NOTE_SOURCE_PY.read_text(encoding="utf-8")
        notes = extract_notes(notes_content)
    if not notes and OUT_YAML.exists():
        notes = parse_notes_from_yaml(OUT_YAML)
    if not notes:
        raise SystemExit("Could not extract notes (from taux_2018.py or coefficient.yaml)")

    # Values per year: 2011 from existing YAML, 2012..2022 from Python files
    values_by_year: dict[int, dict[str, float]] = {}

    if COEFF_2011_YAML.exists():
        values_by_year[2011] = parse_coefficient_2011_yaml(COEFF_2011_YAML)
    elif OUT_YAML.exists():
        values_by_year[2011] = parse_coefficient_2011_yaml(OUT_YAML)
    else:
        values_by_year[2011] = {}

    for year in range(2012, 2023):
        py_path = TCCFE_DIR / f"taux_{year}.py"
        content = py_path.read_text(encoding="utf-8")
        taux = extract_taux_from_py(content)
        if taux:
            manquant_val = taux.pop("manquant", 0.0)  # type: ignore[arg-type]
            values_by_year[year] = {
                to_key(dep, com): val for (dep, com), val in taux.items()
            }
            values_by_year[year]["manquant"] = manquant_val
        elif OUT_YAML.exists():
            values_by_year[year] = _parse_coefficient_yaml_at_date(
                OUT_YAML, f"{year}-01-01"
            )
        else:
            values_by_year[year] = {}

    # All keys = union over years + manquant
    all_keys = set()
    for v in values_by_year.values():
        all_keys |= set(v.keys())
    all_keys.discard("manquant")
    sorted_keys = sorted(k for k in all_keys) + ["manquant"]

    # Verify every key has a note; use placeholder for keys missing from source
    missing_notes = [k for k in sorted_keys if k not in notes]
    if missing_notes:
        print(f"Warning: {len(missing_notes)} keys without commune name (using placeholder)")
        for k in missing_notes:
            notes[k] = "Commune non renseignée"

    # Build coefficient.yaml (only dates when value changes, OpenFisca convention)
    lines = [
        "description: Coefficient multiplicateur TCCFE par (département, commune), toutes années",
        "metadata:",
        "  reference: issue #16",
        "",
    ]
    for key in sorted_keys:
        date_vals = [
            (f"{y}-01-01", values_by_year.get(y, {}).get(key))
            for y in YEARS
        ]
        date_vals = [(d, v) for d, v in date_vals if v is not None]
        # Keep only dates when value changes
        kept = []
        for i, (d, v) in enumerate(date_vals):
            if i == 0 or v != date_vals[i - 1][1]:
                kept.append((d, v))
        lines.append(f'"{key}":')
        lines.append("  metadata:")
        lines.append(f"    note: {yaml_quote(notes[key])}")
        lines.append("  values:")
        for date, val in kept:
            lines.append(f'    "{date}":')
            lines.append(f"      value: {val}")
        lines.append("")

    OUT_YAML.parent.mkdir(parents=True, exist_ok=True)
    OUT_YAML.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_YAML} ({len(sorted_keys)} keys, years {min(YEARS)}–{max(YEARS)})")


if __name__ == "__main__":
    main()
