#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$ROOT"
mkdir -p build
python3 -c 'import json, pathlib; [json.loads(p.read_text(encoding="utf-8")) for p in pathlib.Path("behavior_pack").rglob("*.json")]; [json.loads(p.read_text(encoding="utf-8")) for p in pathlib.Path("resource_pack").rglob("*.json")]'
python3 generate_textures.py
STAGE="$(mktemp -d build/.naruto-stage.XXXXXX)"
ARCHIVE=build/.naruto-ultimate-shinobi-naruto.$$.mcaddon
trap 'rm -rf "$STAGE"; rm -f "$ARCHIVE"' EXIT HUP INT TERM
cp -R behavior_pack resource_pack "$STAGE/"
(cd "$STAGE" && zip -qr "$ROOT/$ARCHIVE" behavior_pack resource_pack)
mv -f "$ARCHIVE" build/naruto-ultimate-shinobi-naruto.mcaddon
trap - EXIT HUP INT TERM
rm -rf "$STAGE"
printf '%s\n' "Created build/naruto-ultimate-shinobi-naruto.mcaddon"
