#!/usr/bin/env python3
"""Replace 'from openfisca_core.model_api import *' with explicit imports. Run from repo root."""

import ast
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


# Get model_api public names at runtime
def get_model_api_names():
    import openfisca_core.model_api as m

    return set(x for x in dir(m) if not x.startswith("_"))


def names_bound_in_file(tree):
    """Names that are bound (params, assignments, imports) so we don't treat them as needing import."""
    bound = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                bound.add(alias.asname or alias.name)
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name != "*":
                    bound.add(alias.asname or alias.name)
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                bound.add(arg.arg)
            if node.args.vararg:
                bound.add(node.args.vararg.arg)
            if node.args.kwarg:
                bound.add(node.args.kwarg.arg)
        if isinstance(node, ast.ClassDef):
            bound.add(node.name)
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    bound.add(t.id)
                elif isinstance(t, ast.Tuple):
                    for e in t.elts:
                        if isinstance(e, ast.Name):
                            bound.add(e.id)
    return bound


def names_used_load(tree):
    """Names used in Load context (reading a value)."""
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)
        if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
            used.add(node.attr)
    return used


def main():
    model_api_names = get_model_api_names()
    star_import_re = re.compile(r"^from openfisca_core\.model_api import \*\s*\n", re.MULTILINE)

    files_changed = 0
    for py_path in REPO_ROOT.glob("openfisca_france_entreprises/**/*.py"):
        text = py_path.read_text(encoding="utf-8")
        if "from openfisca_core.model_api import *" not in text:
            continue
        try:
            tree = ast.parse(text)
        except SyntaxError:
            print("Skip (parse error):", py_path.relative_to(REPO_ROOT), file=sys.stderr)
            continue
        bound = names_bound_in_file(tree)
        used = names_used_load(tree)
        need = (used & model_api_names) - bound
        need_sorted = sorted(need)
        if not need_sorted:
            new_line = ""  # remove the import line
            new_text = star_import_re.sub("", text)
        else:
            imports_str = ", ".join(need_sorted)
            new_line = f"from openfisca_core.model_api import {imports_str}\n"
            new_text = star_import_re.sub(new_line, text, count=1)
        if new_text != text:
            py_path.write_text(new_text, encoding="utf-8")
            files_changed += 1
            print(py_path.relative_to(REPO_ROOT), "->", need_sorted or "(removed)")

    print("Files updated:", files_changed, file=sys.stderr)


if __name__ == "__main__":
    main()
