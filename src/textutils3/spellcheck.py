#!/usr/bin/env python3
"""
Recursive spell check using "aspell"
"""

import shutil
import functools
import subprocess
from pathlib import Path
from typing import Sequence, Tuple
from argparse import ArgumentParser

MAXSIZE = 20e6  # [bytes]


def findtextfiles(path: Path, globext: Sequence[str], exclude: Tuple[str], checkgrammar: bool = False):
    """finds file to spell check"""

    path = Path(path).expanduser()
    if path.is_file():
        spellchk(path, checkgrammar=checkgrammar)
        return

    if isinstance(globext, str):
        globext = [globext]

    for ext in globext:
        for fn in path.rglob(ext):
            if exclude is not None:
                if fn.parent.name.endswith(exclude):
                    continue

            spellchk(fn, checkgrammar)


@functools.cache
def get_aspell() -> str:
    p = shutil.which("aspell")
    if not p:
        raise FileNotFoundError("Aspell executable not found")
    return p

@functools.cache
def get_diction() -> str:
    p = shutil.which("diction")
    if not p:
        raise FileNotFoundError("Diction executable not found")
    return p


def spellchk(fn: Path, checkgrammar: bool = False):

    subprocess.check_call([get_aspell(), "check", str(fn)])

    if checkgrammar:
        subprocess.check_call([get_diction(), str(fn)])


def main():
    p = ArgumentParser(description="searches for TEXT under DIR and echos back filenames")
    p.add_argument("rdir", help="root dir to search")
    p.add_argument("-g", "--glob", help="glob pattern", nargs="+", default=["*.rst", "*.txt", "*.md", "*.tex"])
    p.add_argument("--exclude", help="directories to exclude", nargs="+", default=(".egg-info"))
    p.add_argument("--grammar", action="store_true")
    P = p.parse_args()

    try:
        findtextfiles(P.rdir, P.glob, tuple(P.exclude), P.grammar)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
