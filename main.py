#!/usr/bin/env python3
"""Copy entry.png to the output directory named by MAKEFUN_OUTPUT_DIR
(default /output). Standard library only. Verifies the PNG magic bytes
before copying and byte-compares the copy afterwards."""

import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    with open(src, "rb") as fh:
        data = fh.read()
    if data[:8] != PNG_MAGIC:
        print("entry.png is not a valid PNG (bad magic bytes)",
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        copied = fh.read()
    if copied != data:
        print("copy verification failed: bytes differ", file=sys.stderr)
        return 1
    print("wrote %s %d bytes" % (dst, len(copied)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
