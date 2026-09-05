#!/usr/bin/env bash
# Packs both folders into dist/Pikachu.mcaddon, which Minecraft Bedrock imports
# on open. The version is bumped first: the game rejects an .mcaddon whose UUID
# and version both match a pack it already has ("identical pack detected").
# Pass --no-bump to rebuild without touching the version.
set -euo pipefail
cd "$(dirname "$0")"

if [ "${1:-}" != "--no-bump" ]; then
  python3 tools/bump_version.py
fi

python3 tools/validate.py

mkdir -p dist
rm -f dist/Pikachu.mcaddon
zip -r -X -q dist/Pikachu.mcaddon pikachu_BP pikachu_RP \
  -x '*.DS_Store' '__MACOSX/*'

echo "built dist/Pikachu.mcaddon ($(du -h dist/Pikachu.mcaddon | cut -f1))"
