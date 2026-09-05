#!/usr/bin/env python3
"""Raises the pack version in both manifests, keeping them in lockstep.

Minecraft refuses an .mcaddon whose pack UUID and version both match something
already installed, which is what "identical pack detected" means. Bumping the
version makes the import land as an update instead.

header.version, every module version and every dependency version have to move
together: the two packs depend on each other by version, so bumping one alone
leaves a dependency pointing at a version that no longer exists.

Run: python3 tools/bump_version.py [major.minor.patch]
With no argument it bumps the patch number.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFESTS = [os.path.join(ROOT, p, "manifest.json")
             for p in ("pikachu_BP", "pikachu_RP")]


def read_version():
    with open(MANIFESTS[0]) as f:
        return json.load(f)["header"]["version"]


def main():
    if len(sys.argv) > 1:
        try:
            new = [int(n) for n in sys.argv[1].split(".")]
        except ValueError:
            new = []
        if len(new) != 3:
            sys.exit(f"usage: {sys.argv[0]} [major.minor.patch]")
    else:
        cur = read_version()
        new = [cur[0], cur[1], cur[2] + 1]

    for path in MANIFESTS:
        with open(path) as f:
            m = json.load(f)
        m["header"]["version"] = new
        for mod in m.get("modules", []):
            mod["version"] = new
        for dep in m.get("dependencies", []):
            dep["version"] = new
        with open(path, "w") as f:
            json.dump(m, f, indent=2, ensure_ascii=False)
            f.write("\n")

    print("version " + ".".join(str(n) for n in new))


if __name__ == "__main__":
    main()
