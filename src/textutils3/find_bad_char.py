#!/usr/bin/env python3
"""
iteratively find files with "bad" characters that Python doesn't like.
useful for f2py, BibTeX and more.
"""

import logging
from pathlib import Path
from argparse import ArgumentParser
import shutil
from typing import Iterable


def scanbadchar(path: Path, pat: str, dofix: bool = False):
    """
    path : pathlib.Path
        directory to look under
    pat : str
        filename globbing pattern
    dofix : bool, optional
        rewrite file with bad characters omitted, saving original to filename.bak
    """

    path = Path(path).expanduser()

    flist: Iterable[Path]
    if path.is_file():
        flist = [path]
    elif path.is_dir():
        if not pat:
            raise ValueError("must specify -e filename glob pattern when specifying a directory")
        flist = path.glob(pat)
    else:
        raise FileNotFoundError(path)

    for fn in flist:
        if not fn.is_file():
            continue

        check_bad_char(fn, dofix)


def check_bad_char(file: Path, dofix: bool) -> None:
    finf = file.stat()
    txt = file.read_text(errors="ignore")
    if len(txt) == finf.st_size:
        return

    # bad characters were silently dropped
    logging.warning(f"BAD character in {file}")
    if dofix:
        print(f"fixing {file}")
        shutil.copy2(file, file.with_suffix(".bak"))

        file.write_text(txt)


def main():
    p = ArgumentParser()
    p.add_argument("path", help="top path to search")
    p.add_argument("-e", "--ext", help="file glob pattern")
    p.add_argument("-f", "--fix", help="fix bad files", action="store_true")
    P = p.parse_args()

    scanbadchar(P.path, P.ext, P.fix)


if __name__ == "__main__":
    main()
