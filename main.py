#!/usr/bin/env python3
"""make.fun entry for news-image-20261123.

The grader runs this program twice in a sandbox with no network: the
repository is mounted read-only and /output is writable. The entry image
(entry.png, built by build_image.py) is copied to /output/entry.png,
byte for byte, so both runs write identical bytes.

Locally:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({os.path.getsize(target)} bytes)")


if __name__ == "__main__":
    main()
