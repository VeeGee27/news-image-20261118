#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261118.

Copies the entry image (entry.png, in this repository) to the output
directory as entry.png. Standard library only, no network, deterministic:
both runs write the same bytes.
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
    # Sanity check: the copy must be byte-identical to the source.
    if os.path.getsize(target) != os.path.getsize(SOURCE):
        raise RuntimeError("entry.png copy size mismatch")
    print("wrote", target)


if __name__ == "__main__":
    main()
