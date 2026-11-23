#!/usr/bin/env python3
"""Hand the finished poster to the grader, byte for byte.

The picture is drawn when the entry is built (draw_poster.py) and
kept beside this script as entry.png. This program only carries that
file into the folder the grader reads, so every run of it ends with
the same bytes. It needs no network and no third-party packages.
"""

import os
from pathlib import Path


def deliver() -> None:
    folder = Path(__file__).resolve().parent
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    picture = out_dir / "entry.png"
    picture.write_bytes((folder / "entry.png").read_bytes())
    picture.chmod(0o644)


if __name__ == "__main__":
    deliver()
