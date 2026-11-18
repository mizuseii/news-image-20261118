#!/usr/bin/env python3
"""news-image-20261118 entry (Python 3.13, standard library only).

The entry image is vendored in this repository as entry.png: a
1024x1024 infographic summing up Wednesday 18 November 2026's world
news -- Trump meets Marcos Jr. in Manila and flies on to Shenzhen,
the APEC leaders' summit opens, Cyclone Akvan turns severe over the
Bay of Bengal, and the US-Iran war at sea goes on into day 264.

This program copies that image, byte for byte, to /output/entry.png
(or $MAKEFUN_OUTPUT_DIR). It makes no network calls and writes
identical bytes on every run.

The image itself is drawn by draw_news.py (Pillow, build time only);
main.py needs nothing beyond the standard library at run time.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
TARGET = os.path.join(OUT_DIR, "entry.png")


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    # A plain byte copy is deterministic by construction; confirm the
    # output landed byte-identical to the vendored image.
    assert os.path.getsize(TARGET) == os.path.getsize(SOURCE)
    assert _sha256(TARGET) == _sha256(SOURCE)


if __name__ == "__main__":
    main()
