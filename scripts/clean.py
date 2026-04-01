#!/usr/bin/env python3
"""
Cleans the repo for various generated dirs.
Does not clean in .venv/
"""
from pathlib import Path
import shutil

def remove_pattern(start_path: Path, pattern: str):
    for found_pattern in start_path.rglob(pattern):
        if ".venv" in found_pattern.parts:
            # Stay away from contents in .venv
            continue
        if found_pattern.is_dir():
            print(f"Removing {found_pattern}")
            shutil.rmtree(found_pattern)
        elif found_pattern.is_file():
            print(f"Removing {found_pattern}")
            found_pattern.unlink()

def clean(start: Path):
    remove_pattern(start, "__pycache__")
    remove_pattern(start, "*.egg-info")
    remove_pattern(start, "htmlcov")
    remove_pattern(start, ".pytest_cache")
    remove_pattern(start, ".coverage")

if __name__ == "__main__":
    current_file = Path(__file__).resolve()
    repo_path = current_file.parent.parent
    clean(Path(repo_path))
