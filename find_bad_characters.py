#!/usr/bin/env python
"""
iteratively find files with "bad" characters that Python doesn't like.
useful for f2py, BibTeX and more.
Michael Hirsch, Ph.D.
"""
import logging
import subprocess
from pathlib import Path
from typing import List
from argparse import ArgumentParser
import shutil
try:
    subprocess.check_call(['iconv', '--version'], stdout=subprocess.DEVNULL)
    FIX = True
except Exception as e:
    FIX = False


def scanbadchar(path: Path, pat: str):
    """
    ext: file extension INCLUDING PERIOD
    """
    path = Path(path).expanduser()
    flist: List[Path]
    if path.is_file():
        flist = [path]
    elif path.is_dir():
        flist = list(path.glob(pat))
    else:
        raise FileNotFoundError(f'{path} not found')

    print(f'Scanning {len(flist)} files in {flist[0].parent}')

    for fn in flist:
        if fn.is_dir():
            continue

        try:
            fn.read_text()
        except UnicodeDecodeError:
            logging.warning(f'BAD character in {fn}')
            if FIX:
                print(f'fixing {fn}')

                shutil.copy2(fn, fn.with_suffix('.bak'))
                # this returns stderr 1 if characters were bad despite conversion success.
                ret = subprocess.check_output(['iconv', '-c', '-f', 'utf-8', '-t', 'ascii', str(fn)],
                                              timeout=5, universal_newlines=True)

                fn.write_text(ret)


def main():
    p = ArgumentParser()
    p.add_argument('path', help='top path to search')
    p.add_argument('ext', help='file glob pattern', nargs='?', default='*')
    P = p.parse_args()

    scanbadchar(P.path, P.ext)


if __name__ == '__main__':
    main()
