[![Build Status](https://travis-ci.com/scivision/textutils3.svg?branch=master)](https://travis-ci.com/scivision/textutils3)
[![PyPi version](https://img.shields.io/pypi/pyversions/textutils3.svg)](https://pypi.python.org/pypi/textutils3)
[![PyPi Download stats](http://pepy.tech/badge/textutils3)](http://pepy.tech/project/textutils3)


# Recursive Spellcheck in Python

Recursively spellcheck files using aspell or other backend.
Optional grammar highlighting via `diction` is also provided.


## Install

1. install aspell (optionally, install `diction` the same way)

   * Mac: `brew install aspell`
   * Linux: `apt install aspell`
   * Windows: See Windows section below.
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

## Windows

[Aspell on Windows](http://aspell.net/win32/)
is provided by the Aspell authors, since Aspell is currently built using Autotools.
You will also have to manually install the dictionary for the desired language.
There are two bugs with Aspell 0.5 on Windows:

1. the spell checker changes the line endings to CRLF, even if no explict changes were specified
2. the spell checker shows a blank screen until a key is pressed (this is true even when Aspell.exe is run directly in Command Prompt).

Thus it is probably better to use Aspell via Windows Subsystem for Linux until this bug is fixed by the Aspell authors.