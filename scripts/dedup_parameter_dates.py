#!/usr/bin/env python3
"""Deduplicate parameter value dates: when a value does not change over time,
keep only the oldest date and remove immediately following dates with the same value.
"""

from pathlib import Path

import yaml

PARAMETERS_DIR = Path(__file__).resolve().parent.parent / "openfisca_france_entreprises" / "parameters"


def get_value_at_date(entry):
    """Get the comparable value from a date entry (handles {value: x} or nested)."""
    if isinstance(entry, dict) and "value" in entry:
        return entry["value"]
    return entry


def deduplicate_values(values):
    """Return a new values dict keeping only the first date of each run of same value."""
    if not values or not isinstance(values, dict):
        return values
    dates = sorted(values.keys())
    if not dates:
        return values
    to_keep = [dates[0]]
    prev_val = get_value_at_date(values[dates[0]])
    for d in dates[1:]:
        val = get_value_at_date(values[d])
        if val != prev_val:
            to_keep.append(d)
            prev_val = val
    return {d: values[d] for d in to_keep}


def process_file(path: Path) -> bool:
    """Process one YAML file. Return True if modified."""
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "values" not in data:
        return False
    new_values = deduplicate_values(data["values"])
    if len(new_values) == len(data["values"]):
        return False
    data["values"] = new_values
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    return True


def main():
    modified = []
    for path in sorted(PARAMETERS_DIR.rglob("*.yaml")):
        if path.name == "index.yaml":
            continue
        if process_file(path):
            modified.append(path.relative_to(PARAMETERS_DIR))
    for p in modified:
        print(p)
    print(f"Modified {len(modified)} file(s)")


if __name__ == "__main__":
    main()
