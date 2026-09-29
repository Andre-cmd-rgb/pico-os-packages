#!/usr/bin/env python3
"""The index the board's `pkg` reads: a line a package, tab-separated.

    name  version  size  sha256  about

Each package is packages/NAME/NAME.pico, its source, and
packages/NAME/package.txt:

    version 1.2
    about what it is, in a few words

The board downloads the source, checks its sha256 against this line, and
compiles it with its own picoc into ~/bin/NAME: a package is never
compiled for another version of the language than the board speaks.

    python3 tools/mkindex.py > index.txt
"""
import hashlib
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NAME = re.compile(r"^[a-z][a-z0-9_-]{0,23}$")


def main():
    pkgs = os.path.join(ROOT, "packages")
    bad = False
    print("# pico-os packages: name, version, size, sha256, about (tools/mkindex.py)")
    for name in sorted(os.listdir(pkgs)):
        src = os.path.join(pkgs, name, name + ".pico")
        meta = os.path.join(pkgs, name, "package.txt")
        if not NAME.match(name) or not os.path.isfile(src) or not os.path.isfile(meta):
            print(f"mkindex: packages/{name}: wants a lower-case name, {name}.pico and "
                  "package.txt", file=sys.stderr)
            bad = True
            continue
        fields = {}
        for line in open(meta, encoding="utf-8"):
            key, _, value = line.strip().partition(" ")
            if key:
                fields[key] = value.strip()
        if not fields.get("version") or not fields.get("about") or "\t" in fields["about"]:
            print(f"mkindex: packages/{name}/package.txt: wants a version and an about line",
                  file=sys.stderr)
            bad = True
            continue
        data = open(src, "rb").read()
        print(f"{name}\t{fields['version']}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}\t"
              f"{fields['about']}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
