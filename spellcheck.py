#!/usr/bin/env python
"""
Ctrl \  to abort
"""
import subprocess
from pathlib import Path
from typing import Sequence, Union, Generator
from argparse import ArgumentParser

MAXSIZE = 20e6  # [bytes]

try:
    subprocess.check_call(['diction', '-h'], stdout=subprocess.DEVNULL)
    USEDICTION = True
except Exception:
    USEDICTION = False


def findtext(root: Path, globext: Sequence[str], exclude: Sequence[str],
             checkgrammar: bool = USEDICTION):
    """finds file to spell check"""
    if isinstance(globext, (Path, str)):
        globext = [globext]

    for e in globext:
        # in case "ext" is actually a specific filename
        ext = Path(e).expanduser()
        if ext.is_file():
            spellchk(ext, checkgrammar=checkgrammar)
        else:  # usual case
            spellchklist(Path(root).expanduser().rglob(str(ext)), exclude,
                         checkgrammar)


def spellchklist(flist: Union[Generator[Path, None, None], Sequence[Path]],
                 exclude: Sequence[str],
                 checkgrammar: bool = USEDICTION):
    """Spell check each file"""

    for f in flist:
        spellchk(f, exclude, checkgrammar)


def spellchk(f: Path, exclude: Sequence[str] = None,
             checkgrammar: bool = USEDICTION):

    if exclude is not None:
        for ex in exclude:
            if f.parent.name.endswith(ex):
                return

    try:
        subprocess.check_call(['aspell', 'check', str(f)])
    except Exception as e:  # catch-all for unexpected error
        print(f, e)

    if checkgrammar:
        try:
            subprocess.check_call(['diction', str(f)])
        except Exception as e:  # catch-all for unexpected error
            print(f, e)


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
        findtext(P.rdir, P.glob, P.exclude, P.nogrammar)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
