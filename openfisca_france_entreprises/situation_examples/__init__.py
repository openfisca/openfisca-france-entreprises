"""This file provides a function to load json example situations."""

import json
from pathlib import Path

DIR_PATH = Path(__file__).resolve().parent


def parse(file_name):
    """Load json example situations."""
    return json.loads((DIR_PATH / file_name).read_text(encoding="utf8"))


single = parse("single.json")
couple = parse("couple.json")
