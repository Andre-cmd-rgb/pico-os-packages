#!/usr/bin/env python3
"""The indexes the board's `pkg` reads: a line a package, tab-separated.

    index.txt    name  version  size  sha256  about
    images.txt   name  source-sha256  size  sha256

Each package is packages/NAME/NAME.pico, its source, and
packages/NAME/package.txt:

    version 1.2
    about what it is, in a few words

The board downloads the source and checks its sha256 against index.txt.
images/NAME is the source compiled by the build with pico-os's picoc;
images.txt says which source each program was made from, so the board
takes a program only for the very source it has, and checks it with
`picoc -t` before using it -- else it compiles the source itself.

    python3 tools/mkindex.py > index.txt
    python3 tools/mkindex.py --images > images.txt
"""
import hashlib
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NAME = re.compile(r"^[a-z][a-z0-9_-]{0,23}$")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def images():
    """The compiled programs in images/, each by the source it came from."""
    print("# pico-os packages compiled by the build: name, source sha256, size, sha256 "
          "(tools/mkindex.py --images)")
    folder = os.path.join(ROOT, "images")
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        image = os.path.join(folder, name)
        src = os.path.join(ROOT, "packages", name, name + ".pico")
        if not NAME.match(name) or not os.path.isfile(src):
            print(f"mkindex: images/{name}: no package of that name", file=sys.stderr)
            return 1
        print(f"{name}\t{sha256(src)}\t{os.path.getsize(image)}\t{sha256(image)}")
    return 0


def main():
    if sys.argv[1:] == ["--images"]:
        return images()
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
