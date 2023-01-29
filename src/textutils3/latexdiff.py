#!/usr/bin/env python3
"""
recursively runs latexdiff

Assumes old files are all in one directory, and new files are all in another directory.
"""

from argparse import ArgumentParser
from pathlib import Path
import subprocess


def main():
    P = ArgumentParser()
    P.add_argument("old", help="old path")
    P.add_argument("new", help="new path")
    P.add_argument("out", help="output path")
    p = P.parse_args()

    old = Path(p.old).expanduser().resolve(True)
    new = Path(p.new).expanduser().resolve(True)
    out = Path(p.out).expanduser().resolve(True)

    if not (old.is_dir() and new.is_dir() and out.is_dir()):
        raise NotADirectoryError

    if out.samefile(new) or out.samefile(old) or old.samefile(new):
        raise IOError("old and new are same files")

    for fn in old.glob("*.tex"):
        newfn = new / fn.name
        if not newfn.is_file():
            print("skipping non-existent", newfn)
            continue

        print("comparing", fn)

        ret = subprocess.check_output(["latexdiff", str(fn), str(newfn)], text=True)

        (out / fn.name).write_text(ret)


if __name__ == "__main__":
    main()