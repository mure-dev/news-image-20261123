#!/usr/bin/env python3
"""Deliver the finished poster to the grader, byte for byte.

The picture itself is drawn at build time by draw_poster.py and
kept next to this file as entry.png. All this program does is copy
that file into the folder the grader reads, so repeated runs always
produce the same bytes. It uses only the standard library and needs
no network access.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target.mkdir(parents=True, exist_ok=True)
    destination = target / "entry.png"
    shutil.copyfile(here / "entry.png", destination)
    os.chmod(destination, 0o644)


if __name__ == "__main__":
    main()
