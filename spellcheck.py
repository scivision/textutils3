#!/usr/bin/env python
"""
Recursive spell check using "aspell"
"""
import shutil
import subprocess
from pathlib import Path
from typing import Sequence
from argparse import ArgumentParser

MAXSIZE = 20e6  # [bytes]

EXE_GRAMMAR = shutil.which('diction')
EXE_SPELL = shutil.which('aspell')
if not EXE_SPELL:
    raise FileNotFoundError('Aspell executable not found')


def findtextfiles(path: Path,
                  globext: Sequence[str],
                  exclude: Sequence[str],
                  checkgrammar: bool = False):
    """finds file to spell check"""
    path = Path(path).expanduser()
    if path.is_file():
        spellchk(path, checkgrammar=checkgrammar)

    if isinstance(globext, str):
        globext = [globext]

    for ext in globext:
        for fn in path.rglob(ext):
            if exclude is not None:
                for ex in exclude:
                    if fn.parent.name.endswith(ex):
                        continue

            spellchk(fn, checkgrammar)


def spellchk(fn: Path, checkgrammar: bool = False):

    subprocess.run([EXE_SPELL, 'check', str(fn)])

    if checkgrammar and EXE_GRAMMAR:
        subprocess.run([EXE_GRAMMAR, str(fn)])


def main():
    p = ArgumentParser(description='searches for TEXT under DIR and echos back filenames')
    p.add_argument('rdir', help='root dir to search', nargs='?', default='.')
    p.add_argument('-g', '--glob', help='glob pattern', nargs='+',
                   default=['*.rst', '*.txt', '*.md', '*.tex'])
    p.add_argument('--exclude', help='directories to exclude', nargs='+',
                   default=['.egg-info'])
    p.add_argument('--nogrammar', action='store_false')
    P = p.parse_args()

    try:
        findtextfiles(P.rdir, P.glob, P.exclude, P.nogrammar)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
