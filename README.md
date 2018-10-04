[![Build Status](https://travis-ci.com/scivision/textutils.svg?branch=master)](https://travis-ci.com/scivision/textutils)
[![PyPi version](https://img.shields.io/pypi/pyversions/textutils3.svg)](https://pypi.python.org/pypi/textutils3)
[![PyPi Download stats](http://pepy.tech/badge/textutils3)](http://pepy.tech/project/textutils3)


# Recursive Spellcheck
Recursively spellcheck files using aspell or other backend.
Optional grammar highlighting via `diction` is also provided.


## Install 

1. install aspell (optionally, install `diction` the same way)
   * Mac: `brew install aspell`
   * Linux: `apt install aspell`
   * [Windows](http://aspell.net/win32/)
2. Install Python script
   ```sh
   pip install textutils3
   ```
3. usage: from Terminal:
   ```sh
   spellcheck
   ```
   
for help:
```sh
spellcheck -h
```
